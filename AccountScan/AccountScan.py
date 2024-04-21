import boto3

# check active resources
def check_resources():
    ec2 = boto3.client('ec2')
    eks = boto3.client('eks')
    ec2_resources = ec2.describe_instances()
    eks_clusters = eks.list_clusters()

    ec2_active = len(ec2_resources['Reservations']) > 0
    eks_active = len(eks_clusters['clusters']) > 0

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