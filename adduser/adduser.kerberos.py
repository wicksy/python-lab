#!/usr/bin/env python

import argparse
import os
import pexpect
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--userid", help="Userid", required=True)
parser.add_argument("-p", "--password", help="Password", required=True)
args = parser.parse_args()

userid = args.userid
password = args.password

if userid == "root" or userid == 0:
  print("FATAL: Cannot modify the root user with this script")
  sys.exit(1)

password = password[::-1]

print("INFO: Adding " + userid)
adduser = "/usr/sbin/kadmin.local"
print("INFO: " + adduser)

try:
  child = pexpect.spawn(adduser)
  child.expect("kadmin.local:.*")
  child.sendline("addprinc " + userid)
  child.expect("Enter password.*")
  child.sendline(password)
  child.expect("Re-enter password.*")
  child.sendline(password)
  child.expect("kadmin.local:.*")
  child.sendline("quit")
  time.sleep(1)
  child.close()
except:
  child.kill(9)
  child.close()
  print("ERROR: Adding kerberos principal")
  sys.exit(1)

print("INFO: Account " + userid + " created and password set")
print("INFO: User creation complete")
sys.exit(0)
