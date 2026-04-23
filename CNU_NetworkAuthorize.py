from u679c import encrypt
import requests
import os
import json

# 禁用代理
proxies = None

currentDir = os.path.dirname(__file__)
userConfFp = os.path.join(currentDir, "userConf.json")

class OnlineDevice:
    def __init__(self, infoDict):
        self.ip = infoDict["IP"]
        self.mac = infoDict["MAC"]
        self.vlan = infoDict["VLAN"]
        self.packageNameOccupied = infoDict["Package"]["套餐名称"]
        
class FrequentlyUsedDevice:
    def __init__(self, infoDict):
        self.mac = infoDict["MAC"]
        self.desc = infoDict["Desc"]
        
class Info:
    def __init__(self, infoDict):
        self.ip = infoDict["IP"]
        self.mac = infoDict["MAC"]
        self.name = infoDict["XM"]
        self.department = infoDict["DP"]
        self.numberOfPackages = infoDict["MOC"]
        self.packages = [package["套餐名称"] for package in infoDict["KXTC"]]
        self.userGroup = infoDict["UG"]
        self.onlineDevice = [OnlineDevice(onlineDevice) for onlineDevice in infoDict["OIA"]]
        self.frequentlyUsedDevice = [FrequentlyUsedDevice(frequentlyUsedDevice) for frequentlyUsedDevice in infoDict["CYXX"]]
        
def createConfigurationFile():
    data = {
        "username": "这里改成你的学号",
        "password": "这里改成你的校园网密码",
        "defaultPackage": "这里改成你的默认: 例如电信-100M"
    }
    f = open(userConfFp, "w", encoding="utf8")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.close()


def try2GetJsonFromResponse(response):
    try:
        return response.json()
    except Exception:
        print(response.text)
        print("解析响应失败")
        exit()

# 如果配置文件不存在, 先创建配置文件
if not os.path.exists(userConfFp):
    createConfigurationFile()


try:
    f = open(userConfFp, "r", encoding="utf8")
    userInfo = json.load(f)
except FileNotFoundError:
    createConfigurationFile()
    print("配置文件丢失, 已重新生成, 请填写后重试!")
except json.JSONDecodeError:
    print("配置文件格式错误")
finally:
    f.close()


student_id = userInfo["username"]                   
account_password = encrypt(student_id, userInfo["password"])


# 构造cookies
cookies = {
    "username": student_id,
    "password": account_password
}

# 构造headers
headers = {
    "Origin": "http://cc.nsu.edu.cn",
    "Referer": "http://cc.nsu.edu.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7",
}


data_since_login = {"username":student_id, "password": account_password,"remember":"true","DoWhat":"Login"}
data_since_get_info = {"DoWhat":"GetInfo"}

auth_url = "http://2.2.2.2/Auth.ashx"

response = requests.post(auth_url, headers=headers, json=data_since_login, cookies=cookies, verify=False, proxies=proxies)
data = try2GetJsonFromResponse(response)

print(data["Message"])
if not data["Result"]:
    exit()


response = requests.post(auth_url, headers=headers, json=data_since_get_info, cookies=cookies, verify=False, proxies=proxies)
data = try2GetJsonFromResponse(response)
print(data["Message"])
if not data["Result"]:
    exit()
    
info = Info(data["Data"])

data_since_open_net = {"DoWhat":"OpenNet","Package": info.userGroup[:-1] + "-" + userInfo['defaultPackage']}
response = requests.post(auth_url, headers=headers, json=data_since_open_net, cookies=cookies, verify=False, proxies=proxies)
data = try2GetJsonFromResponse(response)
print(data)
if not data["Result"]:
    exit()


print(f"\nOkk啦, {info.name}同学， 尽情冲浪吧！\n当前IP: {info.ip}\n当前mac: {info.mac}\n当前学号: {student_id}")
