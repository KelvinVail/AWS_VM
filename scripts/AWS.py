import boto3
import time


KEY_NAME = 'YOUR KEY NAME'
ec2 = boto3.resource('ec2')

def list_ec2_instances_ids(status):
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name':'instance-state-name', 'Values': status }])
    for instance in instances:
        ids.append(instance.id)
    return ids

def running_instance(instance_type):
    instances = ec2.instances.filter(
        Filters=[{'Name':'instance-state-name', 'Values': ['running'] }])
    for instance in instances:
        if instance.instance_type == instance_type:
            return instance.public_dns_name

def start_instances(ids):
    ids=[]
    instances  = ec2.instances.filter(InstanceIds=ids).start()
    instances = list_ec2_instances_ids(['running'])
    while len(instances) == 0:
        instances = list_ec2_instances_ids(['running'])
        time.sleep(1)
    for instance in instances:
        ids.append(instance)
        return get_public_dns(ids)

def stop_instances(ids):
    ec2.instances.filter(InstanceIds=ids).stop()

def stop_all_instances():
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name':'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        ids.append(instance.id)
    ec2.instances.filter(InstanceIds=ids).stop()

def get_public_dns(id):
    instances = ec2.instances.filter(InstanceIds=id)
    for instance in instances:
        return instance.public_dns_name

def make_instance_available():
    running_instances = list_ec2_instances_ids(['running'])
    if len(running_instances) > 0:
        return get_public_dns(running_instances)
    
    stopped_instances = list_ec2_instances_ids(['stopped'])
    if len(stopped_instances) > 0:
        return start_instances(stopped_instances)

def create_instance(instance_type, image_id=None, volume_id=None):

    if image_id == None:
        image_id = 'ami-e5083683' #Amazon Linux

    volume = None
    if volume_id != None:
        volume = ec2.Volume(volume_id)

    new_instances = ec2.create_instances(InstanceType=instance_type,
                                         ImageId=image_id,
                                         MinCount=1,
                                         MaxCount=1,
                                         KeyName=KEY_NAME,
                                         InstanceInitiatedShutdownBehavior='terminate',
                                         SecurityGroups=['launch-wizard-5'])

    for new_instance in new_instances:
        while True:
            running_instances = list_ec2_instances_ids(['running'])
            for running in running_instances:
                if new_instance.id == running:
                    if volume != None:
                        volume.attach_to_instance(InstanceId=new_instance.id,
                                                  Device='/dev/xvdb')
                    return get_public_dns([new_instance.id])
            time.sleep(1)
