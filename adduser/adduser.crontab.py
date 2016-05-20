#!/usr/bin/env python

import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--userid", help="Userid", required=True)
args = parser.parse_args()

userid = args.userid
cron = "0 0 * * * kinit -kt /home/" + userid + "/" + userid + ".keytab " + userid
cronfile = "/tmp/adduser.crontab." + str(os.getpid())

if userid == "root" or userid == 0:
  print("FATAL: Cannot modify the root user with this script")
  sys.exit(1)

print("INFO: Setting up crontab for " + userid)
print("INFO: " + cron)

os.system("/bin/rm -f " + cronfile)
f = open(cronfile, 'w')
f.write(cron + "\n")
f.close()

rc = os.system("/usr/bin/crontab -u " + userid + " " + cronfile)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " from crontab")
  sys.exit(1)

os.system("/bin/rm -f " + cronfile)

print("INFO: Account " + userid + " crontab created")
print("INFO: Crontab creation complete")
sys.exit(0)
