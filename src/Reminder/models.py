from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Reminder(models.Model):
	message = models.CharField(max_length=500)
	date = models.DateField(editable=True)
	time = models.TimeField(editable=True)
	created = models.DateTimeField(auto_now_add=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=True, null=True)
	email = models.EmailField(max_length=100, blank=True, null=True)
	completed = models.BooleanField(default=False)
	def __unicode__(self):
		return 'Reminder #{0}'.format(self.pk)



