import urllib.request
import urllib.parse
import re
import json

def get_huawei_token():
    url='https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens'
    data={
  "auth": {
  "identity": {
  "methods": [
  "PASSWORD"
  ],
  "PASSWORD": {
  "user": {
  "name": "pengxuan_lab",
  "PASSWORD": "PXliex3tome*",
  "domain": {
  "name": "pengxuan_lab"
  }
  }
  }
  },
  "scope": {
  "project": {
  "name": "cn-north-1"
  }
  }
  }
  }
    data=json.dumps(data)
    data=bytes(data,'utf8')
    header={
  'Content-Type':"application/json;charset=utf8"
  } 

    request=urllib.request.Request(url,data,headers=header)
    reponse=urllib.request.urlopen(request)

    info=reponse.info()
    dic=(str(info)).split('\n')
    return(re.sub("X-Subject-Token: ","",dic[6]))


def get_baidu_token():
    url='https://aip.baidubce.com/oauth/2.0/token?'
    grant_type='client_credentials'
    client_id='GT0VGBYFbrqmUYyU0h5mRuX6'
    client_secret='9Ble1nWnOQMy8MaAcLYg8iD7ts8DCgmy'
    url_all=url+'grant_type='+grant_type+'&client_id='+client_id+'&client_secret='+client_secret

    request=urllib.request.Request(url=url_all)
    reponse=urllib.request.urlopen(request)
    content=reponse.read()
    dic=eval(content.decode())
    
    return (dic['access_token'])
    
#print (get_baidu_token())
#print (get_huawei_token())