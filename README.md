finst
=====
This is an OPS tool for Linux (CentOS first)

Deployment
=====
![Alt text](https://raw.github.com/skysbird/finst/master/finst.png)


INSTALL
======
###. Build the Profile Server

    Profile Server is written by Erlang OTP R15B02, and we just test it can be ran on this version of erlang, so please make sure you have installed Erlang OTP R15B02 or higher version on your server.

          cd filo/ss_server

         ./rebar compile

         ./rebar generate



###. Startup the Profile Server

         ./start_profile_server.sh 

            Profile Server will start up, and will be listen on port 2222 by default, you can change this port value in filo/ss_server/rel/ss_server/releases/1/vm.args. just add the line -listen_port 12345 in the file then restart the profile server.

   
###. Shutdown the Profile Server

         ./shutdown_profile_server.sh

    
Feature:
====
###. distribute the ssh-key
	
    finst dist --ssh-key -h 'a[0-9].xinwaihui.com'


###. distribute finst self

   - distribute finst to remote host

        finst dist  -h 'a[0-9].xinwaihui.com b[0-9].xinwaihui.com'


###. add,modify,remove user account into fcenter.

   - add add an account with username skysbird 

  
          finst install -u skysbird -c

   - remove account in fcenter

          finst remove -u skysbird -c

   - means change account passwd in fcenter  

          finst modify -u skysbird -c


	

###. add,modify,remove user account from fcener to local or special node.

  - add an account to local, and the account info from fcenter

          finst install -u skysbird 

  - add an account to a0.xinwaihui.com,a1.xinwaihui.com,.....a9.xinwaihui.com.

          finst install -u skysbird -h 'a[0-9].xinwaihui.com'

  - some other usage
 
          finst install -u skysbird -G admin,engineer -g users

          finst install -u skysbird 

          finst remove -u skysbird

          finst modify -u skysbird -G admin 




TODO
=======

###. add,  remove a group.

   - add group with name=eng

         finst install -g eng 
  
         finst install -g eng -h 'a[0-9].xinwaihui.com b[0-9].xinwaihui.com'

   - remove group
  
         finst remove -g eng

         finst remove -g eng -h 'a[0-9].xinwaihui.com'


###. sudo users

   - add group to sudoers

         finst install --sudo -g adm

   - remove group from sudoers

         finst remove --sudo -g admin



