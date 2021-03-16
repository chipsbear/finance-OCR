import time,datetime
import re
import json
import os
import csv
import goodsFunc
import shutil
from collections import namedtuple
ENCODING_JSON='utf-8'
ENCODING_CSV='gbk'
################################################################################
#####################  GLOBAL VARIABLES  #######################################
################################################################################
#indicate the NO.col in csv img
col_ali=3
col_baidu=2
#col_huawei=4
col_answer=4
col_ruiqi=5
#col_xunfei=5
#indicate the first level in API's return json
startjson_ali='cache'
startjson_baidu='words_result'
#startjson_huawei='output'
#startjson_xunfei='cache'
startjson_answer='templateFields'
startjson_ruiqi = 'output'
#goodslist=["ItemContent","ItemStandard","ItemUnit","ItemQuantity","ItemUnitAmount","ItemAmount","ItemTaxAmount","TaxRate"]
namelist=["ali","_baidu","ruiqi"]
sumsymbol=["\n","(",")",",","，","（","）"]
ferror=open("../log/errlog.csv","wb")
ferror_answer=open("../log/err_answer.csv","wb")
path_CSV="../csv/ref_train.csv"

dict_ziduan={}

################################################################################
##################### SMALL FUNCTION BELOW  ####################################
################################################################################
def alidate_ConvertOne(old_filename,rootdir_old_filepath,rootdir_new_filepath):
    newdata={}
    with open(rootdir_old_filepath+old_filename,"r") as f:
        try:
            data = json.load(f)
        except UnicodeDecodeError:
            print(old_filename," cannot be loaded as a json. Please check if its coding format is utf-8.")
            f.close()
            return
        else:
            if("date" in data.keys()):    
                datetime=data['date']
                print(datetime)
                

def writeLog(words,error):
    localtime = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    ferror.write((localtime+" "+str(error)+" "+words).encode())
    
    
def calcPercent(num):
    return str('%.2f%%' % (num * 100))

def readDict(dictionary,filepath):
    fziduan=open(filepath,"wb")
    s="name_ziduan,nb_good_ali,nb_good_baidu,nb_good_ruiqi,nb_all_tested,rate_ali,rate_baidu,rate_ruiqi\n"
    fziduan.write(s.encode())
    for i in dictionary.keys():
        nb_all=dictionary[i]["all"]
        s=i+","+str(dictionary[i]["ali"])+","+str(dictionary[i]["_baidu"])+","+str(dictionary[i]["ruiqi"])+","+str(dictionary[i]["all"])+","
        
        t=""
        for j in namelist:
            if(dictionary[i][j]=='NA'):
                t+="NA,"
            else:
                try:
                    t+=(calcPercent(dictionary[i][j]/nb_all)+",")
                except ZeroDivisionError:
                    t+="0,"
        fziduan.write(s.encode())
        fziduan.write(t.encode())
        fziduan.write(("\n").encode())
def buildDict():
    global dict_ziduan
    fref=open(path_CSV,encoding=ENCODING_CSV,errors='ignore') 
        
    reader=csv.reader(fref,delimiter=',',dialect='excel')    
    title=next(reader)
    ROW=namedtuple('ROW',title)
    for row in reader:
        row=ROW(*row)
        dict_ziduan[row[col_answer]]={"ali":0,"_baidu":0,"huawei_ocr":0,"xunfei":0,"ruiqi":0,"all":0}
    fref.close()

def compFileSeparate(compname,content,row,startjson,col_content,ans):
    global dict_ziduan   
    #进行一波预处理
    #把答案和api输出中的语义为“日期”的转换成yyyymmdd格式
    if('Date' in row[col_answer]):
        if(row[col_content] in content[startjson]):
                content[startjson][row[col_content]]=transDate(content[startjson][row[col_content]],"%Y年%m月%d日")
    #如果本字段出现在了返回的文件中且类型为Str
    if(row[col_content] in content[startjson].keys()):    
        if(isinstance(content[startjson][row[col_content]],str)):
        #把result去空格               
            content[startjson][row[col_content]]=re.sub(" ", "", content[startjson][row[col_content]])
    #把答案和api输出中的语义为“钱”的转换成浮点数
    if(row[col_answer]=='TotalAmount'):
        #print("money here")
        repAmountbyline(content,row,col_content,startjson)
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
    
