#encoding=utf8------------------------------------------------------------------
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
import time
import threading
import mysql_utils

global FS_TYPE,NUM_OF_ACTIVE_THREAD

FS_TYPE = 'ceph'
NUM_OF_ACTIVE_THREAD = 0
# INTERVAL to get number of active thread in system

lock = threading.Lock()

RESPONSE_LIST=[]

##Lock.acquire(blocking=True, timeout=-1),blocking参数表示是否阻塞当前线程等待，timeout表示阻塞时的等待时间 。
##如果成功地获得lock，则acquire()函数返回True，否则返回False，timeout超时时如果还没有获得lock仍然返回False

def makeRequest( *args):

    btime= time.time()
    endtime = btime


##	thread_args_list=[]
##			thread_args_list = [self.tenantid,self.tenant_quota,self.tenant_threads_over_quota,\
##                            self.tenant_is_disruptive,self.tenant_sleep_for_excess,self.fs_module,\
##                            self.fs_class_name,self.requests_per_thread]#0-7
##			for j in range(self.requests_per_thread):
##                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqid'])#8+ 5*j
##                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqtype'])#9,+ 5*j
##                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqsize'])#10+ 5*j
##                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqdst'])#11 + 5*j
##                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqsrc'])#12 + 5*j

    k = 0

    while k < args[7]:#args[7] = request_per_thread

    #   如果是过度用户线程，check 其quota  如果超过quota 则sleep
        if args[3] and threading.activeCount()-1 > args[1]+args[2]:
            if args[4] == -1:#随机休眠时间

                rt = random.random(0,5)
                time.sleep(rt)
                print "tenant %d sleep:%d"%(args[0],rt)

            elif args[4] >0 and args[4] < 20:

                time.sleep(args[4])
                print "tenant %d sleep:%d"%(args[0],args[4])

            else:
                pass
            #print 'dirsputive sleeped 5 seconds'


        fsdriver = getattr(args[5],args[6])()

        reqsize = args[k * 5 + 10]
        isSuccess,data=False,None

        filetype = args[12 + 5*k].split('.')[-1]

        #print 'Request %s excuting' %(args[-1])
        if args[9+ 5*k] == 'r':#read
            isSuccess,data=fsdriver.read( args[12 + 5*k],args[10+ 5*k],'rb' ) # 所有文件都以2进制方式读取  参数：路径，大小(整个文件大小,B字节单位)，读取方式
        elif args[9+ 5*k] == 'c':#create
            isSuccess,data=fsdriver.create( args[12 + 5*k],ftype=filetype)
            reqsize = 0
        elif args[9+ 5*k] == 'd':#delete
            isSuccess,data=fsdriver.delete(args[12 + 5*k])
            reqsize = 0
        elif args[9+ 5*k] == 'rn':#rename
            isSuccess,data=fsdriver.rename(args[12 + 5*k],args[11 + 5*k])
            reqsize = 0
        elif args[9+ 5*k] == 'w':# write
            reqsize,wdata = generate_write_data()
            isSuccess,data=fsdriver.write(args[12 + 5*k],wdata,'wb')
        else:
            return

        endtime = time.time()

        ##db_conn,mcur = mysql_utils.connMySQL(host='10.65.7.151')

        #response text :tid__reqid_issuccess_reqtype_reqsize_ftype__btime_servicetime
        resp_text = str(args[0])+'_'+str(args[8+ 5*k]) +'_'+str(isSuccess)+'_'+args[9+ 5*k]+'_'+str(reqsize)+'_'+filetype+'_'+str(btime)+'_'+str(endtime -btime)

        ##mcur.execute('insert into responses (resp_text) values("%s")' % (resp_text))
        if lock.acquire():
            RESPONSE_LIST.append('%s\n' % (resp_text))
            lock.release()


        k=k+1

    ##db_conn.commit()

    ##mysql_utils.closeConn(db_conn,mcur)


def generate_write_data():

    #utf-8编码 一个汉字 2个字节  gbk编码 一个汉字 1个字节
    wdata = 'afadfasdfasfasfasfsfasfdsadfafaf;ljlsajflasjfldajslfjalsfjla'

    return len(wdata),wdata



