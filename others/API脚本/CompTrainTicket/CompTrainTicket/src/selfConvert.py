import json
import os
import chardet
import re
#rootdir_old_filepath='./primitive_answer/'
#rootdir_new_filepath='./answer/'
ENCODING_TXT='utf-8'
def convert_json(old_filename,rootdir_old_filepath,rootdir_new_filepath):
    newindex=0
    newdata={'templateFields':{}}
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
def convert_alljson(directory='./primitive_answer/',dst='./answer/'):
    for parent,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            convert_json(filename,directory,dst)
    print("All files in "+directory+" is parsed.")
    
def convert_ali(rootdir_result,newname):
    rootdir_aliresult=rootdir_result+"ali/"
    rootdir_alinewresult=rootdir_result+newname
    try:
        os.makedirs(rootdir_alinewresult)
    except:
        print("Alinew already exists")
    for parent,dirnames,filenames in os.walk(rootdir_aliresult):
        for filename in filenames:
            convert_oneali(filename,rootdir_aliresult,rootdir_alinewresult)
            
    os.rename(rootdir_aliresult,rootdir_result+"aliold")
    os.rename(rootdir_alinewresult,rootdir_result+"ali")
def convert_oneali(filename,rootdir_old_filepath,rootdir_new_filepath):
    print(filename)
    newdata={'cache':{}}
    with open(rootdir_old_filepath+filename,"r") as f:
        try:
            data = json.load(f)
        except UnicodeDecodeError:
            print(filename," cannot be loaded as a json. Please check if its coding format is utf-8.")
            f.close()
            return
        else:
            newdata['cache']=data
        
            
    for i in newdata['cache'].keys():
        if (i=='date'):
            #print(newdata['cache']['date'])
            date=newdata['cache']['date'][0:11]
            time=re.sub(date,"",newdata['cache']['date'])
            newdata['cache']['date']=date
            newdata['cache']['time']=time
            break
            
    fh=open(rootdir_new_filepath+filename,"w")
    newdata=json.dumps(newdata)
    fh.write(str(newdata))
    fh.close()
    f.close()

#convert_ali("./06train/output/","haha/")

def convert_oneruiqi(old_filename,rootdir_old_filepath,rootdir_new_filepath):
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
                    if i == 'station_geton' or i =='station_getoff':
                        newdata['output'][i] = data['response']['cache']['identify_results'][0]['details'][i]+'站'
                    else:
                        newdata['output'][i]=data['response']['cache']['identify_results'][0]['details'][i]
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
def convert_allruiqi(directory,dst):
    for parent,dirnames,filenames in os.walk(directory):
        for filename in filenames:
            #print(filename)
            convert_oneruiqi(filename,directory,dst)  
    
