from _interface import FsAdaptor
class CephDrivers(FsAdaptor):
    def __init__(self):
        FsAdaptor.__init__(self)
    def create(self, *args,**kwargs):  # path = ''  ftype = ['txt'|'dir'|'bin']
        return FsAdaptor.create(self, *args,**kwargs)
    def read(self,*args,**kwargs):    # path,size,ftype path ='' size = 0 ftype = r | rb
        return FsAdaptor.read(self,*args)
    def write(self, *args,**kwargs):# path='' str =''
        return FsAdaptor.write(self, *args,**kwargs)
    def delete(self, *args,**kwargs):
        return FsAdaptor.delete(self, *args,**kwargs)
    def rename(self,*args,**kwargs):

        return FsAdaptor.rename(self,*args,**kwargs)