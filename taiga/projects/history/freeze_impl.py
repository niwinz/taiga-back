
# TODO: add attachments
# TODO: points

def userstory_freezer(us):
    return {
        "owner": us.owner_id,
        "status": us.status_id,
        "is_closed": us.is_closed,
        "finish_date": us.finish_date,
        "subject": us.subject,
        "description": us.description,
        "assigned_to": us.assigned_to_id,
        "client_requirement": us.client_requirement,
        "team_requirement": us.team_requirement,
        "watchers": [x.id for x in us.watchers.all()],
        "tags": us.tags,
        "from_issue": us.generated_from_issue_id,
    }
