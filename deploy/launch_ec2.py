import boto3

def create_instance():
    
    response = boto3.resource('ec2', region_name='us-east-1').create_instances(
        ImageId='ami-005fc0f236362e99f',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='ece326_ec2_keypair',
        SecurityGroupIds=['sg-043325a9d77a8ecd1']
    )
    print(response)
    id = response[0].id
    print(id)


def associate_address(instance_id='xxxxxxxxx'): #enter your instance id
    ec2_client=boto3.client('ec2', region_name="us-east-1")
    

    # step 1 - check if the instance is running
    instance_response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_state = instance_response['Reservations'][0]['Instances'][0]['State']['Name']

    if instance_state != 'running':
        print(f"Instance {instance_id} is not running (current state: {instance_state}). Exiting early.")
        return
    else:
        print(f"Instance {instance_id} is running")
    
    response = ec2_client.describe_addresses()
    print(response)

    # step 2 - associate the address
    # check if there is any elastic ip available
    # currently the elastic ip is created through aws console, can add a function to allocate if it doesn't exit
    # associate the address
    for address in response['Addresses']:
        associated_instance_id = address.get('InstanceId')
        allocation_id = address.get('AllocationId')
        
        if not associated_instance_id:
            try:
                associate_response = ec2_client.associate_address(
                    AllocationId=allocation_id,
                    InstanceId=instance_id,
                )
                print(associate_response)
            except Exception as e:
                print(f"Error {e}")


def terminate_all_instance():
    try:
        ec2_client = boto3.client('ec2', region_name='us-east-1')
        ec2_resource = boto3.resource('ec2')

        response=ec2_client.describe_instances()
        # Extract instance IDs
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])

        for id in instance_ids:
            instance = ec2_resource.Instance(id)
            instance.terminate()
    except any as e:
        print(e)


if __name__ == "__main__":
    pass
