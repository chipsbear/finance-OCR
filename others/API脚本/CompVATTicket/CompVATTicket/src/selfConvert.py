import json
import os
import chardet
#rootdir_old_filepath='./primitive_answer/'
#rootdir_new_filepath='./answer/'
ENCODING_TXT='utf-8'
def convert_json(old_filename,rootdir_old_filepath,rootdir_new_filepath):
    newindex=0
    newdata={'templateFields':{}}
    with open(rootdir_old_filepath+old_filename,"r",encoding='utf-8') as f:
        '''
        source_encoding_list=chardet.detect(f.read())
        source_encoding=source_encoding_list['encoding']
        if source_encoding==None:
            print("cannot detect")
            print(old_filename)
        else:
            print(source_encoding)
        '''
        try:
            data = json.load(f,strict=False)
        except UnicodeDecodeError:
            print(old_filename," cannot be loaded as a json. Please check if its coding format is utf-8.")
            f.close()
            return
        else:
            for i in data['templateFields']:
                newdata['templateFields'][i['templateFieldNo']]=""
                if('content' in i):
                    newdata['templateFields'][i['templateFieldNo']]=(i['content']['word'])
        
            f.close()    
    
    fname=old_filename.split('.')
    fname=fname[0].split('_')
    fh=open(rootdir_new_filepath+fname[0]+".json","w")
    newdata=json.dumps(newdata)
    fh.write(str(newdata))
    fh.close()
    
    #return filepath
    
def convert_oneyidao(old_filename,rootdir_old_filepath,rootdir_new_filepath):
    newindex=0
    newdata={'output':{}}
    with open(rootdir_old_filepath+old_filename,"r") as f:
        '''
        source_encoding_list=chardet.detect(f.read())
        source_encoding=source_encoding_list['encoding']
        if source_encoding==None:
            print("cannot detect")
            print(old_filename)
        else:
            print(source_encoding)
        '''
        try:
            data = json.load(f)
        except UnicodeDecodeError:
            print(old_filename," cannot be loaded as a json. Please check if its coding format is utf-8.")
            f.close()
            return
        
        else:
            newdata['error_code']=data['error_code']
            
            if(data['error_code']==0):
                for i in data['output'].keys():
                    newdata['output'][i]=data['output'][i]['words']
            else:
                print(old_filename)
                newdata['output']={}
                
            f.close()    
    
    fname=old_filename.split('.')
    fname=fname[0].split('_')
    fh=open(rootdir_new_filepath+fname[0]+".json","w")
    newdata=json.dumps(newdata)
    fh.write(str(newdata))
    fh.close()

def convert_oneruiqi(old_filename,rootdir_old_filepath,rootdir_new_filepath):
    newindex=0
    newdata={'output':{}}
    with open(rootdir_old_filepath+old_filename,"r") as f:
        try:
            d = f.read()
            d1 = d.replace("'", '"')
            data = json.loads(d1)
            print('ok')
        except UnicodeDecodeError:
            print(old_filename," cannot be loaded as a json. Please check if its coding format is utf-8.")
            f.close()
            return
        
        else:
            newdata['error_code']=data['output']
            
            if(data['output']==1):
                for i in data['response']['cache']['identify_results'][0]['details'].keys():
                    newdata['output'][i]=data['response']['cache']['identify_results'][0]['details'][i]
                print(newdata)
            else:
                print(old_filename)
                newdata['output']={}
                
            f.close()    
    
    fname=old_filename.split('.')
    fname=fname[0].split('_')
    fh=open(rootdir_new_filepath+fname[0]+".json","w")
    newdata=json.dumps(newdata)
    print(newdata)
    fh.write(str(newdata))
    fh.close()

def convert_allyidao(directory,dst):
    for parent,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            #print(filename)
            convert_oneyidao(filename,directory,dst)

def convert_allruiqi(direc,ds):
    for parent,dirnames,filenames in os.walk(direc):
        for filename in filenames:
            #print(filename)
            convert_oneruiqi(filename,direc,ds)

def convert_alljson(directory='./primitive_answer/',dst='./answer/'):
    for parent,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            convert_json(filename,directory,dst)
    print("All files in "+directory+" is parsed.")
    
#convert_allyidao("../Jan2019_benchmark300_scan/output/yidao/","../Jan2019_benchmark300_scan/output/yidaonew/")