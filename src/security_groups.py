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


client = boto3.client('ec2')
security_groups = client.describe_security_groups()

if os.path.exists(csv_path):
    os.remove(csv_path)

with open(csv_path, 'w') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter=',')
    for security_group in security_groups['SecurityGroups']:
        for IpPermission in security_group['IpPermissions']:
            for IpRange in IpPermission['IpRanges']:
                try:
                    if IpPermission['FromPort'] == IpPermission['ToPort']:
                        if 'Description' in IpRange:
                            csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']), IpRange['CidrIp'], IpRange['Description']])
                        else:
                            csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']), IpRange['CidrIp']])
                    else:
                        if 'Description' in IpRange:
                            csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']) + '-' + str(IpPermission['ToPort']), IpRange['CidrIp'], IpRange['Description']])
                        else:
                            csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']) + '-' + str(IpPermission['ToPort']), IpRange['CidrIp']])
                except KeyError as from_error:
                    if (str(from_error)) == "'FromPort'":
                        try:
                            if 'Description' in IpRange:
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All' + '-' + str(IpPermission['ToPort']), IpRange['CidrIp'], IpRange['Description']])
                            else:
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All' + '-' + str(IpPermission['ToPort']), IpRange['CidrIp']])
                        except KeyError as to_error:
                            if (str(to_error)) == "'ToPort'":
                                if 'Description' in IpRange:
                                    csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All', IpRange['CidrIp'], IpRange['Description']])
                                else:
                                    csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All', IpRange['CidrIp']])


with open(csv_path, 'a') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',')
        for security_group in security_groups['SecurityGroups']:
            for IpPermission in security_group['IpPermissions']:
                for UserIdGroupPair in IpPermission['UserIdGroupPairs']:
                    try:
                        if IpPermission['FromPort'] == IpPermission['ToPort']:
                            if 'Description' in UserIdGroupPair:
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']), UserIdGroupPair['GroupId'], UserIdGroupPair['Description']])
                            else:
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']), UserIdGroupPair['GroupId']])
                        else:
                            if 'Description' in UserIdGroupPair:
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']) + '-' + str(IpPermission['ToPort']),  UserIdGroupPair['GroupId'], UserIdGroupPair['Description']])
                            else:
                                csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], str(IpPermission['FromPort']) + '-' + str(IpPermission['ToPort']),  UserIdGroupPair['GroupId']])
                    except KeyError as from_error:
                        if (str(from_error)) == "'FromPort'":
                            try:
                                if 'Description' in UserIdGroupPair:
                                    csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All' + '-' + str(IpPermission['ToPort']), UserIdGroupPair['GroupId'], UserIdGroupPair['Description']])
                                else:
                                    csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All' + '-' + str(IpPermission['ToPort']), UserIdGroupPair['GroupId']])
                            except KeyError as to_error:
                                if (str(to_error)) == "'ToPort'":
                                    if 'Description' in UserIdGroupPair:
                                        csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All', UserIdGroupPair['GroupId'], UserIdGroupPair['Description']])
                                    else:
                                        csvwriter.writerow([security_group['GroupName'], security_group['GroupId'], 'All', UserIdGroupPair['GroupId']])


print('\x1b[6;30;42m' + '\nUploading / updating google spreadsheet\n' + '\x1b[0m')

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
gc = gspread.authorize(credentials)
content = open(csv_path, 'r').read()
split_content = content.split('\n')
sorted_content = "\n".join(sorted(split_content))
gc.import_csv(spreadsheet_id, sorted_content)

print('The link is here: https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
