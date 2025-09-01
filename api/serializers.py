from rest_framework import serializers
from .models import *

class DeviceSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Device
		fields = ['id', 'name', 'is_online', 'last_seen']


class ServerSerializer(serializers.ModelSerializer):
	
	device = DeviceSerializer(read_only = True)
	
	class Meta:
		model = Server
		fields = ['id', 'name', 'subdomain', 'status', 'created_at', 'device']

