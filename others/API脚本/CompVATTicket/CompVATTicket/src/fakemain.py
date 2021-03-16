# -*- coding: utf-8 -*-
import json
import csv
import re
import shutil
import argparse
import time,datetime
import sys
import testFunc
import tokenFunc
import testbadFunc
import selfConvert
import compFunc
import mknewdir
import os
from threading import Thread
from collections import namedtuple

################################################################################
#####################  GLOBAL VARIABLES  #######################################
################################################################################
ENCODING_JSON='utf-8'
motherdir='../default_rootdir'

rootdir_answer = motherdir+"/answer/"
rootdir_prmanswer=motherdir+"/primitive_answer/"
rootdir_data=motherdir+"/cache/"
rootdir_tested=motherdir+"/tested/"
rootdir_bad=motherdir+"/bad/"
rootdir_result=motherdir+"/output/"
rootdir_info="../sysinfo/"
rootdir_invalidjson=motherdir+"/invalidjson/"
################################################################################
##################### BIG FUNCTION BELOW  ######################################
################################################################################

                                
def callAPI(directory):
    token_huawei=tokenFunc.get_huawei_token()
    token_baidu=tokenFunc.get_baidu_token()
    token_ali='80b8d3a52d3b48f98ce21d74df1508c6'
    token_xunfei='8057ed3b1be17b402cd03e88068e3478'
    token_yidao='190714e1413da50c3019c094febe96c9'
    for parent,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            print ("testing..." + filename)
            singlename=filename.split('.')
            singlename=singlename[0]
            
            ######  Multithreads used  ########
            t_huawei = Thread(target=testFunc.test_Huawei, args=(filename,directory,rootdir_result,token_huawei))
            t_ali = Thread(target=testFunc.test_Ali, args=(filename,directory,rootdir_result,token_ali))
            t_baidu = Thread(target=testFunc.test_Baidu, args=(singlename+'.jpg',directory,rootdir_result,token_baidu))
            t_xunfei = Thread(target=testFunc.test_Xunfei, args=(filename,directory,rootdir_result,token_xunfei))
            t_yidao = Thread(target=testFunc.test_Yidao, args=(filename,directory,rootdir_result,token_yidao))
            t_ruiqi = Thread(target=testFunc.test_RuiQi, args=(filename,directory,rootdir_result))
            
            t_baidu.start()
            t_huawei.start()
            t_ali.start()
            t_xunfei.start()
            t_yidao.start()
            t_ruiqi.start()
                               
            t_baidu.join()
            t_ali.join()
            t_huawei.join()
            t_xunfei.join()
            t_yidao.join()
            t_ruiqi.join()
            
            shutil.move(directory+filename, rootdir_tested)
                                                          
            #Move tested images to another folder
#             if(testFunc.HTTPERROR==1):
#                 shutil.move(directory+filename, rootdir_tested)
#             else:
#                 shutil.move(directory+filename,rootdir_bad)
            #then test if _baidu has bad jsons, if yes, give it 3 chances
    dict_baidu={'token':token_baidu,'compname':'_baidu','rootdir_result':rootdir_result}
    dict_xunfei={'token':token_xunfei,'compname':'xunfei','rootdir_result':rootdir_result}
    dict_yidao={'token':token_yidao,'compname':'yidao','rootdir_result':rootdir_result}
    
    testbadFunc.retest(rootdir_invalidjson,rootdir_tested,rootdir_data,testFunc.test_Xunfei,dict_xunfei)
    testbadFunc.retest(rootdir_invalidjson,rootdir_tested,rootdir_data,testFunc.test_Baidu,dict_baidu)
    testbadFunc.retest(rootdir_invalidjson,rootdir_tested,rootdir_data,testFunc.test_Yidao,dict_yidao)
    
    try:
        os.makedirs(rootdir_result+"yidaonew/")
    except FileExistsError:
        print(rootdir_result+"yidaonew/ already created")
    try:
        os.makedirs(rootdir_result+"ruiqinew/")
    except FileExistsError:
        print(rootdir_result+"ruiqinew/ already created")
        
    selfConvert.convert_allyidao(rootdir_result+"yidao/",rootdir_result+"yidaonew/")
    selfConvert.convert_allruiqi(rootdir_result+"ruiqi/",rootdir_result+"ruiqinew/")

    os.rename(rootdir_result+"yidao/",rootdir_result+"yidao_old/")
    os.rename(rootdir_result+"yidaonew/",rootdir_result+"yidao/")
    os.rename(rootdir_result+"ruiqi/",rootdir_result+"ruiqi_old/")
    os.rename(rootdir_result+"ruiqinew/",rootdir_result+"ruiqi/")

    testbadFunc.putBlankJSON(rootdir_result,'_baidu')
    testbadFunc.putBlankJSON(rootdir_result,'xunfei')
    testbadFunc.putBlankJSON(rootdir_result,'yidao')
    
