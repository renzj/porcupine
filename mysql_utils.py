#encoding=utf8------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      tianmingZhang
#
# Created:     12/04/2016
# Copyright:   (c) tianmingZhang 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import MySQLdb

def connMySQL(host='localhost',user='root',passwd='ceph-admin',port=3306,\
                db='cfbench',charset='utf8',use_unicode=True):
    con_args={'host':host,'user':user,'passwd':passwd,'port':port,'db':db,\
                'use_unicode':use_unicode,'charset':charset}

    db_conn=MySQLdb.connect(**con_args)
    #mCur = db_conn.cursor()
    return db_conn,db_conn.cursor()

def closeConn(conn,cur):

    cur.close()
    conn.close()


class FSDriver:

    def __init__(self,fstype):
        pass
    def excute(self,*params):
        #random.uniform(0,3) generate (0,3) float number eg:1.2,2.1,2.0,1.0,0.3
        time.sleep(0.8)# random.uniform(0,1) 如果没有这句，active thread 最多只有10条
        btime = time.time()

        file_object = open(params[3],'r')
        try:
            file_data=file_object.read(params[2])
            if file_data!=None:
                pass #

        finally:
            file_object.close( )

        endtime = time.time()
        file_log = open('D:\\cost_time_log.txt','a')
        try:
            #file_log.write('%.3f - %.3f = %.3f\n' % (btime,endtime,(endtime - btime)))
            file_log.write('%.3f\n' % ((endtime - btime)))
        finally:
            file_log.close()



        # put params and cost timeing into mysql