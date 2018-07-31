# coding:utf8
# created at 2018/7/5.
import os
import sys
import qiniu

ossdir = sys.argv[1]
localdir = sys.argv[2]

q = qiniu.Auth('***','***')
bucket_name = 'xxx'
bucket = qiniu.BucketManager(q)

def qiniu_upload(ossdir,localdir):
    for fpath,dirs,fs in os.walk(localdir):
        for f in fs:
            file_local = os.path.join(fpath,f)
            flist = file_local.split('fe-static/')
            #本地路径/app/fe-static/common
            file_remote = os.path.join(ossdir,flist[1])
            token = q.upload_token(bucket_name,file_remote,3600)
            ret,info = bucket.stat(bucket_name,file_remote)
            if info.status_code == 200:
                continue
            elif info.status_code == 612:
                ret,info = qiniu.put_file(token,file_remote,file_local)
                print('{} upload sccuess'.format(file_local))
            else:
                print(info.status_code)
                break

qiniu_upload(ossdir,localdir)

#执行
#python /opt/scripts/oss_qiniu_upload.py '' /app/fe-static/test
