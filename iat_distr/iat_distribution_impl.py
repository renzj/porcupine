#encoding=utf8-----------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      
#
# Created:     18/04/2016
# Copyright:   (c)  2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import  random

class IATGenerator(object):

    def __init__(self,**kwargs):
        self.seed= kwargs.get('seed',1)

        random.seed(self.seed)
        self.time_base = kwargs.get('time_base',10)

    def Get(self):
        pass

class ParetoIATGenerator(IATGenerator):

    def __init__(self,**kwargs):

        IATGenerator.__init__(self,**kwargs)
        self.alpha = kwargs.get('alpha',1)

    def Get(self):

        return random.paretovariate(self.alpha) / self.time_base,self.time_base # BASE:1, 10 ,100 ,

def main():
    pass

if __name__ == '__main__':
    main()

    main()
