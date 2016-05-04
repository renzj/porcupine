#encoding=utf8
#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      tianmingZhang
#
# Created:     06/04/2016
# Copyright:   (c) tianmingZhang 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from configure import configuration

import mysql_utils
import time

def read_config(path):

    import json
    isSuccess=True
    fiobj = {}
    fi=None
    try:

        fi=file(path)
        fiobj=json.load(fi)
    except Exception,ex:
        isSuccess=False
    finally:
        if fi !=None :
            fi.close()

    return isSuccess,fiobj

def main(config_path="cfbench.json"):

    import os

    isSuccess,config_objs=read_config(os.path.join(os.getcwd(),config_path))

    if isSuccess==False:
        print "read json %s except error" %(config_path)
        return

    db_conn,mcur = mysql_utils.connMySQL(host='10.65.7.151')
    mcur.execute('select max(respid) from responses')

    last_resp_id=mcur.fetchone()

    if len(last_resp_id) == 0:
        last_resp_id = []
        last_resp_id.append(0)


    iat_module,iat_name = configuration(config_objs['request_of_iat']['name'],config_objs['request_of_iat']['conf_tag'])
    mIATGenerator=getattr(iat_module,iat_name)(**(config_objs['request_of_iat']['kwargs']))

    kwargs_context={}

    FS_MODULE,FS_CLASS_NAME=configuration(config_objs['file_system']['name'],config_objs['file_system']['conf_tag'])

    kwargs_context.update({'fs_module':FS_MODULE,'fs_class_name':FS_CLASS_NAME})

    kwargs_context.update(config_objs['request_generator']['kwargs'])

    kwargs_context.update({'IATGenerator':mIATGenerator})

    kwargs_context.update({'interval_get_number_of_active_thread':config_objs['interval_get_number_of_active_thread']})

    kwargs_context.update(config_objs['tenant'])

    req_module,req_name = configuration(config_objs['request_generator']['name'],config_objs['request_generator']['conf_tag'])
    mRequestGenerator = getattr(req_module,req_name)(**kwargs_context)

    btime = time.time()
    mRequestGenerator.runGenerator()
    endtime = time.time()
    mcur.execute('insert into analysis(tid,disruptive,sleep_for_excess,'\
                 'quota,threads_over_quota,total_generate_times,number_of_request_per_time,run_time,begintime,endtime,last_resp_id) values' \
                 '(%d,"%s",%d,%d,%d,%d,%d,"%s","%s","%s",%d)' %\
                 (config_objs['tenant']['tenantid'],str(config_objs['tenant']['disruptive']),config_objs['tenant']['sleep_for_excess'],\
                 config_objs['tenant']['tenant_quota'],config_objs['tenant']['threads_over_quota'],config_objs['request_generator']['kwargs']['total_generate_times'],\
                 config_objs['request_generator']['kwargs']['number_of_request_per_time'],str(endtime - btime),str(btime),str(endtime),last_resp_id[0]))

    db_conn.commit()

    mysql_utils.closeConn(db_conn,mcur)

    return


def testPop(**kwargs):
    mlist=[]
    for i in xrange(20):
        mlist.append(i)

    print len(mlist)
    print mlist.pop(0)
    print mlist.pop(10)
    print len(mlist)
    print mlist

if __name__ == '__main__':
    main()
##    kws={"total_generate_times":1000,"number_of_request_per_time":100,"check_time":5}
##    kaa=kws
##    kaa.update({'count':123})
##    print kaa
##    testPop(**kaa)



