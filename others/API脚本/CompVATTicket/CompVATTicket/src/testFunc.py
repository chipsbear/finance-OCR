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
tmpdata='../Jan2019_benchmark300_scan/cache/'
tmpresult='../Jan2019_benchmark300_scan/output/'
def test_Xunfei(IMAGE_NAME,path_img,rootdir_result,token):
    global HTTPERROR
    HTTPERROR=1
    url='http://webapi.xfyun.cn/v1/service/v1/ocr/invoice'
    curtime=str(int(time.time()))
    appid='5caefc84'
    apikey=token   
    param={"engine_type":"invoice"}
    xparam=b64encode(bytes(json.dumps(param),encoding="utf-8"))
    checksum=hashlib.md5((apikey+curtime+(str)(xparam.decode())).encode())
    
    header={              
        'X-Appid':appid,
        'X-CurTime':curtime,
        'X-Param':xparam,
        'X-CheckSum':checksum.hexdigest()
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    
    base64_bytes=b64encode(byte_content)
    data={"image":base64_bytes}
    data=urllib.parse.urlencode(data)
    data=data.encode('utf-8')
    
   
    request=urllib.request.Request(url,data,headers=header)
    singlename=IMAGE_NAME.split('.')
    singlename=singlename[0]
    try:
        reponse=urllib.request.urlopen(request)
    
    except urllib.error.HTTPError:
        print("==== Ali An HTTP Error Generated =====",)
        HTTPERROR=0        
    else:
        cont=reponse.read()
        fh=open(rootdir_result+"xunfei/"+singlename+".json","wb")
        fh.write(cont)
        fh.close()
        #path_list[0]=rootdir_result+"ali/"+singlename+".json"
        return rootdir_result+"xunfei/"+singlename+".json"
    
def test_Ali(IMAGE_NAME,path_img,rootdir_result,token):
    global HTTPERROR
    HTTPERROR=1
    url='https://ocrapi-invoice.taobao.com/ocrservice/invoice'
    header={              
        'Content-Type':'application/json',
        'Authorization':'APPCODE '+token
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    
    base64_bytes=b64encode(byte_content)
    base64_string=base64_bytes.decode(ENCODING)
    
    data={"query":base64_string}
    data=bytes(json.dumps(data),encoding="utf-8")
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
        
def test_Huawei(IMAGE_NAME,path_img,rootdir_result,token):
    global HTTPERROR
    HTTPERROR=1
    url='https://ais.cn-north-1.myhuaweicloud.com/v1.0/ocr/vat-invoice'
    
    header={              
        'Content-Type':'application/json',
        'X-Auth-Token':token
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    
    base64_bytes=b64encode(byte_content)
    base64_string=base64_bytes.decode(ENCODING)

    data={"image":base64_string,"url":""}
    data=bytes(json.dumps(data),encoding="utf-8")
    request=urllib.request.Request(url,data,headers=header)
    singlename=IMAGE_NAME.split('.')
    singlename=singlename[0]
    try:
        reponse=urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        print("==== Huawei An HTTP Error Generated =====")
        HTTPERROR=0
    else:
        cont=reponse.read()
        fh=open(rootdir_result+"huawei_ocr/"+singlename+".json","wb")
        fh.write(cont)
        fh.close()
        #path_list[2]=rootdir_result+"huawei_ocr/"+singlename+".json"
        return rootdir_result+"huawei_ocr/"+singlename+".json"
def test_Yidao(IMAGE_NAME,path_img,rootdir_result,access_token):
    global HTTPERROR
    global path_list
    
    url_all='http://api.exocr.com/ocr/v1/invoice'
    header={              
        'Content-Type':'application/x-www-form-urlencoded',
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    
    base64_bytes=b64encode(byte_content)
    base64_string=base64_bytes.decode(ENCODING)

    data={"image_base64":base64_string,"AK":"bc3d03d1e58249fc857c4cab3cab4e37","app_secret":"190714e1413da50c3019c094febe96c9"}
    data=urllib.parse.urlencode(data)
    data=data.encode('utf-8')
    request=urllib.request.Request(url_all,data,headers=header)
    singlename=IMAGE_NAME.split('.')
    singlename=singlename[0]
    try:
        reponse=urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        print("==== 易道博识 An HTTP Error Generated =====")#Never happens
        HTTPERROR=0
    else:
        cont=reponse.read()
        fh=open(rootdir_result+"yidao/"+singlename+".json","wb")
        fh.write(cont)
        fh.close()
        #path_list[1]=rootdir_result+"_baidu/"+singlename+".json"
        return rootdir_result+"yidao/"+singlename+".json"    
    
def test_Baidu(IMAGE_NAME,path_img,rootdir_result,access_token):
    global HTTPERROR
    global path_list
    #print(IMAGE_NAME)
    url='https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice?'
    url_all=url+'access_token='+access_token
    header={              
        'Content-Type':'application/x-www-form-urlencoded',
    } 
    with open(path_img+IMAGE_NAME,'rb') as jpg_file:
        byte_content=jpg_file.read()
    
    base64_bytes=b64encode(byte_content)
    base64_string=base64_bytes.decode(ENCODING)

    data={"image":base64_string,"accuracy":"high"}
    data=urllib.parse.urlencode(data)
    data=data.encode('utf-8')
    request=urllib.request.Request(url_all,data,headers=header)
    singlename=IMAGE_NAME.split('.')
    singlename=singlename[0]
    try:
        reponse=urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        print("==== Baidu An HTTP Error Generated =====")#Never happens
        HTTPERROR=0
    else:
        cont=reponse.read()
        fh=open(rootdir_result+"_baidu/"+singlename+".json","wb")
        fh.write(cont)
        fh.close()
        #path_list[1]=rootdir_result+"_baidu/"+singlename+".json"
        return rootdir_result+"_baidu/"+singlename+".json"
#test_Yidao("photo0703PTFP003.jpg","../Jan2019_benchmark300_photo/cache/","../Jan2019_benchmark300_photo/output/","190714e1413da50c3019c094febe96c9")

#for parent,dirnames,filenames in os.walk(tmpdata):
#    for filename in filenames:
#        test_Yidao(filename,tmpdata,tmpresult,'190714e1413da50c3019c094febe96c9') 
#test_Xunfei('X00400001PEQ.jpg','./cache/','e6afe47cdb2610b19c87afaec59684b1')

def test_RuiQi(IMAGE_NAME,path_img,rootdir_result):
    global HTTPERROR
    global path_list
    #print(IMAGE_NAME)
    appkey = "5cb4a528"  #这里输入提供的app_key 
    appsecret = "e92256ce33b87e17a8fa805d8cfd6868"#这里输入提供的app_secret 

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
        data = {'image_data': base64_string, 'AK': appkey, 'timestamp': str(timestamp), 'token': token}
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
