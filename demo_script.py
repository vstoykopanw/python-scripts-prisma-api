import requests
import pandas as pd



login_url = "https://api4.prismacloud.io/login"
ag_url = "https://api4.prismacloud.io/cloud/group"
acc_onboard_url = "https://api4.prismacloud.io/cloud/aws"

creds = {                                                  
    "username":"07b34dc9-dc8b-4b85-8316-279a04757a38",
    "password":"JKvnSADV3qILgKww2ZxNz72RFhg="
}



def login():

    r = requests.post(login_url, json=creds)
    return r.json()["token"]



def acc_group_call(ag_name):

    params = {
        "excludeCloudAccountDetails": False
    }
    headers = {
        "x-redlock-auth": login(),
        "content-type": "application/json"
    }
    r = requests.get(ag_url, headers=headers, params=params)

    for ag in r.json():
        if "name" in ag.keys():
            if ag["name"] == ag_name[0]:
                return ag["id"]

def acc_onboard_call(df):
    body = {
        "accountId": str(df.loc[[0], "account_id"][0]),
        "groupIds": [acc_group_call(df.loc[[0], "group_name"])],
        "name": df.loc[[0], "account_name"][0],
        "roleArn": df.loc[[0], "role_arn"][0],
        "externalId": df.loc[[0], "external_id"][0]
        }
    headers = {
        "x-redlock-auth": login(),
        "content-type": "application/json"
    }


    r = requests.post(acc_onboard_url, headers=headers, json=body)
    print("\n 'cloud/aws' enpoint status code: " + str(r.status_code) + " - " + r.reason)
    print("\n 'x-redlock-status' Message: " + (r.headers)["x-redlock-status"])
    


def main():

    df = pd.read_csv("test_table.csv")
    acc_onboard_call(df)



main()


