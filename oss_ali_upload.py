# coding:utf8
# created at 2018/7/31.

import os
import oss2
import hashlib
import sys
import base64
from multiprocessing import Pool

ossdir = sys.argv[1]
localdir = sys.argv[2]

auth = oss2.Auth('***','***')
endpoint = 'xxx'
bucket = oss2.Bucket(auth,endpoint,'xxx',connect_timeout=30)

def calculate_file_md5(file_name,block_size=64 * 1024):
    with open(file_name,'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return base64.b64encode(md5.digest())

def upload(file_local,file_remote):
    exist = bucket.object_exists(file_remote)
    encode_md5 = calculate_file_md5(file_local)
    if not exist:
        bucket.put_object_from_file(file_remote,file_local,headers={'Content-MD5':encode_md5})
        print('{} upload sccuess'.format(file_local))

#fl(file local)表示当前文件路径，file_remote表示上传到oss的文件路径

if __name__ == '__main__':
    p = Pool(8)
    for fpath,dirs,fs in os.walk(localdir):
        for f in fs:
            file_local = os.path.join(fpath,f)
            flist = file_local.split('fe-static/')
            file_remote = os.path.join(ossdir,flist[1])
            p.apply_async(upload,args=(file_local,file_remote))
    p.close()
    p.join()
