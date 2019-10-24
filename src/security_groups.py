import os
import json
import boto3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Defining variables
csv_path = "./security_groups.csv"
scope = ['https://www.googleapis.com/auth/drive']
credentials = "./creds.json"
spreadsheet_id = "1eQzXpkcnRhCfTu9w9yJosM-x2EBqHQrJWutntfJStQA"

print('\x1b[6;30;42m' + '\n\n\n\nThis is a long output containing complete security group descriptions\n\n\n\n\n' + '\x1b[0m')

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

print('\x1b[6;30;42m' + '\n\n\n\nWriting csv file with from and to ports\n\n\n\n\n' + '\x1b[0m')

if os.path.exists(csv_path):
    os.remove(csv_path)
f = open(csv_path,"a+")

for security_group in all_security_groups['SecurityGroups']:
    for rule in security_group['IpPermissions']:
        try:
            f.write('Group name: ' + security_group['GroupName'] + ', FromPort: '  + str(rule['FromPort']) + ', ToPort: ' + str(rule['ToPort']) + ',IPs: ' + str(rule['IpRanges']).replace(',',' ') + ', UserIdGroupPairs ' + str(rule['UserIdGroupPairs']).replace(',',' ') + '\n')
        except KeyError as error:
            if (str(error)) == "'FromPort'":
                try:
                    f.write('Group name: ' + security_group['GroupName'] + ', FromPort: '  + 'All' + ', ToPort: ' + str(rule['ToPort']) + ',IPs:' + str(rule['IpRanges']).replace(',',' ') + ', UserIdGroupPairs ' +  str(rule['UserIdGroupPairs']).replace(',',' ') + '\n')
                except KeyError as error2:
                    if (str(error2)) == "'ToPort'":
                        f.write('Group name: ' + security_group['GroupName'] + ', FromPort: '  + 'All' + ', ToPort: ' + 'All' + ',IPs:' + str(rule['IpRanges']).replace(',',' ') +  ', UserIdGroupPairs ' + str(rule['UserIdGroupPairs']).replace(',',' ') + '\n')

f.close()

print('\x1b[6;30;42m' + '\n\n\n\nUploading / updating google spreadsheet\n\n\n\n' + '\x1b[0m')

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
gc = gspread.authorize(credentials)
content = open(csv_path, 'r').read()
gc.import_csv(spreadsheet_id, content)

print('The link is here: https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
