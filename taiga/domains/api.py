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

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.http import Http404

from taiga.base.api import ModelCrudViewSet, UpdateModelMixin

from .base import get_active_domain
from .serializers import DomainSerializer, DomainMemberSerializer
from .permissions import DomainMembersPermission, DomainPermission
from .models import DomainMember, Domain


class DomainViewSet(UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (DomainPermission,)
    serializer_class = DomainSerializer
    queryset = Domain.objects.all()

    def list(self, request, **kwargs):
        domain_data = DomainSerializer(request.domain).data
        if request.domain.user_is_normal_user(request.user):
            domain_data['projects'] = None
        elif request.user.is_anonymous():
            domain_data['projects'] = None
        return Response(domain_data)

    def update(self, request, **kwargs):
        raise Http404

    def create(self, request, **kwargs):
        self.kwargs['pk'] = request.domain.pk
        return super().update(request, pk=request.domain.pk, **kwargs)


class DomainMembersViewSet(ModelCrudViewSet):
    permission_classes = (IsAuthenticated, DomainMembersPermission,)
    serializer_class = DomainMemberSerializer

    def get_queryset(self):
        return DomainMember.objects.filter(domain=get_active_domain()).distinct()
