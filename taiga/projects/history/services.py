# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This module contains a main domain logic for object history management.
This is possible example:

  from taiga.projects import history

  class ViewSet(restfw.ViewSet):
      def create(request):
          object = get_some_object()
          history.freeze(object)
          # Do something...
          history.persist_history(object, user=request.user)
"""

from collections import namedtuple
from functools import partial, wraps, lru_cache

from django.db.models.loading import get_model
from django.db import transaction as tx
from django.contrib.contenttypes.models import ContentType

from .models import HistoryType

# Type that represents a freezed object
FrozenObj = namedtuple("FrozenObj", ["id", "type", "value"])
Diff = namedtuple("Diff", ["id", "type", "value", "snapshot"])

# Dict containing registred contentypes with their freeze implementation.
_freeze_impl_map = {}

# Dict containing freeze history
_frozen_objects_storage = {}


# Local, in-process freeze objects storage interface.

def make_key_from_frozen_object(obj:FrozenObj) -> str:
    """
    Create unique key from FrozenObj.
    """
    return "{0}:{1}".format(obj.type, obj.id)


def make_key_from_model_object(obj:object) -> str:
    """
    Create unique key from model instance.
    """
    tn = get_typename_for_model_class(obj.__class__)
    return "{0}:{1}".format(tn, obj.pk)


def store_frozen_object(key:str, obj:FrozenObj):
    """
    Persist on in-process storage the specified frozen
    object instance.
    """
    _frozen_objects_storage[key] = obj


def get_stored_frozen_object(key:str):
    """
    Get previously stored frozen object instance by key.
    """
    return _frozen_objects_storage[key]


def clear_frozen_objects_storage():
    """
    Clear in-process storage related to frozen objects.
    """
    _frozen_objects_storage.clear()


def get_typename_for_model_class(model:object) -> str:
    """
    Get typename for model instance.
    """
    ct = ContentType.objects.get_for_model(model)
    return "{0}.{1}".format(ct.app_label, ct.model)


def register_freeze_implementation(fn=None, *, typename:str=None):
    """
    Register freeze implementation for specified typename.

    This function can be used as decorator.
    """

    if fn is None:
        return partial(register_freeze_implementation, typename=typename)

    if typename is None:
        raise RuntimeError("typename must be specied")

    @wraps(fn)
    def _wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    _freeze_impl_map[typename] = _wrapper
    return _wrapper


# Low level api

def freeze_model_instance(obj:object) -> FrozenObj:
    """
    Creates a new frozen object from model instance.

    The freeze process consists on converting model
    instances to hashable plain python objects and
    wrapped into FrozenObj.
    """

    type = get_typename_for_model_class(obj.__class__)
    if type not in _freeze_impl_map:
        raise RuntimeError("No implementation found for {}".format(type))

    impl_fn = _freeze_impl_map[type]
    return FrozenObj(obj.id, type, impl_fn(obj))


def make_diff(oldobj:FrozenObj, newobj:FrozenObj) -> Diff:
    """
    Compute a diff between two frozen objects.
    """
    assert oldobj.type == newobj.type, "Two diff objects should be of same type."
    assert isinstance(oldobj, FrozenObj), "oldobj should be of FrozenObj type"
    assert isinstance(newobj, FrozenObj), "newobj should be of FrozenObj type"

    first, second = oldobj.value, newobj.value
    diff = {}
    not_found_value = None

    # Check all keys in first dict
    for key in first:
        if key not in second:
            diff[key] = (first[key], not_found_value)
        elif first[key] != second[key]:
            diff[key] = (first[key], second[key])

    # Check all keys in second dict to find missing
    for key in second:
        if key not in first:
            diff[key] = (not_found_value, second[key])

    return Diff(newobj.id, newobj.type, diff, newobj)


def persist_change_entry(diff:Diff, *, user=None):
    """
    Create new history entry of "change" type from diff.
    """
    entry_model = get_model("history", "HistoryEntry")
    key = make_key_from_frozen_object(diff)

    entry = entry_model.objects.create(owner=user,
                                       key=key,
                                       type=HistoryType.change,
                                       diff=diff.value,
                                       snapshot=diff.snapshot.value)
    return entry


def persist_comment_entry(key:str, comment:str, *, user=None):
    """
    Create a new history entry of "comment" type.
    """
    entry_model = get_model("history", "HistoryEntry")
    entry = entry_model.objects.create(owner=user,
                                       key=key,
                                       type=HistoryType.comment,
                                       comment=comment)
    return entry


def persist_delete_entry(obj:FrozenObj, *, user=None):
    """
    Create new history entry of "delete" type.
    """
    entry_model = get_model("history", "HistoryEntry")
    key = make_key_from_frozen_object(obj)

    entry = entry_model.objects.create(owner=user,
                                       key=key,
                                       type=HistoryType.delete,
                                       snapshot=obj.value)
    return entry


def persist_create_entry(obj:FrozenObj, *, user=None):
    """
    Create new history entry of "create" type.
    """
    entry_model = get_model("history", "HistoryEntry")
    key = make_key_from_frozen_object(obj)

    entry = entry_model.objects.create(owner=user,
                                       key=key,
                                       type=HistoryType.create,
                                       snapshot=obj.value)
    return entry


# High level api.

def freeze(obj:object):
    """
    Given any model instance with registred content type,
    persist its frozen representation on in-process storage.

    Repeated calls with same object replaces the previously
    stored object.
    """

    fobj = freeze_model_instance(obj)
    fkey = make_key_from_frozen_object(fobj)

    store_frozen_object(fkey, fobj)


@tx.atomic
def persist_change(obj:object, *, user=None):
    """
    Given any model instance with registred content type,
    create new history entry of "change" type.

    This raises exception in case of object wasn't
    previously freezed.
    """

    key = make_key_from_model_object(obj)
    new_fobj = freeze_model_instance(obj)
    old_fobj = get_stored_frozen_object(key)

    diff = make_diff(old_fobj, new_fobj)
    return persist_change_entry(diff, user=user)


@tx.atomic
def persist_create(obj:object, *, user=None):
    """
    Given any model instance with registred content type,
    create new history entry of "create" type.
    """

    fobj = freeze_model_instance(obj)
    return persist_create_entry(fobj, user=user)


@tx.atomic
def persist_delete(obj:object, *, user=None):
    """
    Given any model instance with registred content type,
    create new history entry of "delete" type.
    """
    fobj = freeze_model_instance(obj)
    return persist_delete_entry(fobj, user=user)


@tx.atomic
def persist_comment(obj:object, comment:str, *, user=None):
    """
    Given any model instance with registred content type,
    create new history entry of "comment" type.
    """
    key = make_key_from_model_object(obj)
    return persist_comment_entry(key, comment, user=user)


# Freeze implementatitions
from .freeze_impl import userstory_freezer

register_freeze_implementation(userstory_freezer, typename="userstories.userstory")