def compall():
       
    foutput=open(rootdir_result+re.sub("../","",motherdir)+"_analyse.csv","wb")
    
    t=compFunc.ferror
    calcPercent=compFunc.calcPercent
    tmp="Name,Ali_Correct_Num,Baidu_Correct_Num,Huawei_Correct_Num,Xunfei_Correct_Num,Yidao_Correct_Num,Ruiqi_Correct_Num,Ali_Comp_Num,Baidu_Comp_Num,Huawei_Comp_Num,Xunfei_Comp_Num,Yidao_Comp_Num,Ruiqi_Comp_Num,All_Comp_Num,AliRate,BaiduRate,HuaweiRate,XunfeiRate,YidaoRate,RuiqiRate\n" 
    tmp=tmp.encode()
    foutput.write(tmp)
    frate_ali=0
    frate_baidu=0
    frate_huawei=0
    frate_xunfei=0
    frate_yidao=0
    frate_ruiqi=0
    nb_img=0
    compFunc.buildDict()
    #print("before:::\n",compFunc.dict_ziduan)
    
    for parent,dirnames,filenames in os.walk(rootdir_tested):
        for filename in filenames:
                   
            tmp=filename
            print(tmp)
            
            
            tmp=tmp.encode()
            t.write(tmp)
                      
            singlename=filename.split('.')
            singlename=singlename[0]
                                                        
            fanswer=open(rootdir_answer+singlename+".json",encoding=ENCODING_JSON)
            content_answer=json.load(fanswer)#answer
            
            content_ali=compFunc.prepData(rootdir_result,"ali",singlename,ENCODING_JSON)
            content_baidu=compFunc.prepData(rootdir_result,"_baidu",singlename,ENCODING_JSON)
            content_huawei=compFunc.prepData(rootdir_result,"huawei_ocr",singlename,ENCODING_JSON)
            content_xunfei=compFunc.prepData(rootdir_result,"xunfei",singlename,ENCODING_JSON)
            content_yidao=compFunc.prepData(rootdir_result,"yidao",singlename,ENCODING_JSON)
            content_ruiqi=compFunc.prepData(rootdir_result,"ruiqi",singlename,ENCODING_JSON)
            rali,rbaidu,rhuawei,rxunfei,ryidao,rruiqi,valid_ali,valid_baidu,valid_huawei,valid_xunfei,valid_yidao,valid_ruiqi,rcomp=compFunc.compFile(content_ali,content_baidu,content_huawei,content_xunfei,content_yidao,content_ruiqi,content_answer)
            
            nb_img+=1
            frate_ali+=rali/valid_ali
            frate_baidu+=rbaidu/valid_baidu
            frate_huawei+=rhuawei/valid_huawei
            frate_xunfei+=rxunfei/valid_xunfei
            frate_yidao+=ryidao/valid_yidao
            frate_ruiqi+=rruiqi/valid_ruiqi
            #print(frate_ali,frate_baidu,frate_huawei)
            tmp1=filename+ ","+str(rali)+","+str(rbaidu)+","+str(rhuawei)+","+str(rxunfei)+","+str(ryidao)+","+str(rruiqi)+','
            tmp2=str(valid_ali)+","+str(valid_baidu)+","+str(valid_huawei)+","+str(valid_xunfei)+","+str(valid_yidao)+","+str(valid_ruiqi)+','+str(rcomp)+","
            tmp3=calcPercent(rali/valid_ali)+","+calcPercent(rbaidu/valid_baidu)+","+calcPercent(rhuawei/valid_huawei)+","+calcPercent(rxunfei/valid_xunfei)+","+calcPercent(ryidao/valid_yidao)+","+calcPercent(rruiqi/valid_ruiqi)+"\n"
            
            tmp=tmp1+tmp2+tmp3
            t.write(("\n").encode())
            foutput.write(tmp.encode())                                  
            fanswer.close()
              
    frate_ali=frate_ali/nb_img
    frate_baidu=frate_baidu/nb_img
    frate_huawei=frate_huawei/nb_img
    frate_xunfei=frate_xunfei/nb_img
    frate_yidao=frate_yidao/nb_img
    frate_ruiqi=frate_ruiqi/nb_img
    tmp="TOTAL,,,,,,,,,,,,,,"+calcPercent(frate_ali)+","+calcPercent(frate_baidu)+","+calcPercent(frate_huawei)+","+calcPercent(frate_xunfei)+","+calcPercent(frate_yidao)+","+calcPercent(frate_ruiqi)
    foutput.write(tmp.encode())
    foutput.close()
    t.close()
    
    compFunc.readDict(compFunc.dict_ziduan,rootdir_result+re.sub("../","",motherdir)+"_ziduan.csv")
    #print(compFunc.dict_ziduan)
