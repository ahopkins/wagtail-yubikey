from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Yubikey(models.Model):
	public_id = models.CharField(max_length=12, unique=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="yubikey")

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)