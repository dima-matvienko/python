import json
import boto3

client = boto3.client('ec2')
all_security_groups = client.describe_security_groups()
pretty_print = json.dumps(all_security_groups, indent=4)

print(pretty_print)

security_groups_short = {}

for security_group in all_security_groups['SecurityGroups']:
   security_groups_short[security_group['GroupName']] = security_group['Description']

print(security_groups_short)