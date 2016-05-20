#!/usr/bin/env python

import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--userid", help="Userid", required=True)
args = parser.parse_args()

userid = args.userid

if userid == "root" or userid == 0:
  print("FATAL: Cannot modify the root user with this script")
  sys.exit(1)

print("INFO: Setting up HDFS home directory for " + userid)

print("INFO: Renewing kerberos ticket")
rc = os.system("/usr/bin/kinit -kt hdfs.headless.keytab hdfs")
if rc > 0:
  print("ERROR: Return code " + str(rc) + " renewing kerberos token")
  sys.exit(1)

print("INFO: Making home directory")
rc = os.system("/usr/bin/hdfs dfs -mkdir -p /user/" + userid)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " from mkdir")
  sys.exit(1)

print("INFO: Changing owner")
rc = os.system("/usr/bin/hdfs dfs -chown " + userid + " /user/" + userid)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " from chown")
  sys.exit(1)

print("INFO: Setting permissions")
rc = os.system("/usr/bin/hdfs dfs -chmod 700 /user/" + userid)
if rc > 0:
  print("ERROR: Return code " + str(rc) + " from chmod")
  sys.exit(1)

print("INFO: Account " + userid + " HDFS home directory created")
print("INFO: User creation complete")
sys.exit(0)
