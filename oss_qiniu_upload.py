# coding:utf8
# created at 2018/7/5.

import os
import sys
import qiniu
from multiprocessing import Pool

ossdir = sys.argv[1]
localdir = sys.argv[2]

q = qiniu.Auth('***','***')
bucket_name = 'xxx'
bucket = qiniu.BucketManager(q)

def upload(file_remote,file_local):
    token = q.upload_token(bucket_name,file_remote,3600)
    ret,info = bucket.stat(bucket_name,file_remote)

    if info.status_code == 612:
        ret,info = qiniu.put_file(token,file_remote,file_local)
        print('{} upload sccuess'.format(file_local))


if __name__ == '__main__':
    p = Pool(8)
    for fpath,dirs,fs in os.walk(localdir):
        for f in fs:
            file_local = os.path.join(fpath,f)
            flist = file_local.split('fe-static/')
            file_remote = os.path.join(ossdir,flist[1])
            p.apply_async(upload,args=(file_remote,file_local))
    p.close()
    p.join()
