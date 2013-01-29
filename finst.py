#!/usr/bin/env python
import sys
import getopt
import os
import subprocess
import crypt


FILE_PATH  = os.path.abspath(os.path.join(os.getcwd(), __file__))
FILO_SERVER = "localhost"
FILO_PORT = 2222

def usage():
    print "usage:"

cmd_list = ['install','remove','modify','dist']

def scp(source, server, path = ""):
        return not subprocess.Popen(["scp", source, "%s:%s" % (server, path)]).wait()
        #cmd = "scp %s %s:/usr/sbin/"%(FILE_PATH,server)
        #return not os.popen(cmd).wait()

def dist(host):
    remote_host_list = split_host(host)
    for host in remote_host_list:
        if scp(FILE_PATH,host,"/usr/sbin"):
            print "Success to distribute finst to %s"%host
        else:
            print "Failed to distrubte finst to %s"%host

def test_already_has_key(host):
    import pexpect
    cmd = "ssh %s echo 'hi'"%host
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect(['password:','continue connecting','hi'],timeout=5)
        if i == 0 or i==1:
            ssh.close()
            return 0
        if i == 2:
            ssh.close()
            print "Key already added to Host %s"%host
            return 1
    except:
        import traceback
        traceback.print_exc()
        return 0
        
    
def do_answer(host,passwd):
    import pexpect
    cmd = "ssh-copy-id %s"%host
    ssh = pexpect.spawn(cmd)
    try:
        i = ssh.expect(['password:','continue connecting','make sure'],timeout=5)
        if i == 0:
            ssh.sendline(passwd)
            j = ssh.expect(['password:','make sure'],timeout=5)            
            if j==0:
                print "password wrong for %s"%host
                ssh.close()
                return 0
            if j==1:
                ssh.close()
                return 1

        elif i==1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
            j = ssh.expect(['password:','make sure'],timeout=5)            
            if j==0:
                print "password wrong for %s"%host
                ssh.close()
                return 0
            if j==1:
                ssh.close()
                return 1
        elif i==2:
            print "Key already added to %s"%host
            ssh.close()
            return 0
        ret = ssh.read()
    except:
        import traceback
        traceback.print_exc()
        pass
        ssh.close()
        return 0
    ssh.close()
    return 1

    
import getpass
def dist_ssh_key(host_str):
    info = "Please Input Password of %s: "%host_str
    passwd = getpass.getpass(info)
    remote_host_list = split_host(host_str)
    for host in remote_host_list:
        print "Adding key to host %s"%host
        if not test_already_has_key(host):
            if do_answer(host,passwd):
                print "Key added to Host %s"%host

        
def add_group(group):
    groupname = group['g']
    return not subprocess.Popen(["groupadd", groupname]).wait()
 
def remove_group(group):
    groupname = group['g']
    return not subprocess.Popen(["groupdel", groupname]).wait()

def add_user(user):
    username = user['u']
    user_str = center_get_user(username)
    if user_str=="no data":
        print "user does not exsist in filo, please add user in filo first"
        sys.exit(2)
    user_dict = json.loads(user_str)
    passwd = user_dict['passwd']
    G = None
    g = None
    if user.has_key("G"):
        G = user["G"]

    if user.has_key("g"):
        g = user["g"]

    if not g and not G:
        return not subprocess.Popen(["useradd", "-m",username,"-p",passwd]).wait()
    elif g and G:
        return not subprocess.Popen(["useradd", "-m",username,"-p",passwd,"-g",g,"-G",G]).wait()
    elif g:
        return not subprocess.Popen(["useradd", "-m",username,"-p",passwd,"-g",g]).wait()
    elif G:
        return not subprocess.Popen(["useradd", "-m",username,"-p",passwd,"-G",G]).wait()

