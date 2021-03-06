# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated

from taiga.base import filters
from taiga.base.api import ModelCrudViewSet

from . import serializers
from . import models
from . import permissions


class DocumentsViewSet(ModelCrudViewSet):
    model = models.Document
    serializer_class = serializers.DocumentSerializer
    permission_classes = (permissions.DocumentPermission,)
    filter_backends = (filters.IsProjectMemberFilterBackend,)

