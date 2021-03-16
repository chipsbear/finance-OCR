import os
import shutil
import testFunc
import tokenFunc
import compFunc
import json
permit=3
rootdir_blankjson='../blankjson/'
def putBlankJSON(dstdir,compname,srcdir=rootdir_blankjson):
    try:
        shutil.copyfile(srcdir+compname+"/blank.json",dstdir+compname+"/blank.json")
    except shutil.Error:
        pass
def validateJSON(directory,dirinvalid,compname,start):
    if(compname=="_baidu"):
        for parent,dirnames,filenames in os.walk(directory):
            for filename in filenames:
                fileop=open(directory+filename,encoding='utf-8')
                filecontent=json.load(fileop)
                if(start not in filecontent.keys()):
                    try:
                        shutil.move(directory+filename, dirinvalid+compname)
                    except shutil.Error:
                        os.remove(directory+filename)
    elif(compname=="xunfei"):
        for parent,dirnames,filenames in os.walk(directory):
            for filename in filenames:
                fileop=open(directory+filename,encoding='utf-8')
                filecontent=json.load(fileop)
                if(filecontent["code"]!="0"):
                    try:
                        shutil.move(directory+filename, dirinvalid+compname)
                    except shutil.Error:
                        os.remove(directory+filename)
        
    else:
        pass
def retest(badjson_dir,tested_dir,data_dir,func,dict_args):
    global permit
    comppath=dict_args['compname']+'/'
    path_result=dict_args['rootdir_result']+comppath
    
    
    validateJSON(path_result,badjson_dir,dict_args['compname'],compFunc.startjson_baidu)
    
    if(os.listdir(badjson_dir+comppath)==[]):
        print("no bad json!")
        permit=3
        return
    elif(permit<=0):
        print("you don't have any chance to rerun") 
        permit=3
        return
    else:
        print(permit," time")
        permit-=1
        for parent,dirnames,filenames in os.walk(badjson_dir+comppath):
            for filename in filenames:
                #print(badjson_dir+comppath+filename)
                singlename=filename.split('.')
                singlename=singlename[0]+'.jpg'
                try:
                    shutil.move(tested_dir+singlename, data_dir)
                except shutil.Error:
                    pass
                except FileNotFoundError:#可能对应的图片在bad中,这种情况不需要再测这张图了，说明不合格式，这个json就不用管了
                    pass
                os.remove(badjson_dir+comppath+filename)

        for parent,dirnames,filenames in os.walk(data_dir):
            for filename in filenames:
                try:
                    func(filename,data_dir,dict_args['rootdir_result'],dict_args['token'])
                    shutil.move(data_dir+filename,tested_dir+filename)
                except FileNotFoundError:#不可能发生
                    pass
                except shutil.Error:#可能部分发生
                    pass
        return retest(badjson_dir,tested_dir,data_dir,func,dict_args)
#validateJSON('./benchmark300_scan/output/xunfei/',"./benchmark300_scan/invalidjson/",'xunfei',compFunc.startjson_xunfei)
#putBlankJSON(dstdir="./benchmark300_scan/output/",compname='xunfei')