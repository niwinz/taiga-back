# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
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

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from djmail.template_mail import MagicMailBuilder

from taiga.domains import get_active_domain
from taiga.base import filters
from taiga.base import exceptions as exc
from taiga.base.decorators import list_route, detail_route
from taiga.base.permissions import has_project_perm
from taiga.base.api import ModelCrudViewSet, ModelListViewSet, RetrieveModelMixin
from taiga.base.users.models import Role
from taiga.base.notifications.api import NotificationSenderMixin
from taiga.projects.aggregates.tags import get_all_tags

from . import serializers
from . import models
from . import permissions
from . import services

from .aggregates import stats
from .aggregates import filters as filters_aggr


class ProjectAdminViewSet(ModelCrudViewSet):
    model = models.Project
    serializer_class = serializers.ProjectDetailSerializer
    list_serializer_class = serializers.ProjectSerializer
    permission_classes = (IsAuthenticated, permissions.ProjectAdminPermission)

    def get_queryset(self):
        domain = get_active_domain()
        return domain.projects.all()

    def pre_save(self, obj):
        if not obj.id:
            obj.owner = self.request.user

        # TODO REFACTOR THIS
        if not obj.id:
            obj.template = self.request.QUERY_PARAMS.get('template', None)

        # FIXME

        # Assign domain only if it current
        # value is None
        if not obj.domain:
            obj.domain = self.request.domain

        super().pre_save(obj)


class ProjectViewSet(ModelCrudViewSet):
    model = models.Project
    serializer_class = serializers.ProjectDetailSerializer
    list_serializer_class = serializers.ProjectSerializer
    permission_classes = (IsAuthenticated, permissions.ProjectPermission)

    @detail_route(methods=['get'])
    def stats(self, request, pk=None):
        project = self.get_object()
        return Response(stats.get_stats_for_project(project))

    @detail_route(methods=['get'])
    def issues_stats(self, request, pk=None):
        project = self.get_object()
        return Response(stats.get_stats_for_project_issues(project))

    @detail_route(methods=['get'])
    def issue_filters_data(self, request, pk=None):
        project = self.get_object()
        return Response(filters_aggr.get_issues_filters_data(project))

    @detail_route(methods=['get'])
    def tags(self, request, pk=None):
        project = self.get_object()
        return Response(get_all_tags(project))

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(owner=self.request.user) |
                       Q(members=self.request.user)).filter(domain=get_active_domain())
        return qs.distinct()

    def pre_save(self, obj):
        if not obj.id:
            obj.owner = self.request.user

        # FIXME

        # Assign domain only if it current
        # value is None
        if not obj.domain:
            obj.domain = self.request.domain

        super().pre_save(obj)


class MembershipViewSet(ModelCrudViewSet):
    model = models.Membership
    serializer_class = serializers.MembershipSerializer
    permission_classes = (IsAuthenticated, permissions.MembershipPermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            qs = self.model.objects.filter(Q(project_id=serializer.data["project"],
                                             user__email=serializer.data["email"]) |
                                           Q(project_id=serializer.data["project"],
                                             email=serializer.data["email"]))
            if qs.count() > 0:
                raise exc.WrongArguments(_("Email address is already taken."))

            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, object):
        # Only assign new token if a current token value is empty.
        if not object.token:
            object.token = str(uuid.uuid1())

        super().pre_save(object)

    def post_save(self, object, created=False):
        super().post_save(object, created=created)

        if not created:
            return

        # Send email only if a new membership is created
        mbuilder = MagicMailBuilder()
        email = mbuilder.membership_invitation(object.email, {"membership": object})
        email.send()


class InvitationViewSet(RetrieveModelMixin, viewsets.ReadOnlyModelViewSet):
    """
    Only used by front for get invitation by it token.
    """
    queryset = models.Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    lookup_field = "token"
    permission_classes = (AllowAny,)

    def list(self, *args, **kwargs):
        raise exc.PermissionDenied(_("You don't have permisions to see that."))


