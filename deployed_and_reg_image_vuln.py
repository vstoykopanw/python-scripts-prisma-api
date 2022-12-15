### Script outputs a table with information on images impacted by provided vulnerability (CVE).
### Designed as a workaround to limitation of Prisma Compute version <= 22.01

import json
import requests
import pandas as pd


URL = input("Enter console URL: ")
# URL = "https://us-east1.cloud.twistlock.com/us-2-158320372"
if URL.endswith("/"):
    URL = URL[:-1]

BEARER = input("Enter your Bearer token: ")
# BEARER = "yyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidnN0b3lrb0BwYWxvYWx0b25ldHdvcmtzLmNvbSIsInJvbGUiOiJhZG1pbiIsImdyb3VwcyI6bnVsbCwicm9sZVBlcm1zIjpbWzI1NSwyNTUsMjU1LDI1NSwyNTUsMTI3LDFdLFsyNTUsMjU1LDI1NSwyNTUsMjU1LDEyNywxXV0sInNlc3Npb25UaW1lb3V0U2VjIjo2MDAsInNhYXNUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKMmMzUnZlV3R2UUhCaGJHOWhiSFJ2Ym1WMGQyOXlhM011WTI5dElpd2ljMlZ5ZG1salpWVnpZV2RsVDI1c2VTSTZkSEoxWlN3aVptbHljM1JNYjJkcGJpSTZabUZzYzJVc0luQnlhWE50WVVsa0lqb2lPVEF5TlRrNU16UTBPVGMxTnpVNU16WXdJaXdpYVhCQlpHUnlaWE56SWpvaU16UXVOelF1T0RRdU5URWlMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwyRndhVEl1Y0hKcGMyMWhZMnh2ZFdRdWFXOGlMQ0p5WlhOMGNtbGpkQ0k2TUN3aWRYTmxjbEp2YkdWVWVYQmxSR1YwWVdsc2N5STZleUpvWVhOUGJteDVVbVZoWkVGalkyVnpjeUk2Wm1Gc2MyVjlMQ0oxYzJWeVVtOXNaVlI1Y0dWT1lXMWxJam9pVTNsemRHVnRJRUZrYldsdUlpd2lhWE5UVTA5VFpYTnphVzl1SWpwMGNuVmxMQ0pzWVhOMFRHOW5hVzVVYVcxbElqb3hOalk0TkRNMk9UUTVPRGN4TENKaGRXUWlPaUpvZEhSd2N6b3ZMMkZ3YVRJdWNISnBjMjFoWTJ4dmRXUXVhVzhpTENKMWMyVnlVbTlzWlZSNWNHVkpaQ0k2TVN3aWMyVnNaV04wWldSRGRYTjBiMjFsY2s1aGJXVWlPaUpRWVd4dklFRnNkRzhnVG1WMGQyOXlhM01nS0ZSRlUxUWdRVU5EVkNrZ0xTQTFOREU0TVRZME1UWTNNREU0TnprNE1EUTRJaXdpYzJWemMybHZibFJwYldWdmRYUWlPall3TENKMWMyVnlVbTlzWlVsa0lqb2laak0xWXprNU9EZ3RNV1poTVMwMFpUYzVMV0U0TldFdE5ETXhZV1UxTldJeE1qUTRJaXdpYUdGelJHVm1aVzVrWlhKUVpYSnRhWE56YVc5dWN5STZabUZzYzJVc0ltVjRjQ0k2TVRZMk9EUXpOelUyT1N3aWFXRjBJam94TmpZNE5ETTJPVFk1TENKMWMyVnlibUZ0WlNJNkluWnpkRzk1YTI5QWNHRnNiMkZzZEc5dVpYUjNiM0pyY3k1amIyMGlMQ0oxYzJWeVVtOXNaVTVoYldVaU9pSlRlWE4wWlcwZ1FXUnRhVzRpZlEuOE1xVW5NVmRmSGZ1SjBGZ2xfcWJRQjRoQUloWlVLdXhyVXVLdGFmNFlNRSIsImV4cCI6MTY2ODQ0MDU2OSwiaXNzIjoidHdpc3Rsb2NrIn0.guHmaldM4YQRoxCN_nTBcpy7UJfL4mMWxCAd6gurddw"

headers = {"Authorization": str("Bearer " + BEARER)}

CVE = input("Enter CVE ID: ")
# CVE = "CVE-2022-42889" #(text4shell)

params = {
    "cve": CVE
}



def resource_data():

    r = requests.get(url=(URL+"/api/v22.01/stats/vulnerabilities/impacted-resources"), headers = headers, params=params)
    if r.status_code == 200:
        resource_info = json.loads(r.text)
        return resource_info
    else:
        print("\nERROR. ('impacted-resources' endpoint)\n")
        print(str(r.status_code) + " - " + r.reason)
        exit()
        


def registry_data():

    temp = []
    r = requests.get(url=(URL+"/api/v22.01/registry"), headers = headers)

    if r.status_code == 200:
        pass
    else:
        print("\nERROR. ('registry' endpoint)\n")
        print(str(r.status_code) + " - " + r.reason)
        exit()

    pages = int(r.headers["Total-Count"]) // 50
    if int(r.headers["Total-Count"]) % 50 > 0:
        pages += 1
    print("\nEstimate time to complete is " + str(int(pages*1.5)) + " seconds.\n\n Working... \n")
    offset = 0

    for p in range(0, pages):
        params = {
            "limit": 50,
            "offset": offset
        }

        r = requests.get(url=(URL+"/api/v22.01/registry"), headers = headers, params=params)
        if r.status_code == 200:
            data = json.loads(r.text)
            pass
        else:
            print("\nERROR. ('registry' endpoint on page )" + p + "\n" )
            print(str(r.status_code) + " - " + r.reason)
            exit()

        for i in data:
            if (i["vulnerabilities"]):
                for v in i["vulnerabilities"]:
                    if v["cve"] == CVE:
                        temp.append(i["_id"])
        
        offset += 50

    registry_info = set(temp)
          
    return registry_info



def main():

    resource_info = resource_data()
    
    images = []
    nodes = []
    containers = []
    sha = []
    hosts = []
    resource_types = []
    registries = []

    if (resource_info["riskTree"]) is None:
        print("\nNo " + CVE + " vulnerabilities found.\n")
        exit()

    for k in resource_info["riskTree"].keys():
        for i in (resource_info["riskTree"])[k]:

            images.append(i["image"])
            containers.append(i["container"])
            nodes.append(i["host"])
            sha.append(k)
            resource_types.append("Deployed Image")
            registries.append(None)    

    if "hosts" in resource_info.keys():

        for h in resource_info["hosts"]:
            images.append(None)
            containers.append(None)
            nodes.append(h)
            sha.append(None)
            resource_types.append("Host")
            registries.append(None)
    

    registry_info = registry_data()

    for reg in registry_info:
        images.append(None)
        containers.append(None)
        nodes.append(None)
        sha.append(None)
        resource_types.append("Registry Image")
        registries.append(reg)

    d1 = {
        "Image Type": resource_types,
        "Resource ID": registries,
        "Images": images,
        "Hosts": nodes,
        "Containers": containers,        
        "Sha": sha
    }


    df = pd.DataFrame(d1)
    df.to_csv(str(CVE + "_vuln_images.csv"), encoding='utf-8')

    print("\nDone.\n")


main()
