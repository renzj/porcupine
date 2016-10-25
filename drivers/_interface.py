#encoding=utf8

import os
class FsAdaptor:
    def __init__(self):
        pass
    def create(self,*args,**kwargs):    # path = ''  ftype = ['txt'|'dir'|'bin']
        if args is not None:
            if kwargs.get('ftype',-1)!=-1:
                if kwargs['ftype']=='dir':
                    try:
                        tmp=os.mkdir(args[0])
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
                        tmp=open(args[0],flag)
                        tmp.close()
                        flag=True
                    except Exception,ex:
                        tmp=ex
                        flag=False
            else:

                    try:
                        tmp=open(args[0],'wb')
                        tmp.close()
                        flag=True

                    except Exception,ex:
                        tmp=ex
                        flag=False
        else:
            tmp='args is none'
            flag = False

        return flag,tmp

    def read(self,*args,**kwargs):    # path ='' size = 0 ftype = r | rb
        if len(args)==2:
            path,size=args
            try:
                f=open(path,'r')
                tmp = f.read(size)
                f.close()
                flag=True
            except Exception,ex:
                tmp=ex
                print tmp
                flag=False
        elif len(args)==3:
            path,size,rtype=args
            try:
                f=open(path,rtype)
                tmp = f.read(size)
                f.close()
                flag=True
            except Exception,ex:
                tmp=ex
                print tmp
                flag=False
        else:
            tmp='parameter error'
            flag=False

        return flag,tmp

    def write(self,*args,**kwargs): # path='' str ='' wtype = 'w' | 'a' | 'wb' | 'ab'
        if len(args)==2:
            path,str,wtype=args
            try:
                f=open(path,wtype)
                tmp=f.write(str)
                f.close()
                flag=True
            except Exception,ex:
                tmp=ex
                flag=False
        else:
            tmp= 'parameter ERROR'
            flag=False
        return flag,tmp

    def delete(self,*args,**kwargs): #path=''
        if args !=():
            path =args[0]
            if os.path.isdir(path):
                try:
                    tmp=os.rmdir(path)
                    flag=True
                except Exception,ex:
                    tmp=ex
                    flag=False
            elif os.path.isfile(path):
                try:
                    tmp=os.remove(path)
                    flag=True
                except Exception,ex:
                    tmp=ex
                    flag=False
            else:
                tmp= 'WRONG PATH'
                flag=False
        else:
            tmp='args is none'
            flag = False

        return flag,tmp

    def rename(self,*args,**kwargs):
        if len(args)==2:
            old,new = args
            tmp=os.rename(old, new)
            flag=True
        else:
            tmp='parameter error'
            flag=False

        return flag,tmp