class RolesViewSet(ModelCrudViewSet):
    model = Role
    serializer_class = serializers.RoleSerializer
    permission_classes = (IsAuthenticated, permissions.RolesPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ('project',)

# User Stories commin ViewSets

class BulkUpdateOrderMixin:
    """
    This mixin need three fields in the child class:

    - bulk_update_param: that the name of the field of the data received from
      the cliente that contains the pairs (id, order) to sort the objects.
    - bulk_update_perm: that containts the codename of the permission needed to
      sort.
    - bulk_update_service: that is a object with the bulk_update_order method
      for ordering the object.
    """

    @list_route(methods=["POST"])
    def bulk_update_order(self, request, **kwargs):
        bulk_data = request.DATA.get(self.bulk_update_param, None)

        if bulk_data is None:
            raise exc.BadRequest(_("%s parameter is mandatory") % self.bulk_update_param)

        project_id = request.DATA.get('project', None)
        if project_id is None:
            raise exc.BadRequest(_("project parameter ir mandatory"))

        project = get_object_or_404(models.Project, id=project_id)

        if request.user != project.owner and not has_project_perm(request.user, project, self.bulk_update_perm):
            raise exc.PermissionDenied(_("You don't have permisions %s.") % self.bulk_update_perm)

        self.bulk_update_service.bulk_update_order(project, request.user, bulk_data)

        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

class PointsViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.Points
    serializer_class = serializers.PointsSerializer
    permission_classes = (IsAuthenticated, permissions.PointsPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ('project',)
    bulk_update_param = "bulk_points"
    bulk_update_perm = "change_points"
    bulk_update_service = services.PointsService()


class UserStoryStatusViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.UserStoryStatus
    serializer_class = serializers.UserStoryStatusSerializer
    permission_classes = (IsAuthenticated, permissions.UserStoryStatusPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ('project',)
    bulk_update_param = "bulk_userstory_statuses"
    bulk_update_perm = "change_userstorystatus"
    bulk_update_service = services.UserStoryStatusesService()


class TaskStatusViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.TaskStatus
    serializer_class = serializers.TaskStatusSerializer
    permission_classes = (IsAuthenticated, permissions.TaskStatusPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_task_statuses"
    bulk_update_perm = "change_taskstatus"
    bulk_update_service = services.TaskStatusesService()


class SeverityViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.Severity
    serializer_class = serializers.SeveritySerializer
    permission_classes = (IsAuthenticated, permissions.SeverityPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_severities"
    bulk_update_perm = "change_severity"
    bulk_update_service = services.SeveritiesService()


class PriorityViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.Priority
    serializer_class = serializers.PrioritySerializer
    permission_classes = (IsAuthenticated, permissions.PriorityPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_priorities"
    bulk_update_perm = "change_priority"
    bulk_update_service = services.PrioritiesService()


class IssueTypeViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.IssueType
    serializer_class = serializers.IssueTypeSerializer
    permission_classes = (IsAuthenticated, permissions.IssueTypePermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_issue_types"
    bulk_update_perm = "change_issuetype"
    bulk_update_service = services.IssueTypesService()


class IssueStatusViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.IssueStatus
    serializer_class = serializers.IssueStatusSerializer
    permission_classes = (IsAuthenticated, permissions.IssueStatusPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_issue_statuses"
    bulk_update_perm = "change_issuestatus"
    bulk_update_service = services.IssueStatusesService()


class QuestionStatusViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.QuestionStatus
    serializer_class = serializers.QuestionStatusSerializer
    permission_classes = (IsAuthenticated, permissions.QuestionStatusPermission)
    filter_backends = (filters.IsProjectMemberFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_question_statuses"
    bulk_update_perm = "change_questionstatus"
    bulk_update_service = services.QuestionStatusesService()
