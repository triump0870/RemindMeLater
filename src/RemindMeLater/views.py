import logging

from django.views import generic

logger = logging.getLogger(__name__)
logger.info("Reminder App Started")

class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"
