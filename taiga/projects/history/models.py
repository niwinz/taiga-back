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

import uuid
import enum

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.functional import cached_property
from django_pgjson.fields import JsonField


class HistoryType(enum.IntEnum):
    comment = 1
    change = 2
    create = 3
    delete = 4


class HistoryEntry(models.Model):
    """
    Domain model that represents a history
    entry storage table.

    It is used for store object changes and
    comments.
    """

    TYPE_CHOICES = ((HistoryType.comment, _("Comment")),
                    (HistoryType.change, _("Change")),
                    (HistoryType.create, _("Create")),
                    (HistoryType.delete, _("Delete")),)

    id = models.CharField(primary_key=True, max_length=255, unique=True,
                          editable=False, default=lambda: str(uuid.uuid1()))

    owner = models.ForeignKey("users.User", null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    key = models.CharField(max_length=255, null=True, default=None, blank=True)

    diff = JsonField(null=True, default=None)
    snapshot = JsonField(null=True, default=None)
    comment = models.TextField(blank=True)

    @cached_property
    def is_comment(self):
        return self.type == HistoryType.comment

    class Meta:
        ordering = ["created_at"]

