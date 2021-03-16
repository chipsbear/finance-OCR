import os
subdir=["/answer","/bad","/output","/tested","/cache","/invalidjson","/primitive_answer","/log"]
compname=["/ali","/_baidu","/huawei_ocr","/xunfei","/ruiqi"]


def mktree(string):
    for i in subdir:
        os.makedirs(string+i)
        if(i=="/output" or i=="/invalidjson"):
            for j in compname:
                os.makedirs(string+i+j)
    
#mktree("./benchmark300")
def joinDir(motherdir):
    rootdir_answer = motherdir+"/answer/"
    rootdir_prmanswer=motherdir+"/primitive_answer/"
    rootdir_data=motherdir+"/cache/"
    rootdir_tested=motherdir+"/tested/"
    rootdir_bad=motherdir+"/bad/"
    rootdir_result=motherdir+"/output/"
    rootdir_info="./sysinfo/"
    rootdir_invalidjson=motherdir+"/invalidjson/"
    return (rootdir_answer,rootdir_prmanswer,rootdir_data,rootdir_tested,rootdir_bad,rootdir_result,rootdir_info,rootdir_invalidjson)