def modify_user(user):
    username = user['u']
    user_str = center_get_user(username)
    if user_str=="no data":
        print "user does not exsist in filo, please mod user in filo first"
        sys.exit(2)
    user_dict = json.loads(user_str)
    G = None
    g = None
    if user.has_key("G"):
        G = user["G"]

    if user.has_key("g"):
        g = user["g"]

    if g and G:
        return not subprocess.Popen(["usermod", "-g",g,"-G",G,username]).wait()
    elif g:
        return not subprocess.Popen(["usermod", "-g",g,username]).wait()
    elif G:
        return not subprocess.Popen(["usermod", "-G",G,username]).wait()

def remove_user(user):
    username = user['u']
    return not subprocess.Popen(["userdel", username]).wait()

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


def remote_add_group(cmd_dict,remote_host):
    cmd = "finst.py install"
    params = ""
    for c,a in cmd_dict.iteritems():
        if c=='h':
            continue
        params = params + "-%s %s "%(c,a)
    cmd = "%s %s"%(cmd,params)
    rel = subprocess.Popen(["ssh", remote_host, cmd]).wait()
    return not rel

def remote_remove_group(cmd_dict,remote_host):
    cmd = "finst.py remove"
    params = ""
    for c,a in cmd_dict.iteritems():
        if c=='h':
            continue
        params = params + "-%s %s "%(c,a)
    cmd = "%s %s"%(cmd,params)
    rel = subprocess.Popen(["ssh", remote_host, cmd]).wait()
    return not rel

import json
import socket,ssl,pprint
import string
import random

def makepassword(rang = "23456789qwertyupasdfghjkzxcvbnm", size = 8):
    return string.join(random.sample(rang, size)).replace(" ","")