class RequestGenerator:

    def __init__(self,**kwargs):
        pass

    def GeneratorRequest(self):
        pass

    def runGenerator(self):
        pass

class ParetoRequestGenerator(RequestGenerator):

    def __init__(self,**kwargs):
        pass

    def GeneratorRequest(self):
        pass


class ConstantRequestGenerator(RequestGenerator):

    def __init__(self,**kwargs):


        self.reqlist = list()
        self.threadlist = list()

        self.timesofdeath = 4
        self.timing = 0

        self.number_req_check = 0
        self.requests_offset = 0
        self.total_requests_in_db = 0
        self.activeThreadCount = 0


        #以下三项 tenantid，request_quota,disruptive从json配置文件里读取
        self.tenantid = kwargs.get('tenantid',3)
        self.tenant_is_disruptive = True if kwargs.get('disruptive',0) == 1 else False

        # 如果为 -1 则是休眠 随机时间,为0 则不休眠
        self.tenant_sleep_for_excess = kwargs.get('sleep_for_excess',5) if self.tenant_is_disruptive else 0

        self.tenant_quota = kwargs.get('tenant_quota',200)
        self.tenant_threads_over_quota = kwargs.get('threads_over_quota',100)
        self.tennat_log_dir = kwargs.get('log_dir','/home/ceph-log/')

        self.requests_per_thread = kwargs.get('requests_per_thread',10)
        self.threads_per_time =kwargs.get('threads_per_time',1000)
        self.number_of_request = kwargs.get('number_of_request',1000)

        self.last_request_thread_file_name  = "request_thread_%s.log"%(str(time.time()))
        self.last_responses_file_name = None

        self.total_generate_times = kwargs.get('total_generate_times',1000)
        self.mIATGenerator= kwargs.get('IATGenerator',None)

        self.interval_get_number_of_active_thread = kwargs.get("interval_get_number_of_active_thread",1)
        self.check_time = kwargs.get('check_time',5)


        self.fs_module = kwargs.get('fs_module',None)
        self.fs_class_name = kwargs.get('fs_class_name',None)


        self.mysql_conn,self.mcur=mysql_utils.connMySQL(host='10.65.7.151')
        self.mcur.execute("select count(*) from requests where tid = %d" % (self.tenantid))
        self.total_requests_in_db = self.mcur.fetchone()[0]
        print "total request:",self.total_requests_in_db
        mysql_utils.closeConn(self.mysql_conn,self.mcur)


        RequestGenerator.__init__(self,**kwargs)

    def getRequest(self):

        # get requests from database mysql

        self.mysql_conn,self.mcur=mysql_utils.connMySQL(host='10.65.7.151')

        reqitems = self.mcur.execute("select * from requests where tid = %d limit %d,%d" % \
                                    (self.tenantid,self.requests_offset,self.number_of_request))

        reqitems = self.mcur.fetchall()

        mysql_utils.closeConn(self.mysql_conn,self.mcur)

        self.requests_offset = self.requests_offset + len(reqitems) if \
                                self.requests_offset + len(reqitems) < self.total_requests_in_db - 1 else 0

        # request dictoary iosize :(kB) iotype:w-write,r--read,d-delete,m--mkdir
        # co--copy c--create ,r--read
        for i in xrange(self.number_of_request):

            self.reqlist.append( {'reqid':reqitems[i%len(reqitems)][1],'tid':reqitems[i%len(reqitems)][2],\
            'reqtype':reqitems[i%len(reqitems)][3],'reqsize':reqitems[i%len(reqitems)][4],\
            'reqdst':reqitems[i%len(reqitems)][5],'reqsrc':reqitems[i%len(reqitems)][6],\
            'ftype':reqitems[i%len(reqitems)][7],'tenant_quota':self.tenant_quota})

    def generateRequest(self):


        self.timing = 0


        self.getRequest()

        for k in xrange(self.threads_per_time):
			thread_args_list=[]
			thread_args_list = [self.tenantid,self.tenant_quota,self.tenant_threads_over_quota,\
                            self.tenant_is_disruptive,self.tenant_sleep_for_excess,self.fs_module,\
                            self.fs_class_name,self.requests_per_thread]#0-7
            for j in xrange(self.requests_per_thread):
                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqid'])#8+ 5*j
                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqtype'])#9,+ 5*j
                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqsize'])#10+ 5*j
                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqdst'])#11 + 5*j
                thread_args_list.append(self.reqlist[(k*self.requests_per_thread+j)%(len(self.reqlist))]['reqsrc'])#12 + 5*j

            self.threadlist.append(threading.Thread(target=makeRequest,args=(tuple(thread_args_list))))

    def startRequest(self):

        self.number_req_check = self.number_req_check + len(self.threadlist)

        for i in xrange(len(self.reqlist)):

            self.threadlist[i].start()
            #self.number_req_check =self.number_req_check - 1


        # put countpertiime and time into mysql 把 countertime 和当前时间 放入数据库中，用于分析 平均每秒请求线程个数

    #清空现有thread list
        self.threadlist =[]
        self.reqlist = []

    def runGenerator(self):
        if self.mIATGenerator is None:
            print 'self.mIATGenerator is none error'
            return

        #start timer to canculate data of request ,threads
        mTimer = threading.Timer(self.interval_get_number_of_active_thread,self.getNumofRunningRequest)
        mTimer.start()

        for i in xrange(self.total_generate_times):
            interval_time = self.mIATGenerator.Get()

            #print 'interval_time:',interval_time

            TIMESOFDEATH = int(interval_time) + self.check_time
            self.setTimesofDeath(TIMESOFDEATH)
            time.sleep(interval_time)
            self.generateRequest()
            self.startRequest()


    def setTimesofDeath(self,timeofdeath):

        self.timesofdeath = timeofdeath


    def getNumofRunningRequest(self):
        # activeCount including main thread,  so -1
        self.activeThreadCount = threading.activeCount() - 1
        print '%s %d %d %d'%( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),\
        (self.activeThreadCount),self.number_req_check,len(RESPONSE_LIST))

        # put activeCount -1 into mysql 写到数据库中 用于分析平均队列长度
        ##mysql_conn,mcur=mysql_utils.connMySQL(host='10.65.7.151')
        if self.last_responses_file_name ==None:

            self.last_responses_file_name = "responses_%s.log" % (str(time.time()))

        else:
            try:
                log_file_size = os.path.getsize(os.path.join(self.tennat_log_dir,self.last_responses_file_name ))

                if log_file_size > 1024*1024*1024*5:##log > 5G 时 换新文件

                    self.last_responses_file_name = "responses_%s.log" % (str(time.time()))

            except:
                print 'ERROR  log file dose not exist!'



        responses_file=open(os.path.join(self.tennat_log_dir,self.last_responses_file_name),"a+")

        request_thread_file= open(os.path.join(self.tennat_log_dir,self.last_request_thread_file_name),"a+")

        request_thread_file.write('threadlines:%d,%s,%d\n'% \
                        (self.tenantid,str(time.time()),self.activeThreadCount))
        request_thread_file.write('arrive_requests:%d,%d,%s\n'% \
                        (self.tenantid,self.number_req_check,str(time.time())))

        request_thread_file.close()



        #mysql_conn.commit()
        btime = time.time()
        responses_len=(RESPONSE_LIST)
        if lock.acquire():
            while len(RESPONSE_LIST) !=0:
                responses_file.writelines(RESPONSE_LIST)

            lock.release()
        print 'responses length:%d costs:%.3f' % (responses_len,time.time() - btime)

        responses_file.close()
        ##mysql_conn.commit()

        ##mysql_utils.closeConn(mysql_conn,mcur)



        #return threading.activeCount - 1

        #上一秒的到达数 置为 0 ，重新计算新一秒的总数
        self.number_req_check = 0


        if self.timing > self.timesofdeath and threading.activeCount() < 3 :
            return
        #循环执行此方法，实现定时器

        #print threading.enumerate()


        self.timing = self.timing + 1

        mTimer = threading.Timer(self.interval_get_number_of_active_thread,self.getNumofRunningRequest)

        mTimer.start()




def main():
    pass

if __name__ == '__main__':
    main()
