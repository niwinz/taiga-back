# Copyright 2014 Andrey Antukh <niwi@niwi.be>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# y ou may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import string

from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .base import clear_domain_cache


def _simple_domain_name_validator(value):
    """
    Validates that the given value contains no whitespaces to prevent common
    typos.
    """
    if not value:
        return

    checks = ((s in value) for s in string.whitespace)
    if any(checks):
        raise ValidationError(
            _("The domain name cannot contain any spaces or tabs."),
            code='invalid',
        )


class Domain(models.Model):
    domain = models.CharField(_('domain name'), max_length=255, unique=True,
                              validators=[_simple_domain_name_validator])
    name = models.CharField(_('display name'), max_length=255)
    scheme = models.CharField(_('scheme'), max_length=60, null=True, default=None)

    # Site Metadata
    public_register = models.BooleanField(default=False)
    default_language = models.CharField(max_length=20, null=False, blank=True, default="",
                                        verbose_name=_("default language"))

    alias_of = models.ForeignKey("self", null=True, default=None, blank=True,
                                 verbose_name=_("Mark as alias of"), related_name="+")

    class Meta:
        verbose_name = _('domain')
        verbose_name_plural = _('domain')
        ordering = ('domain',)

    def __str__(self):
        return self.domain

    def user_is_owner(self, user):
        return self.members.filter(user_id=user.id, is_owner=True).exists()

    def user_is_staff(self, user):
        return self.members.filter(user_id=user.id, is_staff=True).exists()

    def user_is_normal_user(self, user):
        return self.members.filter(user_id=user.id, is_owner=False, is_staff=False).exists()


class DomainMember(models.Model):
    domain = models.ForeignKey("Domain", related_name="members", null=True)
    user = models.ForeignKey("users.User", related_name="+", null=True)

    email = models.EmailField(max_length=255)
    is_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        ordering = ["email"]
        verbose_name = "Domain Member"
        verbose_name_plural = "Domain Members"
        unique_together = ("domain", "user")

    def __str__(self):
        return "DomainMember: {0}:{1}".format(self.domain, self.user)


pre_save.connect(clear_domain_cache, sender=Domain)
pre_delete.connect(clear_domain_cache, sender=Domain)

@receiver(pre_delete, sender=DomainMember, dispatch_uid="domain_member_pre_delete")
def domain_member_pre_delete(sender, instance, *args, **kwargs):
    for domain_project in instance.domain.projects.all():
        domain_project.memberships.filter(user=instance.user).delete()
