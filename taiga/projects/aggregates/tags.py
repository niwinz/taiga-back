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

from contextlib import closing
from django.db import connection

def _get_issues_tags(project):
    extra_sql = ("select unnest(unpickle(tags)) as tagname "
                 "from issues_issue where project_id = %s "
                 "group by unnest(unpickle(tags)) "
                 "order by tagname asc")

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [project.id])
        rows = cursor.fetchall()

    return set([x[0] for x in rows])

def _get_stories_tags(project):
    extra_sql = ("select unnest(unpickle(tags)) as tagname, count(unnest(unpickle(tags))) "
                 "from userstories_userstory where project_id = %s "
                 "group by unnest(unpickle(tags)) "
                 "order by tagname asc")

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [project.id])
        rows = cursor.fetchall()

    return set([x[0] for x in rows])

def get_all_tags(project):
    result = set()
    result.update(_get_issues_tags(project))
    result.update(_get_stories_tags(project))
    return sorted(result)
