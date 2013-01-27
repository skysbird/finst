#!/usr/bin/env python
import sys
import getopt

def usage():
    print "usage:"

cmd_list = ['install','remove','modify','dist']
def main(argv):
    try:           
        cmd = sys.argv[1]
        if cmd not in cmd_list:
            usage();
            sys.exit(2)
        opts, args = getopt.getopt(argv, "g:h:u:c", ["sudo"]) 
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
        elif o=='-c':
            cmd_dict['c'] = 1

    if cmd == "dist":
        if cmd_dict.has_key('h'):
            print "dist"
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

        if cmd == "install":
            if cmd_dict.has_key('u'):
                print "add user"
        if cmd == "modify":
            if cmd_dict.has_key('u'):
                print "modify user"
        if cmd == "remove":
            if cmd_dict.has_key('u'):
                print "remove user"

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
                print "add user"
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
