from django.conf.urls import url
from .views import reminder_list,reminder_detail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^reminders$',reminder_list),
	url(r'^reminders/(?P<pk>[0-9]+)$', reminder_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
