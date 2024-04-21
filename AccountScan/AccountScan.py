import boto3

# running instances check
def check_ec2_running():
    ec2 = boto3.client('ec2')
    ec2_instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    return len(ec2_instances['Reservations']) > 0

# check resources active
def check_resources():
    ec2_active = check_ec2_running()
    
    eks = boto3.client('eks')
    eks_clusters = eks.list_clusters()
    eks_active = len(eks_clusters['clusters']) > 0

    ec2 = boto3.client('ec2')
    ec2_gateways = ec2.describe_nat_gateways()
    nat_gateway_active = len(ec2_gateways['NatGateways']) > 0

    return ec2_active, eks_active, nat_gateway_active

# principal
def lambda_handler(event, context):
    ec2_active, eks_active, nat_gateway_active = check_resources()
    
    sns = boto3.client('sns')
    topic_arn = 'ARN_TOPICO_SNS'

    aws_account_id = context.invoked_function_arn.split(":")[4]

    if ec2_active or eks_active or nat_gateway_active:
        message = f"Active resources:\nEC2: {ec2_active}\nEKS: {eks_active}\nNatGateway: {nat_gateway_active}"
        subject = f"Account: [{aws_account_id}] | Active AWS resources found"
        
        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
