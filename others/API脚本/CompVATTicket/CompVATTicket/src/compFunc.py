import time,datetime
import re
import json
import os
import csv
import goodsFunc
import shutil
from collections import namedtuple
import json 
import math 
import os 
import io 
import requests 
import time 
import datetime 
import hashlib 
import codecs 
import uuid 
import traceback 

ENCODING_JSON='utf-8'
ENCODING_CSV='gbk'
################################################################################
#####################  GLOBAL VARIABLES  #######################################
################################################################################
#indicate the NO.col in csv img
col_ali=3
col_baidu=2
col_huawei=4
col_answer=7
col_xunfei=5
col_yidao=6
col_ruiqi = 8

#indicate the first level in API's return json
startjson_ali='cache'
startjson_baidu='words_result'
startjson_huawei='output'
startjson_xunfei='cache'
startjson_answer='templateFields'
startjson_yidao='output'
startjson_ruiqi = 'output'

goodslist=["ItemContent","ItemStandard","ItemUnit","ItemQuantity","ItemUnitAmount","ItemAmount","ItemTaxAmount","TaxRate"]
namelist=["ali","_baidu","huawei_ocr","xunfei","yidao","ruiqi"]
sumsymbol=["\n","(",")",",","，","（","）"]
ferror=open("../log/errlog.csv","wb")
path_CSV="../csv/refnew_all.csv" 
dict_ziduan={}

################################################################################
##################### SMALL FUNCTION BELOW  ####################################
################################################################################
def writeLog(words,error):
    localtime = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    ferror.write((localtime+" "+str(error)+" "+words).encode())
    
    
def calcPercent(num):
    return str('%.2f%%' % (num * 100))

def readDict(dictionary,filepath):
    fziduan=open(filepath,"wb")
    s="name_ziduan,nb_good_ali,nb_good_baidu,nb_good_huawei,nb_good_xunfei,nb_good_yidao,nb_good_ruiqi,nb_all_tested,rate_ali,rate_baidu,rate_huawei,rate_xunfei,rate_yidao,rate_ruiqi\n"
    fziduan.write(s.encode())
    for i in dictionary.keys():
        nb_all=dictionary[i]["all"]
        s=i+","+str(dictionary[i]["ali"])+","+str(dictionary[i]["_baidu"])+","+str(dictionary[i]["huawei_ocr"])\
        +","+str(dictionary[i]["xunfei"])+","+str(dictionary[i]["yidao"])+","+str(dictionary[i]["ruiqi"])+","+str(dictionary[i]["all"])+","
        
        t=""
        for j in namelist:
            if(dictionary[i][j]=='NA'):
                t+="NA,"
            else:
                try:
                    t+=(calcPercent(dictionary[i][j]/nb_all)+",")
                except ZeroDivisionError:
                    t+="0,"
        #t=calcPercent(dictionary[i]["ali"]/nb_all)+","+calcPercent(dictionary[i]["_baidu"]/nb_all)+","+calcPercent(dictionary[i]["huawei_ocr"]/nb_all)+","+calcPercent(dictionary[i]["xunfei"]/nb_all)+"\n"
        
        fziduan.write(s.encode())
        fziduan.write(t.encode())
        fziduan.write(("\n").encode())
def buildDict():
    global dict_ziduan
    fref=open(path_CSV,encoding=ENCODING_JSON,errors='ignore')  
    reader=csv.reader(fref,delimiter=',',dialect='excel')    
    title=next(reader)
    ROW=namedtuple('ROW',title)
    for row in reader:
        row=ROW(*row)
        dict_ziduan[row[col_answer]]={"ali":0,"_baidu":0,"huawei_ocr":0,"xunfei":0,"yidao":0,"ruiqi":0,"all":0}
    print('1',row)
    fref.close()

