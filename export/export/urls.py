from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from nutep import views as nutep_views
from terminal_export import views as terminal_export_views
from tracking import views as tracking_views


admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'export.views.home', name='home'),
    # url(r'^export/', include('export.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [ 
    url(r'^$', nutep_views.landing, name='landing'),     
    url(r'^dashboard/$', nutep_views.DashboardView.as_view(), name='dashboard'),    
    url(r'^tracking/$', tracking_views.TrackingView.as_view(), name='tracking'),
    url(r'^revise/$', nutep_views.ReviseView.as_view(), name='revise'),
    url(r'^terminalexport/$', terminal_export_views.TerminalExportView.as_view(), name='terminalexport'),
]

urlpatterns += [
    url(r'^select2/', include('django_select2.urls')),
]

urlpatterns += [
    url(r'^django-rq/', include('django_rq.urls')),
]

urlpatterns += [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

router = routers.DefaultRouter()
router.register(r'users', nutep_views.UserViewSet)
router.register(r'events', nutep_views.EventViewSet, 'events')
router.register(r'reviseevents', nutep_views.ReviseViewSet, 'reviseevents')
router.register(r'employees', nutep_views.EmployeesViewSet, 'employees')
router.register(r'dealstats', nutep_views.DealStats, 'dealstats')
router.register(r'jobstatus', nutep_views.JobStatus, 'jobstatus')
router.register(r'news', nutep_views.NewsViewSet, 'news')
router.register(r'pingrevise', nutep_views.PingRevise, 'pingrevise')
router.register(r'trackevents', tracking_views.TrackingViewSet, 'trackevents')
router.register(r'pingtracking', tracking_views.PingTracking, 'pingtracking')
router.register(r'pingterminalexport', terminal_export_views.PingTerminalExport, 'pingterminalexport')
router.register(r'terminalexportevents', terminal_export_views.TerminalExportViewSet, 'terminalexportevents')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns 
