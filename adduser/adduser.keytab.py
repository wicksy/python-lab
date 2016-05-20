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
domain = "EXAMPLE.LOCAL"
keyfile = "/home/" + userid + "/" + userid + ".keytab"

if userid == "root" or userid == 0:
  print("FATAL: Cannot modify the root user with this script")
  sys.exit(1)

password = password[::-1]

print("INFO: Setting up keytab for " + userid)
keytab = "/usr/bin/ktutil"
print("INFO: " + keytab)

try:
  child = pexpect.spawn(keytab)
  child.expect("ktutil:")
  child.sendline("addent -password -p " + userid + "@" + domain + " -k 1 -e rc4-hmac")
  child.expect("Password for")
  child.sendline(password)
  child.sendline("addent -password -p " + userid + "@" + domain + " -k 1 -e aes256-cts")
  child.expect("Password for")
  child.sendline(password)
  child.expect("ktutil:")
  child.sendline("wkt " + keyfile)
  child.expect("ktutil:")
  child.sendline("quit")
  time.sleep(1)
  child.close()
except:
  child.kill(9)
  child.close()
  print("ERROR: Creating keytab")
  sys.exit(1)

rc = os.system("/bin/chmod 0600 " + keyfile)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " chmod on " + keyfile)
  sys.exit(1)

rc = os.system("/bin/chown " + userid + ":" + userid + " " + keyfile)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " chown on " + keyfile)
  sys.exit(1)

print("INFO: Account " + userid + " keytab created (" + keyfile + ")")
print("INFO: Keytab creation complete")
sys.exit(0)
