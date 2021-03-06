# -*- coding: utf-8 -*-

import json
import reversion

from rest_framework import serializers

from ..userstories.serializers import UserStorySerializer
from . import models



class MilestoneSerializer(serializers.ModelSerializer):
    user_stories = UserStorySerializer(many=True, required=False)
    closed_points = serializers.FloatField(source='closed_points', required=False)
    client_increment_points = serializers.FloatField(source='client_increment_points', required=False)
    team_increment_points = serializers.FloatField(source='team_increment_points', required=False)

    class Meta:
        model = models.Milestone
