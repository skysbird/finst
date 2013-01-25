finst
=====
This is an OPS tool for Linux (CentOS first)

TODO:
====

###. add,modify,delete user account into fcenter.

   - add add an account with username skysbird 

  
          finst install -u skysbird -c

   - delete account in fcenter

          finst remove -u skysbird -c

   - means change account passwd in fcenter  

          finst modify -u skysbird -c


	

###. add,modify,delete user account from fcener to local or special node.

  - add an account to local, and the account info from fcenter

          ``finst install -u skysbird ``

  - add an account to a0.xinwaihui.com,a1.xinwaihui.com,.....a9.xinwaihui.com.

          ``finst install -u skysbird -h a[0-9].xinwaihui.com``

  - some other usage
 
             ``finst install -u skysbird -G admin,engineer -g users``

             ``finst install -u skysbird -S 1``

             ``finst remove -u skysbird``

             ``finst change -u skysbird -G admin -S 0 ``




