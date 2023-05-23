from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name







class server_ips(models.Model):
    name = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    subnet = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    def __repr__(self):
        return str(self.ip)



class server_packages(models.Model):
    package_name = models.CharField(max_length=255)
    package_cpu = models.CharField(max_length=255)
    package_ram = models.CharField(max_length=255)
    package_disk = models.CharField(max_length=255)
    package_price = models.CharField(max_length=255)
    package_transfer_limit = models.CharField(max_length=255)
    def __str__(self):
        return self.package_name
    
    class Meta:
        verbose_name_plural = "server_packages"

class server_os(models.Model):
    os_name = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    clone_name = models.CharField(max_length=255)
    clone_id = models.CharField(max_length=255)
    img_url = models.ImageField(upload_to='static/images/os' , null=True)
    def __str__(self):
        return self.os_name    
    class Meta:
        verbose_name_plural = "server_os"


class server_locations(models.Model):
    location_name = models.CharField(max_length=255)
    location_city = models.CharField(max_length=255)
    img_url = models.ImageField(upload_to='static/images/locations' , null=True)
    def __str__(self):
        return self.location_name   
    class Meta:
        verbose_name_plural = "server_locations"



class servers(models.Model):
    vm_id = models.CharField(max_length=255 , null=True)
    server_name = models.CharField(max_length=255)
    server_pack = models.ForeignKey(server_packages, on_delete=models.CASCADE, null=True)
    server_ip = models.ForeignKey(server_ips, on_delete=models.CASCADE)
    server_os = models.ForeignKey(server_os, on_delete=models.CASCADE)
    server_location = models.ForeignKey(server_locations, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.server_name
    class Meta:
        verbose_name_plural = "servers"
