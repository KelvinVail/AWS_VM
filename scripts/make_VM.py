import AWS


#image_id = 'ami-e5083683' #Amazon Linux
image_id = 'ami-405f7226' #Ubuntu Server 16.04
#image_id = 'ami-ee8dbb88' #Microsoft Windows Server 2016 Base

#volume_id = 'YOUR VOLUME ID'

instance_type = 't2.micro'

running_dns = AWS.running_instance(instance_type)

if running_dns != None:
    print(running_dns)
else:
    #print(AWS.create_instance('t2.micro', image_id, volume_id))
    print(AWS.create_instance(instance_type, image_id))
