"""
○ POST /api/servers/ - Create a new server

○ GET /api/servers/ - List all servers

○ GET /api/servers/{id}/ - Get a specific server’s details

○ PATCH /api/servers/{id}/ - Update a specific server’s status

○ POST /api/devices/ - Register a device

○ GET /api/devices/ - List devices

○ PATCH /api/devices/{id}/ - Update a device’s status

"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator

class Device(models.Model):
	name = models.TextField()
	is_online = models.BooleanField(default=True)
	last_seen = models.DateTimeField(auto_now=True)

class Server(models.Model):
	name = models.CharField(max_length = 50, validators=[MinLengthValidator(3)])
	subdomain = models.TextField(editable = False, unique=True, blank=True)
	status = models.CharField(max_length=8, choices = [(x,x) for x in ['stopped', 'starting', 'running', 'error']], default='starting')
	created_at = models.DateTimeField(auto_now_add=True)
	device = models.ForeignKey(Device, null=True, on_delete = models.SET_NULL)

	def save(self, *args, **kwargs):
		if not self.subdomain:
			duplicate_amount = len(Server.objects.filter(name = self.name))
			self.subdomain = slugify(self.name + (f"-{duplicate_amount+1}" if duplicate_amount != 0 else ''))
			super().save()
		else:
			super().save(*args, **kwargs)


			#super().save(*args, **kwargs)
			#result = Server.objects.filter(name = self.name) 
			#self.subdomain = self.name if not result.exists() else self.name+str(self.id)
			#super().save(*args, **kwargs)




