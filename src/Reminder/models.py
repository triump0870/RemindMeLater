from django.db import models

# Create your models here.
class Reminder(models.Model):
	task_id = models.CharField(max_length=30, blank=True, editable=False)
	message = models.CharField(max_length=500)
	time = models.DateTimeField(editable=True)
	created = models.DateTimeField(auto_now_add=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def __unicode__(self):
    	return 'Reminder #{0} - {1}'.format(self.pk, self.task_id)

    	