def compFileSeparate(compname,content,row,startjson,col_content,ans):
    global dict_ziduan   
    #进行一波预处理
    #把答案和api输出中的语义为“日期”的转换成yyyymmdd格式
    if('Date' in row[col_answer]):
        if(row[col_content] in content[startjson]):
                content[startjson][row[col_content]]=transDate(content[startjson][row[col_content]],"%Y年%m月%d日")
    #把答案和api输出中的语义为“钱”的转换成浮点数
    if('Total' in row[col_answer] and ('Cap' not in row[col_answer])):
        repAmountbyline(content,row,col_content,startjson)
    #如果本字段出现在了返回的文件中且类型为Str
    if(row[col_content] in content[startjson].keys()):    
        if(isinstance(content[startjson][row[col_content]],str)):
        #把result去空格               
            content[startjson][row[col_content]]=re.sub(" ", "", content[startjson][row[col_content]])
    
    tmpr=compLine(compname,row,col_content,content,startjson,ans)
    if(tmpr==-1):
        dict_ziduan[row[col_answer]][compname]='NA'
        tmpr=0
        r=0
    else:
        dict_ziduan[row[col_answer]][compname]+=tmpr
        r=1
    return tmpr,r
    
def modifyResult(r,valid,t):
    r+=t[0]
    valid+=t[1]
    return r,valid

def compGoods(compname,itemanswer,ganswer,gresult):
    #print(compname)
    global dict_ziduan
    if(gresult==-1):#本货物字段从不被这个公司返回
        dict_ziduan[itemanswer][compname]='NA'
        tmpr=0
        r=0
        
    elif(gresult==None):#字段本应返回却没有返回
        tmpr=0
        dict_ziduan[itemanswer][compname]+=0
        r=len(ganswer)
    else:#字段返回了，那么就需要对这个字段做比较
        length=min(len(ganswer),len(gresult))
        r=len(gresult)
        tmpr=0
        for i in range(0,length):
            tmpr+=compAnswer(gresult[i],ganswer[i])
        
        dict_ziduan[itemanswer][compname]+=tmpr
    return tmpr,r
def regSummary(string):
    string=re.sub("，",",",string)
    string=re.sub("（","(",string)
    string=re.sub("）",")",string)
    string=re.sub("\n","",string)
    string=re.sub("$__$","",string)
    return string
def replaceinvoice(row,canswer):   
    if(row[col_answer]+'2' in canswer[startjson_answer] and canswer[startjson_answer][row[col_answer]+'2']!=""):
        return(row[col_answer]+'2',1)              
    else:
        return (row[col_answer],0)
    
