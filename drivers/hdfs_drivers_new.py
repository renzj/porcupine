'''
Created on 2016-6-28

@author: Xuan zhang
'''
from _interface import FsAdaptor
from pydoop.hdfs import hdfs
class CephDrivers(FsAdaptor):
    def __init__(self,host='default',port=0,user=None,groups=None):
        FsAdaptor.__init__(self)
        self.fs = hdfs(host,port,user,groups)
    def create(self, *args,**kwargs):  # path = ''  ftype = ['txt'|'dir'|'bin']
        if args is not None:
            if kwargs.get('ftype',-1)!=-1:
                if kwargs['ftype']=='dir':
                    try:
                        tmp=self.fs.create_direcotry(args[0])
                        flag=True
                    except Exception,ex:
                        tmp=ex
                        flag=False
                else:
                    if kwargs['ftype']=='txt':
                        flag = 'w'
                    else:#如果不是目录，默认都以2进制读写
                        flag = 'wb'
                    try:
                        tmp=self.fs.open_file(args[0],flag)
                        tmp.close()
                        flag=True
                    except Exception,ex:
                        tmp=ex
                        flag=False
            else:

                    try:
                        tmp=self.fs.open_file(args[0],'wb')
                        tmp.close()
                        flag=True

                    except Exception,ex:
                        tmp=ex
                        flag=False
        else:
            tmp='args is none'
            flag = False

        return flag,tmp
    def read(self,*args,**kwargs):    # path,size,ftype path ='' size = 0 ftype = r | rb
        if len(args)==2:
            path,size=args
            try:
                f=self.fs.open_file(path,'r')
                tmp = f.read(size)
                f.close()
                flag=True
            except Exception,ex:
                tmp=ex
                flag=False
        elif len(args)==3:
            path,size,rtype=args
            try:
                f=self.fs.open_file(path,rtype)
                tmp = f.read(size)
                f.close()
                flag=True
            except Exception,ex:
                tmp=ex
                flag=False
        else:
            tmp='parameter error'
            flag=False

        return flag,tmp
    def write(self, *args,**kwargs):# path='' str =''
        if len(args)==2:
            path,str,wtype=args
            try:
                f=self.fs.open_file(path,wtype)
                tmp=f.write(str)
                f.close(f)
                flag=True
            except Exception,ex:
                tmp=ex
                flag=False
        else:
            tmp= 'parameter ERROR'
            flag=False
        return flag,tmp
    def delete(self, *args,**kwargs):
        if args !=():
            path = args[0]
            try:
                tmp=self.fs.delete(path)
                flag=True
            except Exception,ex:
                tmp=ex
                flag=False
        else:
            tmp='args is none'
            flag = False

        return flag,tmp
    def rename(self,*args,**kwargs):
        if len(args)==2:
            old,new = args
            try:
                tmp=self.fs.rename(old,new)
                flag=True
            except Exception,ex:
                tmp=ex
                flag = False
        else:
            tmp='parameter error'
            flag=False

        return flag,tmp
