from django.contrib import admin
from .models import server_packages
from .models import server_os
from .models import server_locations
from .models import servers

class ServerPackagesAdmin(admin.ModelAdmin):
    list_display = ['package_name', 'package_cpu', 'package_ram', 'package_disk', 'package_price', 'package_transfer_limit']

admin.site.register(server_packages, ServerPackagesAdmin)

class ServerOSAdmin(admin.ModelAdmin):
    list_display = ['os_name', 'os_version', 'clone_name', 'clone_id' ,'img_url']

admin.site.register(server_os, ServerOSAdmin)


class ServerLocationAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'location_city' ,'img_url']

admin.site.register(server_locations, ServerLocationAdmin)

class ServerAdmin(admin.ModelAdmin):
    list_display = ['server_name', 'server_ip_id' ,'server_location_id' , 'server_os_id', 'project_id']

admin.site.register(servers, ServerAdmin)