################################################################################
#######################  Move Data  ############################################
################################################################################
def moveAnswer():
    for parent,dirnames,filenames in os.walk("../primitive_answer"):
        for filename in filenames:
            shutil.move("../primitive_answer/"+filename, rootdir_prmanswer)
def moveData():
    for parent,dirnames,filenames in os.walk("../cache"):
        for filename in filenames:
            shutil.move("../cache/"+filename, rootdir_data)
def defineGlobal(parsedir):
    global motherdir,rootdir_answer,rootdir_prmanswer,rootdir_data,rootdir_tested,rootdir_bad,rootdir_result,rootdir_info,rootdir_invalidjson
    motherdir=parsedir
    
    rootdir_answer,rootdir_prmanswer,rootdir_data,rootdir_tested,rootdir_bad,rootdir_result,rootdir_info,rootdir_invalidjson=mknewdir.joinDir(motherdir)
    
    try:
        mknewdir.mktree(motherdir)
    except FileExistsError:
        print(motherdir+" already created")
    
      
################################################################################
#######################  M A I N  ##############################################
################################################################################
if __name__=="__main__":
    arglength=len(sys.argv)
    fhelp=open(rootdir_info+"helptxt","r")
    helptext=str(fhelp.read())
    warntext="Invalid Usage: use 'fakemain.py -help' to get help\n无效参数：请使用'fakemain.py -help'以获取使用帮助"
    parser=argparse.ArgumentParser()
    parser.add_argument('servicetype',type=str,help='选择一种服务类型: \n'+helptext)
    parser.add_argument('-d','--directory',type=str,default='../default_rootdir',help='输入一个根目录，默认放在../default_rootdir')
       
    args=parser.parse_args()
    stype=args.servicetype
    pdir=args.directory
    print(pdir)
    
    defineGlobal(pdir)
    
    if(stype=='callapi'):
        moveData()
        callAPI(rootdir_data)
    elif(stype=='compare'):
        #compFunc.validateJSON(rootdir_result+"_baidu/",rootdir_invalidjson,"_baidu",compFunc.startjson_baidu)
        compall()
    elif(stype=='transdata'):
        moveAnswer()
        selfConvert.convert_alljson(rootdir_prmanswer,rootdir_answer)
    elif(stype=='all'):
        moveAnswer()
        moveData()           
        selfConvert.convert_alljson(rootdir_prmanswer,rootdir_answer)
        callAPI(rootdir_data)
        #compFunc.validateJSON(rootdir_result+"_baidu/",rootdir_invalidjson,"_baidu",compFunc.startjson_baidu)
        compall()
    else:
        print(warntext)
   
    fhelp.close()