def compFile(cali,cbaidu,chuawei,cxunfei,cyidao,cruiqi,canswer):
    #r系列的变量代表针对本张发票，竞品公司理应存在的字段数量（除去NotAvailable字段，除去标注答案本身也为空或不存在的字段）
    rbaidu=0
    rali=0
    rhuawei=0
    rxunfei=0
    ryidao=0
    rcomp=0
    rruiqi=0
    #v系列变量代表针对本张发票，竞品公司比对成功的字段数量（与标注答案一致）
    valid_baidu=0
    valid_ali=0
    valid_huawei=0
    valid_xunfei=0
    valid_yidao=0
    valid_ruiqi=0
    
    global dict_ziduan
    #打开refnew_all
    fref=open(path_CSV,encoding=ENCODING_JSON,errors='ignore') 
        
    reader=csv.reader(fref,delimiter=',',dialect='excel')    
    title=next(reader)
    ROW=namedtuple('ROW',title)
    #循环内即对每一个理应存在的字段进行比较，“理应存在”的标准在refnew_all中，如果在各公司返回的json文件中不存在“理应存在”的字段
    #有可能是该字段在发票中并未被检测到（确实为空，或者由于技术所限没有检测到）。当确实为空时，意味着标注答案中不会存在相应字段或者相应字段为空，
    #那么就应该跳过这个字段的比较。而答案不为空，就意味着竞品公司在这张图片上检测这个字段失败，准确率不会得到上涨。
    for row in reader:
        row=ROW(*row)
        print(row)
        answertitle=row[col_answer]
        
        #如果预计答案字段没出现在答案文件中或出现了但值为空时，跳过该字段：故而不会出现答案空值与其他有值的比较
        #以下这个if是由于我司提供的标注并不完善，InvoiceCode和InvoiceNo有时会出现在InvoiceCode2和InvoiceNo2字段中。
        #那么就需要去2里找答案
        if (row[col_answer] in canswer[startjson_answer]):            
            if(canswer[startjson_answer][row[col_answer]]==""):
                #print(row[col_answer])
                if(row[col_answer]=='InvoiceCode' or row[col_answer]=='InvoiceNO'):
                    answertitle,flag=replaceinvoice(row,canswer)
                    if (flag==0):            
                        ferror.write((','+row[col_answer]).encode())
                        continue
                        
                else:
                    ferror.write((','+row[col_answer]).encode())
                    continue
                    
        else:
            #print(row[col_answer])
            if(row[col_answer]=='InvoiceCode' or row[col_answer]=='InvoiceNO'):
                answertitle,flag=replaceinvoice(row,canswer) 
                if (flag==0):            
                    ferror.write((','+row[col_answer]).encode())
                    continue
            else:
                ferror.write((','+row[col_answer]).encode())
                continue
        
        canswer[startjson_answer][answertitle]=re.sub(" ","",canswer[startjson_answer][answertitle])
        #######开始区分答案的内容#######
        #这是和数额有关的字段，因为各家json有的返回￥/不返回￥，有的用浮点数/字符串，所以比较时一定要做统一处理
        if(('Total' in row[col_answer]) and ('Cap' not in row[col_answer])):        
            if(canswer[startjson_answer][row[col_answer]]!=""):
                canswer[startjson_answer][row[col_answer]]=re.sub('￥',"",canswer[startjson_answer][row[col_answer]])
                try:
                    canswer[startjson_answer][row[col_answer]]=float(canswer[startjson_answer][row[col_answer]])
                except ValueError:
                    writeLog(row[col_answer]+" answer is invalid money",ValueError)
                    print(row[col_answer])
                    ferror.write((','+row[col_answer]).encode())
                    continue
        
        if(row[col_answer]=="Summary"):           
            canswer[startjson_answer][row[col_answer]]=regSummary(canswer[startjson_answer][row[col_answer]])
            
            
        #print(row[col_answer])
        #货物字段
        if(row[col_answer] in goodslist):                       
            #这一块是比较烦的一段。有空当面讲吧。
            #主要由于各公司返回地货物字段json格式不一
            goods_answer=goodsFunc.need_treat(goodsFunc.treat_goods_answer,canswer,startjson_answer,row[col_answer],row[col_answer])
            goods_huawei=goodsFunc.need_treat(goodsFunc.treat_goods_huawei,chuawei,startjson_huawei,row[col_huawei],row[col_answer])
            goods_baidu=goodsFunc.need_treat(goodsFunc.treat_goods_baidu,cbaidu,startjson_baidu,row[col_baidu],row[col_answer])
            goods_xunfei=goodsFunc.need_treat(goodsFunc.treat_goods_xunfei,cxunfei,startjson_xunfei,row[col_xunfei],row[col_answer])
            goods_ali=-1
            goods_yidao=-1
            goods_ruiqi=-1
            
            rbaidu,valid_baidu=modifyResult(rbaidu,valid_baidu,compGoods("_baidu",row[col_answer],goods_answer,goods_baidu))
            rhuawei,valid_huawei=modifyResult(rhuawei,valid_huawei,compGoods("huawei_ocr",row[col_answer],goods_answer,goods_huawei))
            rxunfei,valid_xunfei=modifyResult(rxunfei,valid_xunfei,compGoods("xunfei",row[col_answer],goods_answer,goods_xunfei))
            ryidao,valid_yidao=modifyResult(ryidao,valid_yidao,compGoods("yidao",row[col_answer],goods_answer,goods_yidao))         
            rali,valid_ali=modifyResult(rali,valid_ali,compGoods("ali",row[col_answer],goods_answer,goods_ali))
            rruiqi,valid_ruiqi=modifyResult(rruiqi,valid_ruiqi,compGoods("ruiqi",row[col_answer],goods_answer,goods_ruiqi))
            rcomp+=len(goods_answer)
            dict_ziduan[row[col_answer]]['all']+=len(goods_answer)
            continue
                
        #普通共有字段
        dict_ziduan[row[col_answer]]['all']+=1
        rcomp+=1
        ans=canswer[startjson_answer][answertitle]
        #if(row[col_answer]=="Summary"):
            #print(ans)
