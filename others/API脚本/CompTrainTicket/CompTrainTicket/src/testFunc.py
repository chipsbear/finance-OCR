import tokenFunc
import urllib.request
import urllib.parse
import time
import hashlib
import os
from base64 import b64encode
import json
import os 
import io 
import requests  
import datetime 
import codecs 
import uuid 
import traceback 
ENCODING='utf-8'
#rootdir_result="./output/"
#path_list=["","",""]
HTTPERROR=1
    
def test_Ali(IMAGE_NAME,path_img,rootdir_result,token):
    global HTTPERROR
    HTTPERROR=1
    url='https://ocrhcp.market.alicloudapi.com/api/predict/ocr_train_ticket'
    header={
        'Content-Type':'application/json',
        'Authorization':'APPCODE '+token
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    #print(IMAGE_NAME)
    base64_bytes=b64encode(byte_content)
    base64_string=base64_bytes.decode(ENCODING)
    
    data={"image":base64_string}
    data=bytes(json.dumps(data),encoding=ENCODING)
    
    request=urllib.request.Request(url,data,headers=header)
    singlename=IMAGE_NAME.split('.')
    singlename=singlename[0]    
    try:
        reponse=urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        print("==== Ali An HTTP Error Generated =====")
        HTTPERROR=0        
    else:
        cont=reponse.read()
        fh=open(rootdir_result+"ali/"+singlename+".json","wb")
        fh.write(cont)
        fh.close()
        #path_list[0]=rootdir_result+"ali/"+singlename+".json"
        return rootdir_result+"ali/"+singlename+".json"
    
def test_Baidu(IMAGE_NAME,path_img,rootdir_result,access_token):
    global HTTPERROR
    global path_list
    print(IMAGE_NAME)
    url='https://aip.baidubce.com/rest/2.0/ocr/v1/train_ticket?'
    url_all=url+'access_token='+access_token
    header={              
        'Content-Type':'application/x-www-form-urlencoded',
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    
    base64_bytes=b64encode(byte_content)
    base64_string=base64_bytes.decode(ENCODING)

    data={"image":base64_string}
    data=urllib.parse.urlencode(data)
    data=data.encode('utf-8')
    request=urllib.request.Request(url_all,data,headers=header)
    singlename=IMAGE_NAME.split('.')
    singlename=singlename[0]
    try:
        reponse=urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        print("==== Baidu An HTTP Error Generated =====")
        HTTPERROR=0
    else:
        cont=reponse.read()
        fh=open(rootdir_result+"_baidu/"+singlename+".json","wb")
        fh.write(cont)
        fh.close()
        #path_list[1]=rootdir_result+"_baidu/"+singlename+".json"
        return rootdir_result+"_baidu/"+singlename+".json"
'''
for parent,dirnames,filenames in os.walk("./cache"):
    for filename in filenames:
        test_Ali(filename,"./cache/","./output/","80b8d3a52d3b48f98ce21d74df1508c6")

access_token=tokenFunc.get_baidu_token()
for parent,dirnames,filenames in os.walk("./cache"):
    for filename in filenames:
        test_Baidu(filename,'./cache/','./tested/',access_token)
'''
def test_RuiQi(IMAGE_NAME,path_img,rootdir_result):
    global HTTPERROR
    global path_list
    #print(IMAGE_NAME)
    appkey = "5c88b702"  #这里输入提供的app_key 
    appsecret = "f031667b04e7aae6b16ad4ccad0b5d7e"#这里输入提供的app_secret 

    api_url = "http://fapiao.glority.cn/v1/item/get_item_info"
    result = {}

    try: 
        # generate timestamp 
        timestamp = int(time.time()) 

        # generate token 
        m = hashlib.md5() 
        token = appkey + "+" + str(timestamp) + "+" + appsecret 
        m.update(token.encode('utf-8')) 
        token = m.hexdigest() 
        
        with open(path_img+IMAGE_NAME,'rb') as jpg_file:
            byte_content = jpg_file.read()
        base64_bytes=b64encode(byte_content)
        base64_string=base64_bytes.decode(ENCODING)

        # post request 
        data = {'image_data': base64_string, 'AK': appkey, 'type':2,'timestamp': str(timestamp), 'token': token}
        r = requests.post(api_url, data=data)
        singlename=IMAGE_NAME.split('.')
        singlename=singlename[0]
        print(singlename)
        if r.status_code != 200: 
            print("failed to get info from : ", image_url) 
        else: 
            result = r.json()
            r=bytes('{}'.format(result),'utf-8')
            fh=open(rootdir_result+"ruiqi/"+singlename+".json","wb")
            fh.write(r)
            fh.close()
            return rootdir_result+"ruiqi/"+singlename+".json"
    except: 
        traceback.print_exc() 
    return result