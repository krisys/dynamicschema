from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'CreateRecord/(?P<id>.*)/$', 'cck.views.create_record'),
    (r'ListSchemas/$', 'cck.views.list_schemas'),
    (r'ConfigureSchema/(?P<id>.*)/$', 'cck.views.configure_schema'),
    (r'ListRecords/(?P<id>.*)/$', 'cck.views.list_records'),
    (r'ViewRecord/(?P<id>.*)/$', 'cck.views.view_record'),
    (r'EditRecord/(?P<id>.*)/$', 'cck.views.edit_record'),
)
