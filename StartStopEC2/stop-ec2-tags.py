import boto3

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    
    filters = [{
        'Name': 'tag:Scheduled',
        'Values': ['yes']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)   

    RunningInstances = [instance.id for instance in instances]
    
    print(RunningInstances)

    if len(RunningInstances) > 0:
        
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print("Stopping")
    else:
        print("All Stopped")