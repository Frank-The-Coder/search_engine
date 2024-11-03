import boto3
import os

def create_key_pair(keyname):
    response = boto3.client('ec2').create_key_pair(KeyName=keyname)
    with open("ece326_ec2_keypair.pem", "w") as f:
        f.write(response['KeyMaterial'])

    os.chmod('ece326_ec2_keypair.pem', 0o400)


def create_security_group(groupName, description):
    response = boto3.client('ec2').create_security_group(GroupName=groupName, Description=description)
    print(response)


def authorize_security_group():
    response = boto3.client('ec2').authorize_security_group_ingress(
        GroupId='sg-043325a9d77a8ecd1',
        IpPermissions=[
            {
                'FromPort': -1,
                'IpProtocol': 'icmp',
                'ToPort': -1,
                'IpRanges': [
                    {
                        'Description': 'Any IP',
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            },
        ],
    )
    print(response)
    response = boto3.client('ec2').authorize_security_group_ingress(
        GroupId='sg-043325a9d77a8ecd1',
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'ToPort': 22,
                'IpRanges': [
                    {
                        'Description': 'Any IP',
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            },
        ],
    )
    print(response)
    response = boto3.client('ec2').authorize_security_group_ingress(
        GroupId='sg-043325a9d77a8ecd1',
        IpPermissions=[
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'ToPort': 80,
                'IpRanges': [
                    {
                        'Description': 'Any IP',
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            },
        ],
    )
    print(response)




if __name__ == "__main__":


    authorize_security_group()

