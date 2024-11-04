import boto3
import argparse
import sys

def create_instance(keyname = 'ece326_ec2_keypair', security_group_id = 'sg-043325a9d77a8ecd1'):
    
    response = boto3.resource('ec2', region_name='us-east-1').create_instances(
        ImageId='ami-005fc0f236362e99f', #ubuntu LS22.04 release
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        KeyName= keyname, # replace with your key name
        SecurityGroupIds=[security_group_id] # replace with your security group id
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


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Manage AWS instances.")

    # Define arguments
    parser.add_argument("--debug", action="store_true", help="debug flag.")

    parser.add_argument("--create-instance", action="store_true", help="Flag to create an instance.")
    parser.add_argument("--keyname", type=str, help="Key name for the instance.")
    parser.add_argument("--security-group-id", type=str, help="Security group ID for the instance.")
    
    parser.add_argument("--associate-address", action="store_true", help="Flag to associate an address.")
    parser.add_argument("--instance-id", type=str, help="Instance ID for associating address.")
    
    parser.add_argument("--terminate-all-instance", action="store_true", help="Terminate all instances.")

    # Parse arguments
    args = parser.parse_args(argv)

    if args.debug:
        return

    # Check for conditions between arguments
    if args.create_instance:
        if not args.keyname or not args.security_group_id:
            parser.error("--create-instance requires --keyname and --security-group-id.")

    if args.associate_address:
        if not args.instance_id:
            parser.error("--associate-address requires --instance-id.")

    # Return the parsed arguments
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if not args:
        print("Something is very wrong, exiting here")
        sys.exit(1)
    
    if len(sys.argv) == 1:
        print("Run launch_ec2.py -h for more help")
        sys.exit(0)

    if args.create_instance:
        if args.debug:
            create_instance()
        else:
            create_instance(keyname=args.keyname, security_group_id=args.security_group_id)
        sys.exit(0)
    if args.associate_address:
        if args.debug:
            associate_address()
        else:
            associate_address(args.instance_id)
        sys.exit(0)
    if args.terminate_all_instance:
        terminate_all_instance()


