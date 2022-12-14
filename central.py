#!/usr/bin/python3

# Author: K. Walsh <kwalsh@holycross.edu>
# Date: 15 October 2022
#
# Code for a cloud file storage central coordinator. This talks to several
# replicas and sometimes also talks to HTTP clients (browsers).

from dataclasses import dataclass # use python3's dataclass feature
import threading                  # for threading.Thread()
import sys                        # for exiting and command-line args
from fileshare_helpers import *   # for csci356 filesharing helper code
from multithread_logging import * # for csci356 logging helper code


# This data type represents a collection of information about some other
# replica. You can add or remove variables as you see fit. Use it like this:
#   x = Replica("1.2.3.4", "San Francisco, CA", 6000)
#   print(x)
#   print(x.region)
#   list_of_replicas = []
#   list_of_replicas.append(x)
@dataclass
class Replica:
    dnsname: str   # dns name or IP of the replica, used to open a socket to that replica
    region: str    # geographic region where that replica is located
    backend_portnum: int   # back-end port number which that replica is listening on


####  Global Variables ####

my_name = None            # dns name of this server
my_frontend_port = None   # port number for the browser-facing listening socket
my_backend_port = None    # port number for peer-facing listening socket
my_region = None          # geographic region where this server is located

# This condition variable is used to signal that some thread
# crashed, in which case it is time to cleanup and exit the program.
crash_updates = threading.Condition()



#### Top level code to start this central coordinator server  ####

# Given some configuration parameters, this function:
#  - should do something, like open sockets and start threads
#  - should then simply wait forever, until something goes wrong
# If anything goes wrong, then do some cleanup and exit.
def run_central_server(name, region, frontend_port, backend_port):
    logwarn("Starting central coordinator.")
    log("Central coordinator name: %s" % (name))
    log("Central coordinator region: %s" % (region))
    log("Central coordinator frontend port: %s" % (frontend_port))
    log("Central coordinator backend port: %s" % (backend_port))

    global my_name, my_region, my_frontend_port, my_backend_port
    my_name = name
    my_region = region
    my_frontend_port = frontend_port
    my_backend_port = backend_port

    try:

        # TOOD: something useful.

        log("Waiting for something to crash...")
        with crash_updates:
            crash_updates.wait()

    finally:
        log("Some thread crashed, cleaning up...")
        log("Finished!")
        sys.exit(1)

# The code below is used when running this program from the command line. If
# another file imports this one (such as the cloud-drive.py file), then code
# won't run. Instead, the other file would call our run_central_server(...)
# function directly, supplying appropriate parameters.
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage: python3 central.py name region frontend_portnum backend_portnum")
        sys.exit(1)
    name = sys.argv[1]
    region = sys.argv[2]
    frontend_port = int(sys.argv[3])
    backend_port = int(sys.argv[4])

    run_central_server(name, region, frontend_port, backend_port)

