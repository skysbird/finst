#!/usr/bin/env python
import sys
import getopt
import os
import subprocess
FILE_PATH  = os.path.abspath(os.path.join(os.getcwd(), __file__))

def usage():
    print "usage:"

cmd_list = ['install','remove','modify','dist']

def scp(source, server, path = ""):
        return not subprocess.Popen(["scp", source, "%s:%s" % (server, path)]).wait()
        #cmd = "scp %s %s:/usr/sbin/"%(FILE_PATH,server)
        #return not os.popen(cmd).wait()

def dist(host):
    print FILE_PATH
    if scp(FILE_PATH,host,"/usr/sbin"):
        print "Success to distribute finst to %s"%host
    else:
        print "Failed to distrubte finst to %s"%host

def add_user(user):
    print "add user"

def remote_add_user(cmd_dict,remote_host):
    cmd = "finst.py install"
    params = ""
    for c,a in cmd_dict.iteritems():
        if c=='h':
            continue
        params = params + "-%s %s "%(c,a)
    cmd = "%s %s"%(cmd,params)
    rel = subprocess.Popen(["ssh", remote_host, cmd]).wait()
    return not rel

def remote_modify_user(cmd_dict,remote_host):
    cmd = "finst.py modify"
    params = ""
    for c,a in cmd_dict.iteritems():
        if c=='h':
            continue
        params = params + "-%s %s "%(c,a)
    cmd = "%s %s"%(cmd,params)
    rel = subprocess.Popen(["ssh", remote_host, cmd]).wait()
    return not rel

def remote_remove_user(cmd_dict,remote_host):
    cmd = "finst.py remove"
    params = ""
    for c,a in cmd_dict.iteritems():
        if c=='h':
            continue
        params = params + "-%s %s "%(c,a)
    cmd = "%s %s"%(cmd,params)
    rel = subprocess.Popen(["ssh", remote_host, cmd]).wait()
    return not rel

def main(argv):
    try:           
        cmd = sys.argv[1]
        if cmd not in cmd_list:
            usage();
            sys.exit(2)
        opts, args = getopt.getopt(argv, "g:h:u:cG:", ["sudo"]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)             

    cmd_dict = {}
    for o,a in opts:
        if o=="-u":
            cmd_dict['u'] = a
        elif o=='-g':
            cmd_dict['g'] = a
        elif o=='-h':
            cmd_dict['h'] = a
        elif o=='-G':
            cmd_dict['G'] = a
        elif o=='-c':
            cmd_dict['c'] = 1

    if cmd == "dist":
        if cmd_dict.has_key('h'):
            host_list = cmd_dict['h']
            dist(host_list)
        else:
            usage()
        sys.exit(0)
    
    if cmd_dict.has_key('c'):
        print "center action" 
        if cmd == "install":
            if cmd_dict.has_key('u'):
                print "center add user"
        elif cmd == "modify":
            if cmd_dict.has_key('u'):
                print "center modify user"
        elif cmd == "remove":
            if cmd_dict.has_key('u'):
                print "center remove user"

        sys.exit(0)
        
    if cmd_dict.has_key('h'):
        print "remote action"
        remote_host = cmd_dict['h']
        if cmd == "install":
            if cmd_dict.has_key('u'):
               if remote_add_user(cmd_dict,remote_host):
                    print "Success to add user to remote host %s"%remote_host
               else:
                    print "Failed to add user to remote host %s"%remote_host

        if cmd == "modify":
            if cmd_dict.has_key('u'):
               if remote_modify_user(cmd_dict,remote_host):
                    print "Success to modify user to remote host %s"%remote_host
               else:
                    print "Failed to modify user to remote host %s"%remote_host
        if cmd == "remove":
            if cmd_dict.has_key('u'):
               if remote_remove_user(cmd_dict,remote_host):
                    print "Success to remove user to remote host %s"%remote_host
               else:
                    print "Failed to remove user to remote host %s"%remote_host

        sys.exit(0)

        if cmd == "install":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                print "add group"
        if cmd == "modify":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                print "modify group"
        if cmd == "remove":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                print "remove group"
        
        sys.exit(0)

    else:
        print "local action"
        if cmd == "install":
            if cmd_dict.has_key('u'):
                add_user({})
        if cmd == "modify":
            if cmd_dict.has_key('u'):
                print "modify user"
        if cmd == "remove":
            if cmd_dict.has_key('u'):
                print "remove user"

        if cmd == "install":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                print "add group"
        if cmd == "modify":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                print "modify group"
        if cmd == "remove":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                print "remove group"

        sys.exit(0)
        
             
    print opts

if __name__ == "__main__":
    if len(sys.argv)<2:
        usage();
    else:
        main(sys.argv[2:])
