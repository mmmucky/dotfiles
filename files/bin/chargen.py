#!/usr/bin/python
import socket
import os               # Miscellaneous OS interfaces.
import sys              # System-specific parameters and functions.
from time import sleep
UMASK = 0
WORKDIR = "/"
MAXFD = 1024
MESSAGES = ['4', '9', '5', '3', '1', ' ']
I=0
if (hasattr(os, "devnull")):
   REDIRECT_TO = os.devnull
else:
   REDIRECT_TO = "/dev/null"

def createDaemon():
   """Detach a process from the controlling terminal and run it in the
   background as a daemon.
   """
   try:
      pid = os.fork()
   except OSError, e:
      raise Exception, "%s [%d]" % (e.strerror, e.errno)
   if (pid == 0): # The first child.
      os.setsid()
      try:
         pid = os.fork()  # Fork a second child.
      except OSError, e:
         raise Exception, "%s [%d]" % (e.strerror, e.errno)
      if (pid == 0):  # The second child.
         os.chdir(WORKDIR)
         os.umask(UMASK)
      else:
         os._exit(0)  # Exit parent (the first child) of the second child.
   else:
      os._exit(0) # Exit parent of the first child.
   import resource    # Resource usage information.
   maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
   if (maxfd == resource.RLIM_INFINITY):
      maxfd = MAXFD
   for fd in range(0, maxfd):
      try:
         os.close(fd)
      except OSError: # ERROR, fd wasn't open to begin with (ignored)
         pass
   os.open(REDIRECT_TO, os.O_RDWR)  # standard input (0)
   os.dup2(0, 1)      # standard output (1)
   os.dup2(0, 2)      # standard error (2)

   return(0)

if __name__ == "__main__":
#   retCode = createDaemon()
   HOST = 'localhost'
   PORT =1002
   ADDR = (HOST, PORT)
   serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   serversock.bind(ADDR)
   serversock.listen(2)
   while 1:
      clientsock, addr = serversock.accept()
      I=0
      while 1:
         try:
            clientsock.send(MESSAGES[I])
            I=I+1
            if I==len(MESSAGES):
               I=0
            sleep(1)
         except socket.error:
            clientsock.close()
            break
   serversock.close()
   sys.exit(retCode)
