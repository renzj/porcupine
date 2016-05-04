
def configuration(mmname,mmtag):
    import sys
    from lxml import etree
    class xml(object):
        def __init__(self):
            self.path =''
            self.direct =''
            self.class_name =''
#    fstype = 'ceph'
    fs=xml()
    try:
        xml=etree.parse('cfbench.cfg.xml')
        root=xml.getroot()
        for mod in root:
            if mod.attrib['name']== mmname and mod.tag == mmtag:
                for submod in mod:
                    setattr(fs,submod.tag,submod.text)
                break
    except Exception,ex:
        print 'Parse XML Error',ex
    sys.path.append(fs.path)
    module =__import__(fs.direct,[fs.class_name])

 #   ceph = getattr(module,fs.class_name)
    return module,fs.class_name



