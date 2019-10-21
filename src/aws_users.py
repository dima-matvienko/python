import json
import boto3

client = boto3.client('iam')
iam_all_users = client.list_users()
pretty_print = json.dumps(iam_all_users, indent=4, sort_keys=True, default=str)

print(pretty_print)

users_short = {}

for user in iam_all_users['Users']:
    users_short[user['UserName']] = user['Path']

print(users_short)
