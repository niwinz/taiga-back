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

from django.db import transaction
from django.db import connection

from . import models


class UserStoryStatusesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_userstorystatus set "order" = $1
            where projects_userstorystatus.id = $2 and
                  projects_userstorystatus.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()


class PointsService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_points set "order" = $1
            where projects_points.id = $2 and
                  projects_points.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()

class TaskStatusesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_taskstatus set "order" = $1
            where projects_taskstatus.id = $2 and
                  projects_taskstatus.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()


class IssueStatusesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_issuestatus set "order" = $1
            where projects_issuestatus.id = $2 and
                  projects_issuestatus.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()


class IssueTypesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_issuetype set "order" = $1
            where projects_issuetype.id = $2 and
                  projects_issuetype.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()


class PrioritiesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_priority set "order" = $1
            where projects_priority.id = $2 and
                  projects_priority.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()


class SeveritiesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_severity set "order" = $1
            where projects_severity.id = $2 and
                  projects_severity.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()


class QuestionStatusesService(object):
    @transaction.atomic
    def bulk_update_order(self, project, user, data):
        cursor = connection.cursor()

        sql = """
        prepare bulk_update_order as update projects_questionstatus set "order" = $1
            where projects_questionstatus.id = $2 and
                  projects_questionstatus.project_id = $3;
        """

        cursor.execute(sql)
        for id, order in data:
            cursor.execute("EXECUTE bulk_update_order (%s, %s, %s);",
                           (order, id, project.id))
        cursor.close()
