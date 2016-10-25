#encoding=utf8------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      
#
# Created:     12/04/2016
# Copyright:   (c)  2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import platform
SYSTEM=platform.system()

if SYSTEM =='Windows':
    import mysql.connector as DB
else:
    import MySQLdb as DB

def connMySQL(host='localhost',user='root',passwd='ceph-admin',port=3306,\
                db='cfbench',charset='utf8',use_unicode=True):
    con_args={'host':host,'user':user,'passwd':passwd,'port':port,'db':db,\
                'use_unicode':use_unicode,'charset':charset}

    db_conn=DB.connect(**con_args)
    #mCur = db_conn.cursor()
    return db_conn,db_conn.cursor()

def closeConn(conn,cur):

    cur.close()
    conn.close()

