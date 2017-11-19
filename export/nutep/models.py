# -*- coding: utf-8 -*-
import datetime
import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_text, force_unicode
from django.utils.formats import date_format
from uuslug import slugify


def base_path(root, filename):    
    from django.conf import settings
    os.umask(0)
    path = u'%s/%s_%s' % (root, datetime.date.today().month, datetime.date.today().year,)
    att_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(att_path):
        os.makedirs(att_path, 0777)    
    return os.path.join(path, slugify(filename, separator="."))


def attachment_path(instance, filename):   
    return base_path('attachments', filename)


def userprofile_path(instance, filename):    
    root = u'profile/%s' % (instance.user,)    
    return base_path(root, filename)


class File(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(blank=True, null=True, max_length=255)    
    file = models.FileField(upload_to=attachment_path, blank=True, null=True,)
    note = models.CharField(blank=True, null=True, max_length=255)
        
    def __unicode__(self):
        return force_unicode(self.title) 


class Team(models.Model):
    name = models.CharField('Наименование', max_length=150, db_index=True)
    users = models.ManyToManyField(User, blank=True, related_name="teams")
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Рабочая группа')
        verbose_name_plural = force_unicode('Рабочие группы')
        ordering = ('name', )        


class BaseModelManager(models.Manager):    
    def get_queryset(self):        
        return super(BaseModelManager, self).get_queryset().filter(deleted=False)


class PrivateModelManager(BaseModelManager):    
    def for_user(self, user):
        if not user:
            return super(PrivateModelManager, self).get_queryset().none()
        return super(PrivateModelManager, self).get_queryset().filter(models.Q(teams__users=user) | models.Q(owner=user)).distinct()


class ProcessDeletedModel(models.Model):    
    _last_event = None
    _first_event = None
    objects = BaseModelManager()
    all_objects = models.Manager()
    deleted = models.BooleanField('Пометка удаления', default=False)    
           
    def last_event(self):
        if not self._last_event:
            if self.history:
                self._last_event = self.history.all().order_by("-date").first()
        return self._last_event
    
    def first_event(self):
        if not self._first_event:
            if self.history:
                self._first_event = self.history.all().order_by("date")[:1].first()
        return self._first_event
    
    class Meta:
        abstract = True 


class PrivateModel(ProcessDeletedModel):
    teams = models.ManyToManyField(Team, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    objects = PrivateModelManager()    
    class Meta:
        abstract = True


class BaseModel(ProcessDeletedModel):
    name = models.CharField('Наименование', max_length=150, db_index=True)
    guid = models.CharField(max_length=50, null=True, db_index=True, unique=True)
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        ordering = ('name', )
        abstract = True
        

class HistoryMeta(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')    
    is_created = models.BooleanField(default=False)    
    date = models.DateTimeField(blank=True, null=True, db_index=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)         
    def __unicode__(self):
        return u'{0}'.format(self.user) 
    

class BaseError(models.Model):
    XML = 1
    MODEL = 2
    UNKNOWN = 3 
    WEBFAULT = 4   
    
    TYPE_CHOICES = (
        (XML, force_unicode('Ошибка учетной системы')),
        (WEBFAULT, force_unicode('Ошибка обмена данных')),
        (MODEL, force_unicode('Ошибка данных')),
        (UNKNOWN, force_unicode('Ошибка')),
             
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')   
    date = models.DateTimeField(auto_now_add=True, blank=True)
    code = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    field = models.CharField(max_length=50, db_index=True, blank=True, null=True)            
    message = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=UNKNOWN, db_index=True, blank=True)
    
    def __unicode__(self):
        return u'{0}'.format(self.code) 
    class Meta:
        verbose_name = force_unicode('Ошибка')
        verbose_name_plural = force_unicode('Ошибки')
        ordering = ('id', )
    

class Vessel(BaseModel):
    history = GenericRelation('HistoryMeta')    

    class Meta:        
        verbose_name = force_unicode('Судно')
        verbose_name_plural = force_unicode('Суда')        
    
class Voyage(BaseModel):        
    vessel = models.ForeignKey(Vessel, null=True, related_name="voyages")
    flag = models.CharField(max_length=100, null=True, blank=True) 
    eta = models.DateTimeField(null=True, blank=True)
    history = GenericRelation('HistoryMeta')    
      
    class Meta:
        verbose_name = force_unicode('Рейс')
        verbose_name_plural = force_unicode('Рейсы')
        unique_together = ('vessel', 'name')    

    def as_dict(self):
        return {
            "id": self.id,           
            "vessel": force_text(self.vessel),
            "voyage": force_text(self.name),
            "eta": date_format(timezone.localtime(self.eta), "d.m.Y"),            
        }        


class ServiceProvided(models.Model):
    PORUCHENIE = '00001'    
    OTHERDOCS = '00002'
    SERVICES = (
        (PORUCHENIE, force_unicode('Экспортные поручения')),
        (OTHERDOCS, force_unicode('Прочие документы')),
    )
    service = models.CharField(choices=SERVICES, max_length=5, db_index=True, unique=True)
    def __unicode__(self):
        return u'{0}'.format(self.get_service_display()) 
    class Meta:
        verbose_name = force_unicode('Услуга')
        verbose_name_plural = force_unicode('Услуги')
    
    
class Line(PrivateModel): 
    name = models.CharField('Наименование', max_length=150, db_index=True)
    guid = models.CharField(max_length=50, null=True, db_index=True)
    services = models.ManyToManyField(ServiceProvided, blank=True)       
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Линия')
        verbose_name_plural = force_unicode('Линии')
        ordering = ('name', )
        
        
class Terminal(BaseModel):       
    class Meta:
        verbose_name = force_unicode('Терминал')
        verbose_name_plural = force_unicode('Терминалы')

                   
class Contract(PrivateModel):
    name = models.CharField('Наименование', max_length=150, db_index=True)
    guid = models.CharField(max_length=50, null=True, db_index=True)    
    line = models.ForeignKey(Line, related_name="contracts")
    terminal = models.ForeignKey(Terminal)
    startdate = models.DateTimeField(db_index=True)
    expired = models.DateTimeField(db_index=True)    
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Договор')
        verbose_name_plural = force_unicode('Договоры')
        ordering = ('name', )


class UserProfile(models.Model):
    guid = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, unique=True, related_name='profile')
    lines = models.ManyToManyField(Line, blank=True)
    image = models.ImageField(upload_to=userprofile_path, blank=True, null=True,)
    def fullname(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)    
    def __unicode__(self):
        return u'{0}'.format(self.user) 
    

class Draft(models.Model):
    name = models.CharField('BL', max_length=150, db_index=True)        
    guid = models.CharField(max_length=50)        
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)    
    date = models.DateTimeField()
    shipper = models.CharField(max_length=255, null=True, blank=True)
    consignee = models.CharField(max_length=255, null=True, blank=True)    
    voyage = models.ForeignKey(Voyage, related_name="drafts", null=True)
    finalDestination = models.CharField(max_length=255, null=True, blank=True)
    POD = models.CharField(max_length=150, null=True, blank=True)
    POL = models.CharField(max_length=150, null=True, blank=True)
    finstatus = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    poruchenie = models.BooleanField(default=False)
    poruchenieNums = models.CharField(max_length=150, null=True, blank=True)
    notify = models.CharField(max_length=255, null=True, blank=True)
    line = models.ForeignKey(Line)
    order = models.ForeignKey("Order", related_name='drafts', blank=True, null=True)
    
    def __unicode__(self):
        return u'{0}'.format(self.name)
    
    def active_template(self):
        return self.order.active_template()

    def contract(self):
        return self.order.contract
     
    class Meta:
        verbose_name = force_unicode('Коносамент')
        verbose_name_plural = force_unicode('Коносаменты')
        ordering = ('name', )  


class Mission(models.Model):
    name = models.CharField(max_length=12, db_index=True)
    guid = models.CharField(max_length=50)        
    draft = models.ForeignKey(Draft, related_name="missions", on_delete=models.CASCADE)
    files = GenericRelation(File)
    reception_date = models.DateTimeField(blank=True, null=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    
        
    def __unicode__(self):
        return u'{0}'.format(self.name)
    
    def pdf_files(self):
        return self.files.filter(title__iendswith='pdf')
    
    def xlsx_files(self):
        return self.files.filter(title__iendswith='xlsx')
    
    class Meta:
        verbose_name = force_unicode('Поручение')
        verbose_name_plural = force_unicode('Поручения')
        ordering = ('name', )  

            
class Container(models.Model):
    name = models.CharField(max_length=12, db_index=True)
    SOC = models.BooleanField(default=False)
    size = models.CharField(max_length=2, db_index=True)
    type = models.CharField(max_length=4, db_index=True)
    line = models.ForeignKey(Line, null=True, blank=True)
    seal = models.CharField(max_length=150, null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    netto = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    gross = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    tare = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    package = models.CharField(max_length=150, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    draft = models.ForeignKey(Draft, related_name="containers", on_delete=models.CASCADE)
    def __unicode__(self):
        return u'{0}'.format(self.name) 
    class Meta:
        verbose_name = force_unicode('Контейнер')
        verbose_name_plural = force_unicode('Контейнеры')
        ordering = ('name', ) 
                              

class Readiness(models.Model):
    size = models.CharField(max_length=2, db_index=True)
    type = models.CharField(max_length=4, db_index=True)
    ordered = models.PositiveIntegerField(null=True, blank=True)
    done = models.PositiveIntegerField(null=True, blank=True)
    draft = models.ForeignKey(Draft, related_name="readiness", on_delete=models.CASCADE)
    def __unicode__(self):
        return u'{0}'.format(self.id) 
    class Meta:
        verbose_name = force_unicode('Готовность')
        verbose_name_plural = force_unicode('Готовность')
        ordering = ('id', ) 


class Order(PrivateModel):
    voyage = models.ForeignKey(Voyage, blank=True, null=True, on_delete=models.PROTECT,
                               related_name="orders")
    contract = models.ForeignKey(Contract, blank=True, null=True, on_delete=models.PROTECT)
    history = GenericRelation('HistoryMeta')
    
    files = GenericRelation(File)    

    def __unicode__(self):
        return u'%s %s' % (self.voyage, self.contract) 
    
    class Meta:
        unique_together = ('voyage', 'contract')
        verbose_name = force_unicode('Заявка')
        verbose_name_plural = force_unicode('Заявки')
    
    def active_template(self):
        return self.templates.first()

    def as_dict(self):        
        return {
            "id": self.id,
            "line": self.contract.line.name,
            "contract": self.contract.name,           
            "vessel": force_text(self.voyage.vessel),
            "voyage": force_text(self.voyage),
            "eta": date_format(timezone.localtime(self.voyage.eta), "d.m.Y") if self.voyage.eta else '',  
            "url": reverse('drafts', kwargs={'order': self.pk}),                                
        } 


    def drafts_done(self):        
        return self.drafts.filter(poruchenie=True)    
        
    def drafts_total(self):        
        return self.drafts.all()
        
    def drafts_readiness(self):        
        total = float(len(self.drafts_total()))
        if not total:
            return 0
        done = float(len(self.drafts_done()))        
        return int(done / total * 100) 
    

class UploadedTemplateManager(PrivateModelManager):    
    def for_user(self, user):        
        return super(UploadedTemplateManager, self).for_user(user).defer("xml_response")
    

class UploadedTemplate(PrivateModel):
    NEW = 1
    INPROCESS = 2
    PROCESSED = 3
    REFRESH = 4
    ERROR = 500
    
    STATUS_CHOICES = (
        (NEW, force_unicode('Новый')),
        (INPROCESS, force_unicode('Успешно загружен')),
        (PROCESSED, force_unicode('Обработан')),
        (ERROR, force_unicode('Ошибка')),     
        (REFRESH, force_unicode('Обновление данных')),
    )
    
    objects = UploadedTemplateManager()    
    attachment = models.FileField('Файл шаблона', upload_to=attachment_path) 
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW, db_index=True, blank=True)
    http_code = models.CharField('HTTP Код', max_length=50, null=True, blank=True)
    xml_response = models.TextField('XML ответ', null=True, blank=True)        
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, related_name="templates")
    history = GenericRelation('HistoryMeta')    
    errors = GenericRelation('BaseError')
    md5_hash = models.CharField('md5 hash', max_length=32, null=True, blank=True, db_index=True)
    is_override = models.BooleanField(default=False)
    services = models.ManyToManyField(ServiceProvided, blank=True)
    
    def set_status(self):        
        if len(self.errors.all()): # pylint: disable=E1101
            self.status = UploadedTemplate.ERROR        
        else:
            self.status = UploadedTemplate.INPROCESS
        self.save()
    
    def __unicode__(self):
        return u'{0}'.format(self.attachment.name)  

    def filename(self):
        return os.path.basename(self.attachment.name)
    
    def status_class(self):
        mapper = {
            self.NEW: 'new',
            self.PROCESSED: 'success',
            self.INPROCESS: 'info',
            self.ERROR: 'danger',
            self.REFRESH: 'refresh',
        }
        return mapper.get(self.status)
    
    @property
    def voyage(self):
        return self.order.voyage
    
    @property
    def vessel(self):
        return self.order.voyage.vessel
    
    @property
    def contract(self):
        return self.order.contract
    
    @property
    def line(self):
        return self.order.contract.line

    def as_dict(self):
        return {
            "id": self.id,            
            "status": self.get_status_display(),
            "vessel": force_text(self.vessel),
            "voyage": force_text(self.voyage),
            "eta": date_format(timezone.localtime(self.voyage.eta), "d.m.Y") if self.voyage.eta else "",
            "contract": force_text(self.contract),
            "line": force_text(self.line),
            "filename": force_text(self.filename()),
            "updated":  date_format(timezone.localtime(self.last_event().date), "d.m.Y H:i") if self.last_event() else "",
            "user": force_text(self.last_event().user),
            "url": reverse('template-details', kwargs={'pk': self.pk}),
            "status_class": self.status_class(),
            "status_id": "%s-status" % self.id,
            "refreshing": self.status == self.REFRESH,            
            "orderid": self.order.id,
            "drafts_url": reverse('drafts', kwargs={'order': self.order.pk}),
        }

    class Meta:
        verbose_name = force_unicode('Шаблон')
        verbose_name_plural = force_unicode('Шаблоны')
        ordering = ('-id', )
