finst
=====
This is an OPS tool for Linux (CentOS first)

TODO:
====
###. add,  remove a group.

   - add group with name=eng

         finst install -g eng 
  
         finst install -g eng -h a[0-9].xinwaihui.com

   - remove group
  
         finst remove -g eng

         finst remove -g eng -h a[0-9].xinwaihui.com

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

          finst install -u skysbird -h a[0-9].xinwaihui.com

  - some other usage
 
          finst install -u skysbird -G admin,engineer -g users

          finst install -u skysbird 

          finst remove -u skysbird

          finst modify -u skysbird -G admin 

###. sudo users

   - add group to sudoers

         finst install --sudo -g adm

   - remove group from sudoers

         finst remove --sudo -g admin


    



