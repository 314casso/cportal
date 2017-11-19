from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now

from nutep.middleware import get_current_user
from nutep.models import HistoryMeta, Line, UploadedTemplate, Vessel, Voyage, Order


def prepare_history(sender, instance, created, **kwargs): 
    if not hasattr(instance, 'user'):
        instance.user = get_current_user()   
    HistoryMeta.objects.create(date=now(), content_object=instance,
                               is_created=created, user=instance.user)
    

def private_data(sender, instance, *args, **kwargs):  
    if not instance.owner:
        first_event = instance.first_event()
        if first_event:
            instance.owner = first_event.user
        else:
            instance.owner = get_current_user()


def update_teams(sender, instance, created, **kwargs):
    if created:
        for team in instance.contract.teams.all():             
            instance.teams.add(team)


def connect_signals():
    pre_save.connect(private_data, sender=UploadedTemplate)
    post_save.connect(update_teams, sender=UploadedTemplate)
    post_save.connect(update_teams, sender=Order)
    post_save.connect(prepare_history, sender=UploadedTemplate)            
    post_save.connect(prepare_history, sender=Voyage)
    post_save.connect(prepare_history, sender=Vessel)
    post_save.connect(prepare_history, sender=Line)
