from configure import configuration

if __name__=='__main__':

#    mod,mod_name = configuration('ceph','drivers')
    mod,mod_name = configuration('pareto','iat_distribution_impl')##E:\pycharm workspace\CFBench\adaptor\
    pareto = getattr(module,mod_name)()

    #ceph = DriverFactory()
    print pareto
    ##ceph.create()
##    ceph.read('D:\\cost_time_log.txt')
##    ceph.write()
##    ceph.delete()
##    ceph.rename()