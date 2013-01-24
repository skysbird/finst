finst
=====
This is an OPS tool for Linux (CentOS first)

TODO:


1 add,modify,delete user account into fcenter.
  a.
  finst install -u skysbird -c
  means add an account:
	username = skysbird
	passwd = [random]

  b.
  finst remove -u skysbird -c
  means delete account in fcenter

  c.
  finst modify -u skysbird -c
  means change account passwd in fcenter
	

2 add,modify,delete user account from fcener to local or special node.

  a.
  finst install -u skysbird 

  means add an account to local, and the account info from fcenter

  finst install -u skysbird -h a[0-9].xinwaihui.com

  means add an account to a0.xinwaihui.com,a1.xinwaihui.com,.....a9.xinwaihui.com.

  




