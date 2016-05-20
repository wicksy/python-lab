#!/usr/bin/env python

import argparse
import os
import pexpect
import sys
import yaml
import ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--userid", help="Userid", required=True)
parser.add_argument("-g", "--groups", help="Groups (comma delimited, no spaces)", required=True)
args = parser.parse_args()

userid = args.userid
groups = args.groups

script = os.path.basename(__file__)
scriptpath = os.path.realpath(__file__)
basedir = os.path.dirname(scriptpath)
configfile = os.path.join(basedir, ".adduser")

config = ConfigParser.RawConfigParser()
config.read(configfile)

print("INFO: Reading config file (" + configfile + ")")
try:
  password = config.get('adduser', 'password')
  print("INFO: Found initial password (REDACTED)")
except:
  print("ERROR: Missing configuration record")
  sys.exit(1)

if userid == "root" or userid == 0:
  print("FATAL: Cannot modify the root user with this script")
  sys.exit(1)

print("INFO: Adding " + userid)
adduser = "/usr/sbin/useradd -m -d /home/" + userid + " -s /bin/bash " + userid
print("INFO: " + adduser)

rc = os.system(adduser)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " adding user")
  sys.exit(1)

print("INFO: Setting groups for " + userid + " to " + groups)
moduser = "/usr/sbin/usermod -G " + groups + " " + userid
print("INFO: " + moduser)

rc = os.system(moduser)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " modifying user")
  sys.exit(1)

print("INFO: Setting initial password for " + userid)
passwd = "passwd " + userid

try:
  child = pexpect.spawn(passwd)
  child.expect("New password:")
  child.sendline(password)
  child.expect("Retype new password:")
  child.sendline(password)
  child.expect("passwd:.*")
  child.close()
except:
  child.kill(9)
  child.close()
  print("ERROR: Setting password")
  sys.exit(1)

print("INFO: Account " + userid + " created and password set")
print("INFO: User creation complete")
sys.exit(0)
