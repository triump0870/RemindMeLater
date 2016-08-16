from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import url

from apis import views


urlpatterns = [
    url(r'^reminders$', views.ReminderList.as_view(), name='api-list'),
    url(r'^reminders/(?P<pk>[0-9]+)$',
        views.ReminderDetail.as_view(), name='api-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
