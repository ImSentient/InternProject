from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import Server, Device
from .serializers import ServerSerializer, DeviceSerializer
from random import randint

class ServerCreateView(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def perform_create(self, serializer):
        server = serializer.save()
        
        if server.status in ['error', 'running']:
            server.delete()
            raise ValidationError(f"Invalid status set! Cannot create server with status = {server.status}")
        
        if server.status == "starting":
            devices = Device.objects.filter(is_online=True)
            if len(devices) == 0:
                server.status = "error"
            else:
                server.device = devices[randint(0, len(devices)-1)]
                server.status = "running"
                server.device.save()

            
        server.save(update_fields = ['device', 'status'])



class ServerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def perform_update(self, serializer):
        print(serializer.validated_data)
        server = self.get_object().status #Server.objects.get(pk=serializer.validated_data.get("id")).status
        new_server = serializer.validated_data.get("status")

        if [server, new_server] not in [['stopped', 'starting'],
                                        ['starting', 'running'],
                                        ['starting', 'error'],
                                        ['running', 'stopped'],
                                        ['error', 'starting']]:
            raise ValidationError(f"Invalid transition! {server} -> {new_server} for server {self.get_object().subdomain}")
        else:

            if new_server == 'starting':
                devices = Device.objects.filter(is_online=True)
                if len(devices) == 0:
                    #serializer.validated_data['status'] = "error"
                    serializer.save(status="error")
                else:
                    #serializer.validated_data['device'] = devices[randint(0, len(devices)-1)]
                    #serializer.validated_data['status'] = "running"
                    #serializer.validated_data['device'].save()
                    dev = devices[randint(0, len(devices)-1)]
                    dev.save()
                    serializer.save(device = dev, status='running')

class DeviceCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer