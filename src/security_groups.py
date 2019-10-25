import os
import boto3
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials

#Defining variables
csv_path = "./security_groups.csv"
scope = ['https://www.googleapis.com/auth/drive']
credentials = "./creds.json"
spreadsheet_id = "1eQzXpkcnRhCfTu9w9yJosM-x2EBqHQrJWutntfJStQA"

#This is for bold font on column headers

client = boto3.client('ec2')
all_security_groups = client.describe_security_groups()

if os.path.exists(csv_path):
    os.remove(csv_path)

with open(csv_path, 'w') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter=',')
    csvwriter.writerow(['Group Name', 'Group ID', 'Port Range', 'Source'])
    for security_group in all_security_groups['SecurityGroups']:
        for rule in security_group['IpPermissions']:
            for CidrIp in rule['IpRanges']:
                try:
                    if rule['FromPort'] == rule['ToPort']:
                        csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(rule['FromPort']), CidrIp['CidrIp']])
                    else:
                        csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(rule['FromPort']) + '-' + str(rule['ToPort']), CidrIp['CidrIp']])
                except KeyError as error:
                    if (str(error)) == "'FromPort'":
                        try:
                            csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All' + '-' + str(rule['ToPort']), CidrIp['CidrIp']])
                        except KeyError as error2:
                            if (str(error2)) == "'ToPort'":
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All', CidrIp['CidrIp']])

print('\x1b[6;30;42m' + '\n\n\n\nUploading / updating google spreadsheet\n\n\n\n' + '\x1b[0m')

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
gc = gspread.authorize(credentials)
content = open(csv_path, 'r').read()
gc.import_csv(spreadsheet_id, content)

print('The link is here: https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
