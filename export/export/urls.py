from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from nutep.views import (DraftDetailView, DraftListView, ServiceView,
                         TemplateDeleteView, TemplateDetailView,
                         get_active_templates, get_template_status, landing,
                         upload_file, get_last_orders, get_loading_list,
    get_mission_xlsx)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'export.views.home', name='home'),
    # url(r'^export/', include('export.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('', 
    url(r'^$', landing, name='landing'),
    url(r'^services/$', ServiceView.as_view(), name='services'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^deletetemplate/(?P<pk>[0-9]+)$', TemplateDeleteView.as_view(), name='delete-template'),  
    url(r'^gettemplate/(?P<pk>[0-9]+)$', get_template_status, name='get-template'),
    url(r'^templatedetails/(?P<pk>[0-9]+)$', TemplateDetailView.as_view(), name='template-details'),
    url(r'^drafts/(?P<order>[0-9]+)$', DraftListView.as_view(), name='drafts'),
    url(r'^draftdetails/(?P<pk>[0-9]+)$', DraftDetailView.as_view(), name='draft-details'),
)

urlpatterns += patterns('',
    url(r'^select2/', include('django_select2.urls')),
)

urlpatterns += patterns('',
    url(r'^django-rq/', include('django_rq.urls')),
)

urlpatterns += patterns('',
    url(r'^activetemplates/', get_active_templates, name="active-templates"),
    url(r'^getlastorders/', get_last_orders, name="get-last-orders"),
    url(r'^getloadinglist/(?P<pk>[0-9]+)$', get_loading_list, name="get-loading-list"),
    url(r'^getmissionxlsx/(?P<pk>[0-9]+)$', get_mission_xlsx, name="get-mission-xlsx"),
    
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
    
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns 
