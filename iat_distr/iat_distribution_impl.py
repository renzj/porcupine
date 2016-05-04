#encoding=utf8-----------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      tianmingZhang
#
# Created:     18/04/2016
# Copyright:   (c) tianmingZhang 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import  random

class IATGenerator(object):

    def __init__(self,**kwargs):
        pass

    def Get(self):
        pass

class ConstantIATGenerator(IATGenerator):

    def __init__(self,**kwargs):

        IATGenerator.__init__(self,**kwargs)
        self.constant_time = kwargs.get("contant_time",1)
    def Get(self):

        return self.constant_time

class ParetoIATGenerator(IATGenerator):

    def __init__(self,**kwargs):

        IATGenerator.__init__(self,**kwargs)

        self.alpha = kwargs.get('alpha',1)
        self.seed= kwargs.get('seed',1)
        random.seed(self.seed)
        self.time_base = kwargs.get('time_base',10)

    def Get(self):

        return random.paretovariate(self.alpha) / self.time_base # BASE:1, 10 ,100 ,

def main():
    pass

if __name__ == '__main__':
    main()