def compFile(cali,cbaidu,cruiqi,canswer):
    rbaidu=0
    rali=0
    rruiqi =0
    #rhuawei=0
    #rxunfei=0
    rcomp=0
    valid_baidu=0
    valid_ali=0
    valid_ruiqi = 0
    #valid_huawei=0
    #valid_xunfei=0
    
    global dict_ziduan
    fref=open(path_CSV,encoding=ENCODING_CSV,errors='ignore')     
    reader=csv.reader(fref,delimiter=',',dialect='excel')    
    title=next(reader)
    ROW=namedtuple('ROW',title)
    
    for row in reader:
        row=ROW(*row)
        answertitle=row[col_answer]
        
        #如果预计答案字段没出现在答案文件中或出现了但值为空时，跳过该字段：故而不会出现答案空值与其他有值的比较
        if (row[col_answer] in canswer[startjson_answer]):            
            if(canswer[startjson_answer][row[col_answer]]==""):
                ferror.write(",#".encode())
                ferror.write(row[col_answer].encode())
                continue
        else:
            ferror.write(",#".encode())
            ferror.write(row[col_answer].encode())
            continue
        
        canswer[startjson_answer][answertitle]=re.sub(" ","",canswer[startjson_answer][answertitle])
        #######开始区分答案的内容#######     
        if(row[col_answer]=='TotalAmount'):
        
            repAmountbyline(canswer,row,col_answer,startjson_answer)
        
                
        #普通共有字段
        dict_ziduan[row[col_answer]]['all']+=1
        rcomp+=1
        ans=canswer[startjson_answer][answertitle]
        #if(row[col_answer]=="Summary"):
            #print(ans)
        tbaidu=compFileSeparate('_baidu',cbaidu,row,startjson_baidu,col_baidu,ans)
        tali=compFileSeparate('ali',cali,row,startjson_ali,col_ali,ans)
        truiqi=compFileSeparate('ruiqi',cruiqi,row,startjson_ruiqi,col_ruiqi,ans)
        #print(tbaidu,tali)
        if(tbaidu==(0,1) and tali==(0,1) and truiqi==(0,1)):
            ferror_answer.write(",*".encode())
            ferror_answer.write(row[col_answer].encode())
            print("might be wrong with answer")
        
        rbaidu,valid_baidu=modifyResult(rbaidu,valid_baidu,tbaidu)
        print(rali,valid_ali,tali) 
        rali,valid_ali=modifyResult(rali,valid_ali,tali) 

        rruiqi,valid_ruiqi=modifyResult(rruiqi,valid_ruiqi,truiqi)      
        
        #rhuawei,valid_huawei=modifyResult(rhuawei,valid_huawei,compFileSeparate('huawei_ocr',chuawei,row,startjson_huawei,col_huawei,ans))
        #rxunfei,valid_xunfei=modifyResult(rxunfei,valid_xunfei,compFileSeparate('xunfei',cxunfei,row,startjson_xunfei,col_xunfei,ans))    
        #print('\n')
    #print(rali,rbaidu,rhuawei,rxunfei,valid_ali,valid_baidu,valid_huawei,valid_xunfei,rcomp)        
    fref.close()  
    ferror_answer.write("\n".encode())
    return (rali,rbaidu,rruiqi,valid_ali,valid_baidu,valid_ruiqi,rcomp)

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
        if not(isinstance(content[start][row[num]],str)):
            #print(content[start][row[num]],"i'm not string")
            return
           
        content[start][row[num]]=re.sub("￥","",content[start][row[num]])
        content[start][row[num]]=re.sub("元","",content[start][row[num]])
        if(content[start][row[num]]!=""):
            try:
                #print("i convert::",content[start][row[num]])
                content[start][row[num]]=float(content[start][row[num]])
            except ValueError:
                #print ("invalid money format\n")
                #writeLog(content[start][row[num]]+" is invalid money format",ValueError)
                content[start][row[num]]=0
                    
