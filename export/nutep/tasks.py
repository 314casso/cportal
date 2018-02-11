from django_rq import job


@job('default')
def update_user(user):
    print "*" * 100
    print user