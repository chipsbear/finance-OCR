import re
def need_treat(func,content,start,itemword,itemanswer):
    if(itemword=='NotAvailable'):
        return -1
    else:
        condition=0
        if("Amount" in itemanswer):
            condition=1
        return func(content,start,itemword,condition)

def treat_goods_huawei(content,start,itemword,condition):
#应该处理一下虽然有字段但内容为空的情况 ，直接返回None   
    if("item_list" not in content[start].keys()):
        return None
    else:
        goods=content[start]["item_list"]        
        if(len(goods)==0):#完全没有item则返回没有
            return None
        tmp=[]
        for i in goods:
            if(itemword not in i.keys()):#华为不会出现这种情况
                return None
            tmp.append(subSpace(i[itemword],condition))
        return tmp
def treat_goods_answer(content,start,itemword,condition):
    #it's already judged if the answer exists in content_answer and not null, so no need to judge it here    
    tmp=content[start][itemword]
    tmp=tmp.split("$__$")
    tmpreturn=[]
    for i in tmp:
        i=subSpace(i,condition)
        tmpreturn.append(i)
    
    return tmpreturn
def treat_goods_baidu(content,start,itemword,condition):
    if(itemword not in content[start].keys()):
        return None
    else:
        goods=content[start][itemword]
        if(goods==[]):#对应的列表是空的
            return None
        tmp={}        
        for i in goods:
            tmp[int(i["row"])-1]=subSpace(i["word"],condition)
            #print(type(tmp[int(i["row"])-1]))
        #print(tmp)
        return tmp
def treat_goods_xunfei(content,start,itemword,condition):
    if(itemword not in content[start].keys()):
        return None
    else:
        tmp=content[start][itemword]
        if(tmp==""):#对应的字段是空的
            return None
        tmp=tmp.split("\n")
        tmpreturn=[]
        for i in tmp:
            i=subSpace(i,condition)
            tmpreturn.append(i)
        return tmpreturn

def subSpace(string,condition):
    try:
        string=re.sub(" ","",string)
        
    except TypeError:
        return 0
    if(condition):
        string=re.sub("￥","",string)
        string=re.sub("¥","",string)
        if(string!=""):
            try:
                string=float(string)
            except ValueError:
                #print ("invalid money format\n")
                string=0
    return string
    
#def compGoodsSeparate(compname,goods,goods_answer):
#    length=len(min(len(goods),len(goods_answer)))
#    for i in range(0,length):
#        if(goods[i]==goods_answer[i]):
            
        
    