from django.conf.urls import url
from .views import CreateReminderView, ReminderDetailView

urlpatterns = [
	url(r'^reminder/$',CreateReminderView.as_view(),name='reminder'),
	url(r'^reminder/(?P<pk>[0-9]+)/$', ReminderDetailView.as_view(), name='reminder-detail'),
]