def send_cmd(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
   # require a certificate from the server
    ssl_sock = ssl.wrap_socket(s)
    ssl_sock.connect((FILO_SERVER, FILO_PORT))
    ssl_sock.write(cmd)
    data = ssl_sock.read()
    data += ssl_sock.read()
    ssl_sock.close()
    return data

def center_get_user(username):
    cmd_dict = {}
    cmd_dict['cmd'] = 'get_user'
    cmd_dict['u'] = username
    cmd_str = json.dumps(cmd_dict)
    r = send_cmd(cmd_str)
    return r

def center_add_user(user):
   if not user.has_key('e'):
        usage()
        sys.exit(2)

   user_str = center_get_user(user['u'])
   if user_str!="no data":
        print "user already exsist in filo center"
        sys.exit(2)

   passwd = makepassword()
   print "passwd is %s"%passwd
   passwd = crypt.crypt(passwd,makepassword(size=2))
   cmd_dict = user
   cmd_dict['cmd'] = "add_user"
   cmd_dict['p'] = passwd
   cmd_str = json.dumps(cmd_dict)
   r = send_cmd(cmd_str)
   return r=="ok"

def center_remove_user(user):
   user_str = center_get_user(user['u'])
   if user_str=="no data":
        print "user has not in filo yet"
        sys.exit(2)
   cmd_dict = user
   cmd_dict['cmd'] = "remove_user"
   cmd_str = json.dumps(cmd_dict)
   r = send_cmd(cmd_str)
   return r=="ok"

def center_modify_user(user):
   user_str = center_get_user(user['u'])
   if user_str=="no data":
        print "user has not in filo yet"
        sys.exit(2)
   cmd_dict = user
   cmd_dict['cmd'] = "modify_user"
   cmd_str = json.dumps(cmd_dict)
   r = send_cmd(cmd_str)
   return r=="ok"
   
def main(argv):
    try:           
        cmd = sys.argv[1]
        if cmd not in cmd_list:
            usage();
            sys.exit(2)
        opts, args = getopt.getopt(argv, "g:h:u:cG:e:", ["sudo","ssh-key"]) 
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
        elif o=='-e':
            cmd_dict['e'] = a
        elif o=='-c':
            cmd_dict['c'] = 1
        elif o=='--ssh-key':
            cmd_dict['ssh-key'] = 1
        elif o=='--sudo':
            cmd_dict['sudo'] = 1


    if cmd == "dist":
        if cmd_dict.has_key('h'):
            if not cmd_dict.has_key("ssh-key"):
                host_list = cmd_dict['h']
                dist(host_list)
            else:
                host_list = cmd_dict['h']
                dist_ssh_key(host_list)
                
        else:
            usage()
        sys.exit(0)
    
    if cmd_dict.has_key('c'):
        print "center action" 
        if cmd == "install":
            if cmd_dict.has_key('u'):
                if center_add_user(cmd_dict):
                    print "Success to add user to filo center"
        elif cmd == "modify":
            if cmd_dict.has_key('u'):
                if center_modify_user(cmd_dict):
                    print "Success to add user to filo center"
        elif cmd == "remove":
            if cmd_dict.has_key('u'):
                if center_remove_user(cmd_dict):
                    print "Success to add user to filo center"

        sys.exit(0)
        
    if cmd_dict.has_key('h'):
        print "remote action"
        remote_host = cmd_dict['h']
        remote_host_list = split_host(remote_host)
        for remote_host in remote_host_list:
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

            if cmd == "install":
                if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                   if remote_add_group(cmd_dict,remote_host):
                        print "Success to add group to remote host %s"%remote_host
                   else:
                        print "Failed to add group to remote host %s"%remote_host
            if cmd == "remove":
                if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                   if remote_remove_group(cmd_dict,remote_host):
                        print "Success to remove group to remote host %s"%remote_host
                   else:
                        print "Failed to remove group to remote host %s"%remote_host
            
            sys.exit(0)

    else:
        print "local action"
        if cmd == "install":
            if cmd_dict.has_key('u'):
                if add_user(cmd_dict):
                    print "Success to add user"
                else:
                    print "Failed to add user"
                    sys.exit(2)

        if cmd == "modify":
            if cmd_dict.has_key('u'):
                if modify_user(cmd_dict):
                    print "Success to modify user"
                else:
                    print "Failed to modify user"
                    sys.exit(2)
        if cmd == "remove":
            if cmd_dict.has_key('u'):
                if remove_user(cmd_dict):
                    print "Success to remove user"
                else:
                    print "Failed to remove user"
                    sys.exit(2)

        if cmd == "install":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                if add_group(cmd_dict):
                    print "Success to add group"
                else:
                    print "Failed to add group"
                    sys.exit(2)

        if cmd == "remove":
            if cmd_dict.has_key('g') and not cmd_dict.has_key('u'):
                if remove_group(cmd_dict):
                    print "Success to remove group"
                else:
                    print "Failed to remove group"
                    sys.exit(2)

        sys.exit(0)
        
             
    print opts

import re

reobj = re.compile("\[.*\]")


def merge(a,b):
    #merge a[0-9] like to b, b must not have []
    rel = []
    if '[' not in a and ']' not in a:
        if b:
            return ["%s.%s"%(a,b)]
        else:
            return [a]
    else:
        #parse [] in a
        number_str = reobj.findall(a)[0][1:-1]
        
        ra = reobj.sub("[]",a)
        number_list = number_str.split('-')
        for n in range(int(number_list[0]),int(number_list[1])+1):
            if b:
                rel.append("%s.%s"%(reobj.sub(str(n),ra),b))
            else:
                rel.append("%s"%(reobj.sub(str(n),ra)))
        return rel
            
        
          
def parse(host):
    part_list = host.split(".")
    result = [""]

    for part in reversed(part_list):
        result1 = []
        for r in result:
            result1 = result1+ merge(part,r)
            
        result = result1
    return result1

    

def split_host(host):
    rel = []
    host = host.strip()
    reobj = re.compile("\s+")
    host = reobj.sub(' ',host)
    host_list = host.split(' ')

    for h in host_list:
        rel = rel + parse(h)
    return rel 
    


if __name__ == "__main__":
    profile_server = os.environ.get('FINST_PROFILE_SERVER')
    if not profile_server:
        print "Not find FINST_PROFILE_SERVER environment variable, will use the default localhost:2222"
    else:
        server_port = profile_server.split(":")
        FILO_SERVER = server_port[0]
        FILO_PORT = int(server_port[1])

    if len(sys.argv)<2:
        usage();
    else:
        main(sys.argv[2:])
