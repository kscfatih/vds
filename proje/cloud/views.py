from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from .models import Project 
from .models import server_packages
from .models import servers
from .models import server_os
from .models import server_locations
import requests
import json
from proxmoxer import ProxmoxAPI
import time
import paramiko
from django.views.decorators.csrf import csrf_exempt
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxmox = ProxmoxAPI('46.196.48.16', user='root@pam', password='123qweQWE', verify_ssl=False)
node = proxmox.nodes('vcenter')
proxmox.login()
@login_required(login_url="/account/login_user")
def cloud_home(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'cloud/index.html', {'projects': projects})


@login_required(login_url="/account/login_user")
def save_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        user_id = request.user.id

        # Proje modeline kaydet
        project = Project(project_name=project_name, project_description=project_description, user_id=user_id)
        project.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})





def create_server2(request):
    return render(request,'cloud/create-server.html')


def delete_server(request):
    node.qemu('101').delete()
    return HttpResponse("VM Silindi.")

def view_server_kopya(request):
    vm_config = node.qemu('101').status.current.get()
    return render(request, 'server_view.html', {'vm_config': vm_config})





def create_server(request):
    
    os = server_os.objects.all()
    location = server_locations.objects.all()
    server_package = server_packages.objects.all()
    project_id = request.session.get('project_id' , None)
    if request.method == 'POST':
        pack_id = request.POST.get('packId')
        location_id = request.POST.get('locationId')
        os_id = request.POST.get('osId')
        pack = server_packages.objects.get(id=pack_id)
        name = request.POST.get('hostname')
        ram = int(pack.package_ram)* 1024
        cpu = int(pack.package_cpu)
        disk = int(pack.package_disk)
        try:
            vmid = 101
            target_node = 'vcenter'  # Klonun yerleştirileceği hedef düğümü belirtin
            new_vmid = 1002  # Klonun yeni VM ID'sini belirtin
            server_add = servers(server_name = name , server_ip_id=1 , server_os_id = os_id, server_location_id = location_id , server_pack_id = pack_id , vm_id=new_vmid , project_id = project_id )
            server_add.save()
            
            # Klonlama işlemini gerçekleştir
            

            proxmox.nodes(target_node).qemu(vmid).clone.create(newid=new_vmid, name=name )
            # Klonlama işleminin tamamlanmasını bekle
            time.sleep(80)

            # Klonun RAM diskini güncelle
            
            
                    # SSH bağlantısı için gerekli bilgiler
            host = '46.196.48.16'
            port = 22
            username = 'root'
            password = '123qweQWE'

                # SSH bağlantısını oluşturma
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username, password)
                # RAM ayarlama
                
            ram_cmd = f"qm set {new_vmid} --memory {ram}"
            stdin, stdout, stderr = ssh.exec_command(ram_cmd)
            ram_output = stdout.read().decode()

                # Disk boyutunu değiştirme
            new_disk_size = f'{disk}G'
            resize_cmd = f"qm resize {new_vmid} scsi0 {new_disk_size}"
            stdin, stdout, stderr = ssh.exec_command(resize_cmd)
            resize_output = stdout.read().decode()

                # CPU ayarlama
                
            cpu_cmd = f"qm set {new_vmid} --cores {cpu}"
            stdin, stdout, stderr = ssh.exec_command(cpu_cmd)
            cpu_output = stdout.read().decode()

                # SSH bağlantısını kapatma
            ssh.close()

        # İşlem sonuçlarını gösterme
            response_ram = f"RAM Ayarı: {ram_output}<br> Disk Boyutu Ayarı: {resize_output}<br> CPU Ayarı: {cpu_output}"
                
            return HttpResponse(response_ram)
            
        except Exception as e:
            print("Hata:", str(e))
            return HttpResponse("Bir hata oluştu. Lütfen tekrar deneyin.")  # veya başka bir hata mesajı

    else:
        return render(request, 'cloud/create/index.html', {'server_package': server_package , 'os':os , 'location' : location , 'project_id': project_id } )




def wait(request):
    vm_config = node.qemu('1002').status.current.get()
    return render(request , 'cloud/wait.html' , {'vm_config':vm_config})



def clone_vm(request):
    try:
        # ubuntu-server'ın VM ID'sini bulun
        source_vm_id = None
        for node in proxmox.nodes.get():
            if node['node'] == 'vcenter':
                for vm in proxmox.nodes(node['node']).qemu.get():
                    if vm.get('name') == 'ubuntu-server':
                        source_vm_id = vm.get('vmid')
                        break
        # Eğer bulunduysa, klonla ve yeni VM oluştur
        if source_vm_id is not None:
            # yeni bir vmid alın, eşsiz olmalıdır
            new_vmid = str(max([int(vm['vmid']) for node in proxmox.nodes.get() for vm in proxmox.nodes(node['node']).qemu.get()]) + 1)
            node_name = 'vcenter'
            proxmox.nodes(node_name).qemu(source_vm_id).clone.post(newid=new_vmid, full='1', storage='local-lvm', target=node_name)
            # Klonlama işlemi tamamlanana kadar bekleyin
            time.sleep(80)
            # yeni VM oluşturulduktan sonra, konfigürasyonunu al ve değiştir
            config = proxmox.nodes(node_name).qemu(new_vmid).config.get()
            # RAM ve disk boyutunu ayarla
            config['memory'] = 2048  # RAM 2GB
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # SSH bağlantısı oluştur
            ssh.connect(hostname='46.196.48.16', username='root', password='123qweQWE')
            # Diski genişletme komutunu çalıştır
            stdin, stdout, stderr = ssh.exec_command('qm resize 102 scsi0 50G')
            # Çıktıyı yazdır
            print(stdout.read().decode())
            ssh.close()
            # 'meta', 'digest' ve 'vmgenid' öğelerini kaldırın çünkü Proxmox API'si bunları ayarlamayı kabul etmeyebilir
            config.pop('meta', None)
            config.pop('digest', None)
            config.pop('vmgenid', None)
            # yeni konfigürasyonu uygula
            proxmox.nodes(node_name).qemu(new_vmid).config.set(**config)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failiure'})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error': str(e)})

    






@csrf_exempt
def my_form_view(request):
    if request.method == 'POST':
        data = dict(request.POST.items())  # convert QueryDict to dictionary
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def view_server(request  , project_id):
    vm_config = node.qemu('1002').status.current.get()
    server_list = servers.objects.filter(project_id=project_id)
    request.session['project_id'] = project_id
    if request.method == "POST":
       
        return None
    
    else:
        return render(request, "cloud/view/index.html" , {'server_list': server_list , 'vm_config' :vm_config })

def deneme(request):
    project_id = request.session.get('project_id' , None)
    print(project_id)
    return render(request, "cloud/view/index.html")





        
        
        

