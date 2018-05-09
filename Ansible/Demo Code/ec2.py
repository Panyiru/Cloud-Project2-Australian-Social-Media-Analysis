import boto
import time
import traceback
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne',endpoint='nova.rc.nectar.org.au')
ACCESS_KEY='8995abcdf7bb4058980ef6789104699a'
SERECT_KEY='78b0c09bca8a4d55aa6725042f62029f'

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


print("creating 2 instances")

instanceNum=2
ec2_conn.run_instances('ami-00003837', max_count=instanceNum, key_name='cloud', instance_type='m1.small', placement='melbourne-qh2', security_groups=['default'])
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
    ec2_conn.attach_volume(vol.id,ins.id,"/dev/vdb")
print('attach finished')


#write IP for ansible
filePath1 = '/Users/panyiru/Desktop/Ansible/Demo Code/host'
filePath2 = '/Users/panyiru/Desktop/Ansible/Demo Code/roles/install-replica1/vars/main.yaml'
filePath3 = '/Users/panyiru/Desktop/Ansible/Demo Code/roles/install-replica2/vars/main.yaml'
with open(filePath1, 'w') as f:
      content="[webserver]\n"+IPs[0]+"\n"+"[dbserver]\n"+IPs[1]+"\n"+"\n"+"[all:vars]\n"+"ansible_ssh_user=ubuntu\n"+"ansible_ssh_private_key_file=/Users/panyiru/.ssh/cloud.key\n"
      f.write(content)

with open(filePath2, 'w') as f:
    content="replica: "+ IPs[1]+"\n"+"hostname: "+IPs[0]
    f.write(content)

with open(filePath3,'w') as f:
    content="replica: "+IPs[0]+"\n"+"hostname: "+IPs[1]
    f.write(content)

print("write file finished")
