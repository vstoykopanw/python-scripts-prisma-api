
### The scrip will not work after next update to Prisma's "prismacloud.io/cloud/aws" API endpoint,
### that is currenly planned for February 2023.


import json
import requests


creds = {"username": "", "password": ""} # Your Access and Secret keys

login_url = "https://api3.prismacloud.io/login"        ### - Remember to edit your app stack number
acc_group_url = "https://api3.prismacloud.io/cloud/group"       ### - Remember to edit your app stack number
acc_onboard_url = "https://api3.prismacloud.io/cloud/aws"       ### - Remember to edit your app stack number

ACC_ID = input("Enter AWS Account ID: ")
ACC_GROUP_NAME = input("Enter Account Group Name: ")
ACC_NAME = input("Enter Account Name (To be shown in Prisma): ")
ROLE_ARN = input("Enter Role ARN: ")
EXTERNAL_ID = input("Enter External ID: ")


### Input examples:
# ACC_ID = "296938890305"
# ACC_NAME = "NoneProdAWSAccount"
# ACC_GROUP_NAME = "Default Account Group"
# ROLE_ARN = "arn:aws:iam::296938890305:role/PrismaCloudReadOnlyRole-oct-2022"
# EXTERNAL_ID = "665c487a-5f0a-4196-85a9-28e6f03d6c8c"



def login():

    r = requests.post(url = login_url, json = creds, timeout=5)
    if r.status_code == 200:
        token = json.loads((r.content).decode('utf-8'))['token']
        return token
    else:
        print("\n 'login' API status code: " + str(r.status_code) + " - " + r.reason + "\n")
        exit()
        

def acc_group_call():

    headers = {
        "x-redlock-auth": login(),
        "content-type": "application/json"
    }

    params = {
        "excludeCloudAccountDetails": True
    }

    r = requests.request("GET", acc_group_url, headers=headers, params=params)
    for ag in json.loads(r.text):
        if "name" in ag.keys():
            if ag["name"] == ACC_GROUP_NAME:
                return ag["id"], headers



def acc_onboard_call():

    acc_group_id, headers = acc_group_call()

    body = {
        "accountId": ACC_ID,
        "enabled": True,
        "groupIds": [acc_group_id],
        "name": ACC_NAME,
        "roleArn": ROLE_ARN,
        "protectionMode": "MONITOR_AND_PROTECT",    # Can be set to MONITOR or MONITOR_AND_PROTECT
        "externalId": EXTERNAL_ID
        }


    r = requests.request("POST", acc_onboard_url, headers=headers, json=body)
    print("\n 'x-redlock-status' Message: " + (r.headers)["x-redlock-status"])
    print("\n 'cloud/aws' API status code: " + str(r.status_code) + " - " + r.reason)



def main():

    acc_onboard_call()

    print("\nDone.\n")

main()