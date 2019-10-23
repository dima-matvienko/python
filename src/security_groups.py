import json
import boto3

client = boto3.client('ec2')
all_security_groups = client.describe_security_groups()
pretty_print = json.dumps(all_security_groups, indent=4)

print(pretty_print)

print('\x1b[6;30;42m' + '\n\n\n\nThis is a short output containing only group names and descriptions\n\n\n\n\n' + '\x1b[0m')

security_groups_short = {}

for security_group in all_security_groups['SecurityGroups']:
   security_groups_short[security_group['GroupName']] = security_group['Description']

for groupname, description in security_groups_short.items():
    print(groupname,description)

print('\x1b[6;30;42m' + '\n\n\n\nThis is a short output containing only group names, from and to ports\n\n\n\n\n' + '\x1b[0m')

for security_group in all_security_groups['SecurityGroups']:
    for rule in security_group['IpPermissions']:
        try:
            print('Group name: ' + security_group['GroupName'] + ', FromPort: '  + str(rule['FromPort']) + ', ToPort: ' + str(rule['ToPort']))
        except KeyError:
            continue
