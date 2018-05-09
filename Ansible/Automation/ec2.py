import boto
import time
import traceback
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne',endpoint='nova.rc.nectar.org.au')
ACCESS_KEY='43f6141543c348fa9d9e99bb1340f847'
SERECT_KEY='b073fd9b7710451ab34766409754179d'

print('establish connection...')

try:
    ec2_conn = boto.connect_ec2(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SERECT_KEY,
                            is_secure=True,
                            region=region,
                            port=8773,
                            path='/services/Cloud',
                            validate_certs=False)
except Exception as e:
    print("Exception: "+str(e))


print("creating 4 instances")

WebinstanceNum=1
ec2_conn.run_instances('ami-00003837', max_count=WebinstanceNum, key_name='cloud', instance_type='m1.large', placement='melbourne-qh2', security_groups=['default'])
DBinstanceNum=3
ec2_conn.run_instances('ami-00003837', max_count=DBinstanceNum, key_name='cloud', instance_type='m1.small', placement='melbourne-qh2', security_groups=['default'])
for i in range(4):
    vol_req=ec2_conn.create_volume(30,'melbourne-qh2')

print("finished")

instances = ec2_conn.get_only_instances()
vols = ec2_conn.get_all_volumes();
print('checking instance status')

for i in instances:
    while i.update()!="running":
        time.sleep(5)
print("all nodes have been created successfully!")

#list instances details

print("list instance details")
IPs =[]
for i in instances:
    print(i.private_ip_address)
    IPs.append(i.private_ip_address)

#attach volume
print('attaching volume to instance')
for ins, vol in zip([i for i in instances],[vol for vol in vols] ):
    ec2_conn.attach_volume(vol.id,ins.id,"/dev/vdc")
print('attach finished')


#write IP for ansible
filePath1 = '/Users/panyiru/Desktop/Ansible/Automation/host'
filePath2 = '/Users/panyiru/Desktop/Ansible/Automation/roles/db1replica/vars/main.yaml'
filePath3 = '/Users/panyiru/Desktop/Ansible/Automation/roles/db2replica/vars/main.yaml'
filePath4 = '/Users/panyiru/Desktop/Ansible/Automation/roles/db3replica/vars/main.yaml'
with open(filePath1, 'w') as f:
      content="[webserver]\n"+IPs[0]+"\n"+"[dbserver1]\n"+IPs[1]+"\n"+"[dbserver2]\n"+IPs[2]+"\n"+"[dbserver3]\n"+IPs[3]+"\n"+"\n"+"[all:vars]\n"+"ansible_ssh_user=ubuntu\n"+"ansible_ssh_private_key_file=/Users/panyiru/.ssh/cloud.key\n"
      f.write(content)
#dbserver1
with open(filePath2, 'w') as f:
    content="replica1: "+ IPs[2]+"\n"+"replica2: "+IPs[3]+"\n"+"hostname: "+IPs[1]
    f.write(content)
#dbserver2
with open(filePath3,'w') as f:
    content="replica1: "+IPs[1]+"\n"+"replica2: "+IPs[3]+"\n"+"hostname: "+IPs[2]
    f.write(content)
#dbserver3
with open(filePath4,'w') as f:
    content="replica1: "+IPs[1]+"\n"+"replica2: "+IPs[2]+"\n"+"hostname: "+IPs[3]
    f.write(content)

print("write file finished")
