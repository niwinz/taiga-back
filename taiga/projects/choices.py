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

from django.utils.translation import ugettext_lazy as _


US_STATUSES = (
    (1, _("Open"), False, True, "#669933"),
    (2, _("Closed"), True, False, "#999999"),
)

TASK_STATUSES = (
    (1, _("New"), False, True,  "#999999"),
    (2, _("In progress"), False, False, "#ff9900"),
    (3, _("Ready for test"), True, False, "#ffcc00"),
    (4, _("Closed"), True, False, "#669900"),
    (5, _("Needs Info"), False, False, "#999999"),
)

POINTS_CHOICES = (
    (1, u'?', None, True),
    (2,  u'0', 0, False),
    (3, u'1/2', 0.5, False),
    (4,  u'1', 1, False),
    (5,  u'2', 2, False),
    (6,  u'3', 3, False),
    (7,  u'5', 5, False),
    (8,  u'8', 8, False),
    (9, u'10', 10, False),
    (10, u'15', 15, False),
    (11, u'20', 20, False),
    (12, u'40', 40, False),
)

PRIORITY_CHOICES = (
    (1, _(u'Low'), '#666666', False),
    (3, _(u'Normal'), '#669933', True),
    (5, _(u'High'), '#CC0000', False),
)

SEVERITY_CHOICES = (
    (1, _(u'Wishlist'), '#666666', False),
    (2, _(u'Minor'), '#669933', False),
    (3, _(u'Normal'), '#0000FF', True),
    (4, _(u'Important'), '#FFA500', False),
    (5, _(u'Critical'), '#CC0000', False),
)

ISSUE_STATUSES = (
    (1, _("New"), False, '#8C2318', True),
    (2, _("In progress"), False, '#5E8C6A', False),
    (3, _("Ready for test"), True, '#88A65E', False),
    (4, _("Closed"), True, '#BFB35A', False),
    (5, _("Needs Info"), False, '#89BAB4', False),
    (6, _("Rejected"), True, '#CC0000', False),
    (7, _("Postponed"), False, '#666666', False),
)

ISSUE_TYPES = (
    (1, _(u'Bug'), '#89BAB4', True),
)

QUESTION_STATUS = (
    (1, _("Pending"), False, '#FFA500', True),
    (2, _("Answered"), False, '#669933', False),
    (3, _("Closed"), True,'#BFB35A', False),
)

