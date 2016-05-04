#encoding=utf8------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      tianmingZhang
#
# Created:     19/04/2016
# Copyright:   (c) tianmingZhang 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import mysql_utils
import time
def insert_into_detail(resp_id=0):
    db_conn,mcur = mysql_utils.connMySQL(host='10.65.7.151')
   
    mcur.execute("select resp_text from responses where respid> %d"%(resp_id))

    results=mcur.fetchall()
    print 'results to be inserted:',len(results)
    
    bt = time.time()
    for item in results:
        entries = item[0].split('_')

        #当文件类型中包含  '_'  下划线时：
        ftype = entries[5]
        for i in range(8,len(entries)):
            ftype = ftype +'_'+entries[i-2]
        mcur.execute("insert into responsesdetail values(NULL,%d,%d,'%s','%s',%d,'%s','%s',%f)" \
            %(int(entries[0]),int(entries[1]),entries[2],entries[3],int(entries[4]),ftype,\
            entries[-2],float(entries[-1])))

    db_conn.commit()
    mysql_utils.closeConn(db_conn,mcur)

    print 'It costs:',time.time() - bt
def avg_data_by_id(threadid=0,arrive_req_id=0,respde_id=0):

    db_conn,mcur = mysql_utils.connMySQL(host='10.65.7.151')
    mcur.execute("select tid,AVG(active_threads) from threadlines where id>%d group by tid"%(threadid))
    avg_active_threads_results = mcur.fetchall()


    mcur.execute("select tid,AVG(avg_arrive_reqs) from arrive_requests where id > %d group by tid"%(arrive_req_id))
    avg_arrive_reqs_results = mcur.fetchall()

    mcur.execute("select tid,AVG(servicetime) from responsesdetail where id > %d group by tid "%(respde_id))
    avg_servicetime_results = mcur.fetchall()

    print 'avg_active_threads:'

    for result in avg_active_threads_results:
        print '\t %d   %.3f ' %(result[0],result[1])

    print 'avg_arrive_reqs:'

    for result in avg_arrive_reqs_results:
        print '\t %d   %.3f ' %(result[0],result[1])

    print 'avg_servicetime:'

    for result in avg_servicetime_results:
        print '\t %d   %.3f ' %(result[0],result[1])

def avg_data_by_time(starttime,endtime):

    db_conn,mcur = mysql_utils.connMySQL(host='10.65.7.151')
    if starttime ==0 or endtime==0:
        return

    wherestatement=' between %s and %s group by tid'%(str(float(starttime)),str(float(endtime)))
    mcur.execute("select tid,AVG(active_threads) from threadlines where checktime %s "%(wherestatement))
    avg_active_threads_results = mcur.fetchall()


    mcur.execute("select tid,AVG(avg_arrive_reqs) from arrive_requests where checktime %s "%(wherestatement))
    avg_arrive_reqs_results = mcur.fetchall()

    mcur.execute("select tid,AVG(servicetime) from responsesdetail where begintime %s "%(wherestatement))
    avg_servicetime_results = mcur.fetchall()

    print 'avg_active_threads:'

    for result in avg_active_threads_results:
        print '\t %d   %.3f ' %(result[0],result[1])

    print 'avg_arrive_reqs:'

    for result in avg_arrive_reqs_results:
        print '\t %d   %.3f ' %(result[0],result[1])

    print 'avg_servicetime:'

    for result in avg_servicetime_results:
        print '\t %d   %.3f ' %(result[0],result[1])


def main(threadid=0,arrive_req_id=0,respde_id=0,resp_id=0,starttime=0,endtime=0):
    insert_into_detail(resp_id=resp_id)

   # avg_data_by_id(threadid=threadid,arrive_req_id=arrive_req_id,respde_id=respde_id)
    avg_data_by_time(starttime,endtime)
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 4:
        main(threadid=int(sys.argv[1]),arrive_req_id=int(sys.argv[2]),respde_id=int(sys.argv[3]),resp_id=int(sys.argv[4]))
    elif len(sys.argv) > 3 and len(sys.argv[1]) > 10 and len(sys.argv[2]) > 10:
        
        main(resp_id=int(sys.argv[3]),starttime=sys.argv[1],endtime=sys.argv[2])

    else:
        print 'parameter error you must enter thread ,req,respde,response ids or starttime,endtime'




