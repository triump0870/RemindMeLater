from django.views import generic
import logging
logger = logging.getLogger("raven")
logger.error("test")

class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"