ROLES = (
    (10, "ux", "UX", True, [
        [ "add_issue", "issues", "issue" ],
        [ "change_issue", "issues", "issue" ],
        [ "delete_issue", "issues", "issue" ],
        [ "view_issue", "issues", "issue" ],
        [ "add_milestone", "milestones", "milestone" ],
        [ "change_milestone", "milestones", "milestone" ],
        [ "delete_milestone", "milestones", "milestone" ],
        [ "view_milestone", "milestones", "milestone" ],
        [ "add_attachment", "projects", "attachment" ],
        [ "change_attachment", "projects", "attachment" ],
        [ "delete_attachment", "projects", "attachment" ],
        [ "view_attachment", "projects", "attachment" ],
        [ "add_issuestatus", "projects", "issuestatus" ],
        [ "change_issuestatus", "projects", "issuestatus" ],
        [ "delete_issuestatus", "projects", "issuestatus" ],
        [ "view_issuestatus", "projects", "issuestatus" ],
        [ "add_issuetype", "projects", "issuetype" ],
        [ "change_issuetype", "projects", "issuetype" ],
        [ "delete_issuetype", "projects", "issuetype" ],
        [ "view_issuetype", "projects", "issuetype" ],
        [ "add_membership", "projects", "membership" ],
        [ "change_membership", "projects", "membership" ],
        [ "delete_membership", "projects", "membership" ],
        [ "view_membership", "projects", "membership" ],
        [ "add_points", "projects", "points" ],
        [ "change_points", "projects", "points" ],
        [ "delete_points", "projects", "points" ],
        [ "view_points", "projects", "points" ],
        [ "add_priority", "projects", "priority" ],
        [ "change_priority", "projects", "priority" ],
        [ "delete_priority", "projects", "priority" ],
        [ "view_priority", "projects", "priority" ],
        [ "add_project", "projects", "project" ],
        [ "change_project", "projects", "project" ],
        [ "delete_project", "projects", "project" ],
        [ "view_project", "projects", "project" ],
        [ "add_severity", "projects", "severity" ],
        [ "change_severity", "projects", "severity" ],
        [ "delete_severity", "projects", "severity" ],
        [ "view_severity", "projects", "severity" ],
        [ "add_taskstatus", "projects", "taskstatus" ],
        [ "change_taskstatus", "projects", "taskstatus" ],
        [ "delete_taskstatus", "projects", "taskstatus" ],
        [ "view_taskstatus", "projects", "taskstatus" ],
        [ "add_userstorystatus", "projects", "userstorystatus" ],
        [ "change_userstorystatus", "projects", "userstorystatus" ],
        [ "delete_userstorystatus", "projects", "userstorystatus" ],
        [ "view_userstorystatus", "projects", "userstorystatus" ],
        [ "add_task", "tasks", "task" ],
        [ "change_task", "tasks", "task" ],
        [ "delete_task", "tasks", "task" ],
        [ "view_task", "tasks", "task" ],
        [ "add_role", "users", "role" ],
        [ "change_role", "users", "role" ],
        [ "delete_role", "users", "role" ],
        [ "view_role", "users", "role" ],
        [ "change_user", "users", "user" ],
        [ "view_user", "users", "user" ],
        [ "add_rolepoints", "userstories", "rolepoints" ],
        [ "change_rolepoints", "userstories", "rolepoints" ],
        [ "delete_rolepoints", "userstories", "rolepoints" ],
        [ "view_rolepoints", "userstories", "rolepoints" ],
        [ "add_userstory", "userstories", "userstory" ],
        [ "change_userstory", "userstories", "userstory" ],
        [ "delete_userstory", "userstories", "userstory" ],
        [ "view_userstory", "userstories", "userstory" ],
        [ "add_wikipage", "wiki", "wikipage" ],
        [ "change_wikipage", "wiki", "wikipage" ],
        [ "delete_wikipage", "wiki", "wikipage" ],
        [ "view_wikipage", "wiki", "wikipage" ]
    ]),
    (20, "design", "Design", True, [
        [ "add_issue", "issues", "issue" ],
        [ "change_issue", "issues", "issue" ],
        [ "delete_issue", "issues", "issue" ],
        [ "view_issue", "issues", "issue" ],
        [ "add_milestone", "milestones", "milestone" ],
        [ "change_milestone", "milestones", "milestone" ],
        [ "delete_milestone", "milestones", "milestone" ],
        [ "view_milestone", "milestones", "milestone" ],
        [ "add_attachment", "projects", "attachment" ],
        [ "change_attachment", "projects", "attachment" ],
        [ "delete_attachment", "projects", "attachment" ],
        [ "view_attachment", "projects", "attachment" ],
        [ "add_issuestatus", "projects", "issuestatus" ],
        [ "change_issuestatus", "projects", "issuestatus" ],
        [ "delete_issuestatus", "projects", "issuestatus" ],
        [ "view_issuestatus", "projects", "issuestatus" ],
        [ "add_issuetype", "projects", "issuetype" ],
        [ "change_issuetype", "projects", "issuetype" ],
        [ "delete_issuetype", "projects", "issuetype" ],
        [ "view_issuetype", "projects", "issuetype" ],
        [ "add_membership", "projects", "membership" ],
        [ "change_membership", "projects", "membership" ],
        [ "delete_membership", "projects", "membership" ],
        [ "view_membership", "projects", "membership" ],
        [ "add_points", "projects", "points" ],
        [ "change_points", "projects", "points" ],
        [ "delete_points", "projects", "points" ],
        [ "view_points", "projects", "points" ],
        [ "add_priority", "projects", "priority" ],
        [ "change_priority", "projects", "priority" ],
        [ "delete_priority", "projects", "priority" ],
        [ "view_priority", "projects", "priority" ],
        [ "add_project", "projects", "project" ],
        [ "change_project", "projects", "project" ],
        [ "delete_project", "projects", "project" ],
        [ "view_project", "projects", "project" ],
        [ "add_severity", "projects", "severity" ],
        [ "change_severity", "projects", "severity" ],
        [ "delete_severity", "projects", "severity" ],
        [ "view_severity", "projects", "severity" ],
        [ "add_taskstatus", "projects", "taskstatus" ],
        [ "change_taskstatus", "projects", "taskstatus" ],
        [ "delete_taskstatus", "projects", "taskstatus" ],
        [ "view_taskstatus", "projects", "taskstatus" ],
        [ "add_userstorystatus", "projects", "userstorystatus" ],
        [ "change_userstorystatus", "projects", "userstorystatus" ],
        [ "delete_userstorystatus", "projects", "userstorystatus" ],
        [ "view_userstorystatus", "projects", "userstorystatus" ],
        [ "add_task", "tasks", "task" ],
        [ "change_task", "tasks", "task" ],
        [ "delete_task", "tasks", "task" ],
        [ "view_task", "tasks", "task" ],
        [ "add_role", "users", "role" ],
        [ "change_role", "users", "role" ],
        [ "delete_role", "users", "role" ],
        [ "view_role", "users", "role" ],
        [ "change_user", "users", "user" ],
        [ "view_user", "users", "user" ],
        [ "add_rolepoints", "userstories", "rolepoints" ],
        [ "change_rolepoints", "userstories", "rolepoints" ],
        [ "delete_rolepoints", "userstories", "rolepoints" ],
        [ "view_rolepoints", "userstories", "rolepoints" ],
        [ "add_userstory", "userstories", "userstory" ],
        [ "change_userstory", "userstories", "userstory" ],
        [ "delete_userstory", "userstories", "userstory" ],
        [ "view_userstory", "userstories", "userstory" ],
        [ "add_wikipage", "wiki", "wikipage" ],
        [ "change_wikipage", "wiki", "wikipage" ],
        [ "delete_wikipage", "wiki", "wikipage" ],
        [ "view_wikipage", "wiki", "wikipage" ]
    ]),
    (30, "front", "Front", True, [
        [ "add_issue", "issues", "issue" ],
        [ "change_issue", "issues", "issue" ],
        [ "delete_issue", "issues", "issue" ],
        [ "view_issue", "issues", "issue" ],
        [ "add_milestone", "milestones", "milestone" ],
        [ "change_milestone", "milestones", "milestone" ],
        [ "delete_milestone", "milestones", "milestone" ],
        [ "view_milestone", "milestones", "milestone" ],
        [ "add_attachment", "projects", "attachment" ],
        [ "change_attachment", "projects", "attachment" ],
        [ "delete_attachment", "projects", "attachment" ],
        [ "view_attachment", "projects", "attachment" ],
        [ "add_issuestatus", "projects", "issuestatus" ],
        [ "change_issuestatus", "projects", "issuestatus" ],
        [ "delete_issuestatus", "projects", "issuestatus" ],
        [ "view_issuestatus", "projects", "issuestatus" ],
        [ "add_issuetype", "projects", "issuetype" ],
        [ "change_issuetype", "projects", "issuetype" ],
        [ "delete_issuetype", "projects", "issuetype" ],
        [ "view_issuetype", "projects", "issuetype" ],
        [ "add_membership", "projects", "membership" ],
        [ "change_membership", "projects", "membership" ],
        [ "delete_membership", "projects", "membership" ],
        [ "view_membership", "projects", "membership" ],
        [ "add_points", "projects", "points" ],
        [ "change_points", "projects", "points" ],
        [ "delete_points", "projects", "points" ],
        [ "view_points", "projects", "points" ],
        [ "add_priority", "projects", "priority" ],
        [ "change_priority", "projects", "priority" ],
        [ "delete_priority", "projects", "priority" ],
        [ "view_priority", "projects", "priority" ],
        [ "add_project", "projects", "project" ],
        [ "change_project", "projects", "project" ],
        [ "delete_project", "projects", "project" ],
        [ "view_project", "projects", "project" ],
        [ "add_severity", "projects", "severity" ],
        [ "change_severity", "projects", "severity" ],
        [ "delete_severity", "projects", "severity" ],
        [ "view_severity", "projects", "severity" ],
        [ "add_taskstatus", "projects", "taskstatus" ],
        [ "change_taskstatus", "projects", "taskstatus" ],
        [ "delete_taskstatus", "projects", "taskstatus" ],
        [ "view_taskstatus", "projects", "taskstatus" ],
        [ "add_userstorystatus", "projects", "userstorystatus" ],
        [ "change_userstorystatus", "projects", "userstorystatus" ],
        [ "delete_userstorystatus", "projects", "userstorystatus" ],
        [ "view_userstorystatus", "projects", "userstorystatus" ],
        [ "add_task", "tasks", "task" ],
        [ "change_task", "tasks", "task" ],
        [ "delete_task", "tasks", "task" ],
        [ "view_task", "tasks", "task" ],
        [ "add_role", "users", "role" ],
        [ "change_role", "users", "role" ],
        [ "delete_role", "users", "role" ],
        [ "view_role", "users", "role" ],
        [ "change_user", "users", "user" ],
        [ "view_user", "users", "user" ],
        [ "add_rolepoints", "userstories", "rolepoints" ],
        [ "change_rolepoints", "userstories", "rolepoints" ],
        [ "delete_rolepoints", "userstories", "rolepoints" ],
        [ "view_rolepoints", "userstories", "rolepoints" ],
        [ "add_userstory", "userstories", "userstory" ],
        [ "change_userstory", "userstories", "userstory" ],
        [ "delete_userstory", "userstories", "userstory" ],
        [ "view_userstory", "userstories", "userstory" ],
        [ "add_wikipage", "wiki", "wikipage" ],
        [ "change_wikipage", "wiki", "wikipage" ],
        [ "delete_wikipage", "wiki", "wikipage" ],
        [ "view_wikipage", "wiki", "wikipage" ]
    ]),
    (40, "back", "Back", True, [
        [ "add_issue", "issues", "issue" ],
        [ "change_issue", "issues", "issue" ],
        [ "delete_issue", "issues", "issue" ],
        [ "view_issue", "issues", "issue" ],
        [ "add_milestone", "milestones", "milestone" ],
        [ "change_milestone", "milestones", "milestone" ],
        [ "delete_milestone", "milestones", "milestone" ],
        [ "view_milestone", "milestones", "milestone" ],
        [ "add_attachment", "projects", "attachment" ],
        [ "change_attachment", "projects", "attachment" ],
        [ "delete_attachment", "projects", "attachment" ],
        [ "view_attachment", "projects", "attachment" ],
        [ "add_issuestatus", "projects", "issuestatus" ],
        [ "change_issuestatus", "projects", "issuestatus" ],
        [ "delete_issuestatus", "projects", "issuestatus" ],
        [ "view_issuestatus", "projects", "issuestatus" ],
        [ "add_issuetype", "projects", "issuetype" ],
        [ "change_issuetype", "projects", "issuetype" ],
        [ "delete_issuetype", "projects", "issuetype" ],
        [ "view_issuetype", "projects", "issuetype" ],
        [ "add_membership", "projects", "membership" ],
        [ "change_membership", "projects", "membership" ],
        [ "delete_membership", "projects", "membership" ],
        [ "view_membership", "projects", "membership" ],
        [ "add_points", "projects", "points" ],
        [ "change_points", "projects", "points" ],
        [ "delete_points", "projects", "points" ],
        [ "view_points", "projects", "points" ],
        [ "add_priority", "projects", "priority" ],
        [ "change_priority", "projects", "priority" ],
        [ "delete_priority", "projects", "priority" ],
        [ "view_priority", "projects", "priority" ],
        [ "add_project", "projects", "project" ],
        [ "change_project", "projects", "project" ],
        [ "delete_project", "projects", "project" ],
        [ "view_project", "projects", "project" ],
        [ "add_severity", "projects", "severity" ],
        [ "change_severity", "projects", "severity" ],
        [ "delete_severity", "projects", "severity" ],
        [ "view_severity", "projects", "severity" ],
        [ "add_taskstatus", "projects", "taskstatus" ],
        [ "change_taskstatus", "projects", "taskstatus" ],
        [ "delete_taskstatus", "projects", "taskstatus" ],
        [ "view_taskstatus", "projects", "taskstatus" ],
        [ "add_userstorystatus", "projects", "userstorystatus" ],
        [ "change_userstorystatus", "projects", "userstorystatus" ],
        [ "delete_userstorystatus", "projects", "userstorystatus" ],
        [ "view_userstorystatus", "projects", "userstorystatus" ],
        [ "add_task", "tasks", "task" ],
        [ "change_task", "tasks", "task" ],
        [ "delete_task", "tasks", "task" ],
        [ "view_task", "tasks", "task" ],
        [ "add_role", "users", "role" ],
        [ "change_role", "users", "role" ],
        [ "delete_role", "users", "role" ],
        [ "view_role", "users", "role" ],
        [ "change_user", "users", "user" ],
        [ "view_user", "users", "user" ],
        [ "add_rolepoints", "userstories", "rolepoints" ],
        [ "change_rolepoints", "userstories", "rolepoints" ],
        [ "delete_rolepoints", "userstories", "rolepoints" ],
        [ "view_rolepoints", "userstories", "rolepoints" ],
        [ "add_userstory", "userstories", "userstory" ],
        [ "change_userstory", "userstories", "userstory" ],
        [ "delete_userstory", "userstories", "userstory" ],
        [ "view_userstory", "userstories", "userstory" ],
        [ "add_wikipage", "wiki", "wikipage" ],
        [ "change_wikipage", "wiki", "wikipage" ],
        [ "delete_wikipage", "wiki", "wikipage" ],
        [ "view_wikipage", "wiki", "wikipage" ]
    ]),
    (50, "product-ouner", "Product Owner", False, [
        [ "add_issue", "issues", "issue" ],
        [ "change_issue", "issues", "issue" ],
        [ "delete_issue", "issues", "issue" ],
        [ "view_issue", "issues", "issue" ],
        [ "add_milestone", "milestones", "milestone" ],
        [ "change_milestone", "milestones", "milestone" ],
        [ "delete_milestone", "milestones", "milestone" ],
        [ "view_milestone", "milestones", "milestone" ],
        [ "add_attachment", "projects", "attachment" ],
        [ "change_attachment", "projects", "attachment" ],
        [ "delete_attachment", "projects", "attachment" ],
        [ "view_attachment", "projects", "attachment" ],
        [ "add_issuestatus", "projects", "issuestatus" ],
        [ "change_issuestatus", "projects", "issuestatus" ],
        [ "delete_issuestatus", "projects", "issuestatus" ],
        [ "view_issuestatus", "projects", "issuestatus" ],
        [ "add_issuetype", "projects", "issuetype" ],
        [ "change_issuetype", "projects", "issuetype" ],
        [ "delete_issuetype", "projects", "issuetype" ],
        [ "view_issuetype", "projects", "issuetype" ],
        [ "add_membership", "projects", "membership" ],
        [ "change_membership", "projects", "membership" ],
        [ "delete_membership", "projects", "membership" ],
        [ "view_membership", "projects", "membership" ],
        [ "add_points", "projects", "points" ],
        [ "change_points", "projects", "points" ],
        [ "delete_points", "projects", "points" ],
        [ "view_points", "projects", "points" ],
        [ "add_priority", "projects", "priority" ],
        [ "change_priority", "projects", "priority" ],
        [ "delete_priority", "projects", "priority" ],
        [ "view_priority", "projects", "priority" ],
        [ "add_project", "projects", "project" ],
        [ "change_project", "projects", "project" ],
        [ "delete_project", "projects", "project" ],
        [ "view_project", "projects", "project" ],
        [ "add_severity", "projects", "severity" ],
        [ "change_severity", "projects", "severity" ],
        [ "delete_severity", "projects", "severity" ],
        [ "view_severity", "projects", "severity" ],
        [ "add_taskstatus", "projects", "taskstatus" ],
        [ "change_taskstatus", "projects", "taskstatus" ],
        [ "delete_taskstatus", "projects", "taskstatus" ],
        [ "view_taskstatus", "projects", "taskstatus" ],
        [ "add_userstorystatus", "projects", "userstorystatus" ],
        [ "change_userstorystatus", "projects", "userstorystatus" ],
        [ "delete_userstorystatus", "projects", "userstorystatus" ],
        [ "view_userstorystatus", "projects", "userstorystatus" ],
        [ "add_task", "tasks", "task" ],
        [ "change_task", "tasks", "task" ],
        [ "delete_task", "tasks", "task" ],
        [ "view_task", "tasks", "task" ],
        [ "add_role", "users", "role" ],
        [ "change_role", "users", "role" ],
        [ "delete_role", "users", "role" ],
        [ "view_role", "users", "role" ],
        [ "change_user", "users", "user" ],
        [ "view_user", "users", "user" ],
        [ "add_rolepoints", "userstories", "rolepoints" ],
        [ "change_rolepoints", "userstories", "rolepoints" ],
        [ "delete_rolepoints", "userstories", "rolepoints" ],
        [ "view_rolepoints", "userstories", "rolepoints" ],
        [ "add_userstory", "userstories", "userstory" ],
        [ "change_userstory", "userstories", "userstory" ],
        [ "delete_userstory", "userstories", "userstory" ],
        [ "view_userstory", "userstories", "userstory" ],
        [ "add_wikipage", "wiki", "wikipage" ],
        [ "change_wikipage", "wiki", "wikipage" ],
        [ "delete_wikipage", "wiki", "wikipage" ],
        [ "view_wikipage", "wiki", "wikipage" ]
    ]),
    (60, "stakeholder", "Stakeholder", False, [
        [ "add_issue", "issues", "issue" ],
        [ "change_issue", "issues", "issue" ],
        [ "delete_issue", "issues", "issue" ],
        [ "view_issue", "issues", "issue" ],
        [ "view_milestone", "milestones", "milestone" ],
        [ "add_attachment", "projects", "attachment" ],
        [ "change_attachment", "projects", "attachment" ],
        [ "delete_attachment", "projects", "attachment" ],
        [ "view_attachment", "projects", "attachment" ],
        [ "view_issuestatus", "projects", "issuestatus" ],
        [ "view_issuetype", "projects", "issuetype" ],
        [ "view_membership", "projects", "membership" ],
        [ "view_points", "projects", "points" ],
        [ "view_priority", "projects", "priority" ],
        [ "view_project", "projects", "project" ],
        [ "view_severity", "projects", "severity" ],
        [ "view_taskstatus", "projects", "taskstatus" ],
        [ "view_userstorystatus", "projects", "userstorystatus" ],
        [ "view_task", "tasks", "task" ],
        [ "view_role", "users", "role" ],
        [ "change_user", "users", "user" ],
        [ "view_user", "users", "user" ],
        [ "view_rolepoints", "userstories", "rolepoints" ],
        [ "view_userstory", "userstories", "userstory" ],
        [ "change_wikipage", "wiki", "wikipage" ],
        [ "view_wikipage", "wiki", "wikipage" ]
    ])
)