#         print(row)
        rbaidu,valid_baidu=modifyResult(rbaidu,valid_baidu,compFileSeparate('_baidu',cbaidu,row,startjson_baidu,col_baidu,ans))
        rali,valid_ali=modifyResult(rali,valid_ali,compFileSeparate('ali',cali,row,startjson_ali,col_ali,ans))      
        rhuawei,valid_huawei=modifyResult(rhuawei,valid_huawei,compFileSeparate('huawei_ocr',chuawei,row,startjson_huawei,col_huawei,ans))
        rxunfei,valid_xunfei=modifyResult(rxunfei,valid_xunfei,compFileSeparate('xunfei',cxunfei,row,startjson_xunfei,col_xunfei,ans))
        
        ryidao,valid_yidao=modifyResult(ryidao,valid_yidao,compFileSeparate('yidao',cyidao,row,startjson_yidao,col_yidao,ans))
        rruiqi,valid_ruiqi=modifyResult(rruiqi,valid_ruiqi,compFileSeparate('ruiqi',cruiqi,row,startjson_ruiqi,col_ruiqi,ans))
        #print('\n')
    #print(rali,rbaidu,rhuawei,rxunfei,valid_ali,valid_baidu,valid_huawei,valid_xunfei,rcomp)        
    fref.close()  
    
    return (rali,rbaidu,rhuawei,rxunfei,ryidao,rruiqi,valid_ali,valid_baidu,valid_huawei,valid_xunfei,valid_yidao,valid_ruiqi,rcomp)

def prepData(directory,compname,singlename,encoding):
    fpath=directory+compname+"/"+singlename+".json"
    try:
        f=open(fpath,encoding=ENCODING_JSON)
    except FileNotFoundError:
        f=open(directory+compname+"/blank.json")
    
    content=json.load(f)
    f.close()    
    return content


def compLine(compname,row,col,content,start,answerLine):
    s=row[col]
    #如果csv中没有对应的条目则跳过，有对应条目则去判断当前api返回的结果中有没有该条目（如百度返回不定数量的条目）
    if(s=='NotAvailable'):
        return -1;
    if(s!=''):
        if(s in content[start].keys()):
            #print(compname,content[start][s])
            #print(compname)
            #如果比较的字段是VCODE
            #if(row[col_answer]=="VCode"):
            #    a=content[start][s]
            #    tmpl=len(a)
            #    content[start][s]=a[tmpl-10:tmpl]
            if(row[col_answer]=="Summary"):
                content[start][s]=regSummary(content[start][s])
                #print(content[start][s],"summary========",answerLine)
            return compAnswer(content[start][s],answerLine)
        else:
            return 0
    else:
        return 0
def compAnswer(resultLine,answer):
    if(resultLine==answer):
        #equal to correct answer
        return 1
    else:
        #not equal to correct answer        
        #print(resultLine,answer,type(resultLine),type(answer),"not equal")
        return 0

def transDate(stro,stro_format):
    if(stro==""):
        return stro
    try:
        t = time.strptime(stro, stro_format)
    except ValueError:
        #writeLog("invalid date format",ValueError)
        return("")
    else:
        y,m,d=t[0:3]
    
        if(m>=10):
            m=str(m)
        else:
            m="0"+str(m)
    
        if(d>=10):
            d=str(d)
        else:
            d="0"+str(d)    
        
        y=str(y)
   
        return(str(y+m+d))    
    
    
def repAmountbyline(content,row,num,start):
       if(row[num]!='' and (row[num] in content[start].keys())):
            content[start][row[num]]=re.sub("￥","",content[start][row[num]])
            content[start][row[num]]=re.sub("¥","",content[start][row[num]])
            if(content[start][row[num]]!=""):
                try:
                    content[start][row[num]]=float(content[start][row[num]])
                except ValueError:
                    #print ("invalid money format\n")
                    writeLog(content[start][row[num]]+" is invalid money format",ValueError)
                    content[start][row[num]]=0
                    