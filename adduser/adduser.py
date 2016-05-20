#!/usr/bin/env python

import os
import pexpect
import random
import re
import string
import sys
import yaml
import ConfigParser

ssh = "/usr/bin/ssh -t"
sudo = "/usr/bin/sudo"

password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))

script = os.path.basename(__file__)
scriptpath = os.path.realpath(__file__)
basedir = os.path.dirname(scriptpath)
configfile = os.path.join(basedir, "." + re.sub("\.py$", "", script))
yamlfile = os.path.join("./", re.sub("\.py$", "", script) + ".yaml")

config = ConfigParser.RawConfigParser()
config.read(configfile)

print("INFO: Reading config file (" + configfile + ")")
try:
  slinux = config.get('servers', 'linux')
  print("INFO: Found linux account server (" + slinux + ")")
  plinux = config.get('scripts', 'linux')
  print("INFO: Found linux script (" + plinux + ")")
  skadmin = config.get('servers', 'kadmin')
  print("INFO: Found kerberos server (" + skadmin + ")")
  pkadmin = config.get('scripts', 'kadmin')
  print("INFO: Found kerberos script (" + pkadmin + ")")
  skeytab = config.get('servers', 'keytab')
  print("INFO: Found keytab server (" + skeytab + ")")
  pkeytab = config.get('scripts', 'keytab')
  print("INFO: Found keytab script (" + pkeytab + ")")
  scrontab = config.get('servers', 'crontab')
  print("INFO: Found crontab server (" + scrontab + ")")
  pcrontab = config.get('scripts', 'crontab')
  print("INFO: Found crontab script (" + pcrontab + ")")
  shdfs = config.get('servers', 'hdfs')
  print("INFO: Found HDFS server (" + shdfs + ")")
  phdfs = config.get('scripts', 'hdfs')
  print("INFO: Found HDFS script (" + phdfs + ")")
except:
  print("ERROR: Missing configuration record")
  sys.exit(1)

print("INFO: Reading yaml source (" + yamlfile + ")")
f = open(yamlfile)
yml = yaml.safe_load(f)
f.close()

print("INFO: Adding users")
print("INFO: " + str(len(yml['users'])) + " users to add")
print("INFO: Users added to " + str(len(yml['groups'])) + " groups")

groups = ""
for group in yml['groups']:
  groups = groups + group + ","

groups = groups[0:len(groups)-1]
print("INFO: Groups: " + groups)

for user in yml['users']:

  forename = user.split()[0]
  surname = user.split()[len(user.split())-1]
  userid = forename + surname
  userid = userid.lower()

  if user == "root" or userid == "root" or user == 0 or userid == 0:
    print("FATAL: Cannot modify the root user with this script")
    sys.exit(1)

  print("INFO: Adding " + userid + " (" + user + ")")

# Linux
#
  adduserlinux = plinux + " --user " + userid + " --groups " + groups
  cmd = ssh + " " + slinux + " " + sudo + " " + adduserlinux
  print("INFO: " + cmd)
  rc = os.system(cmd)
  if rc > 0:
    print("ERROR: Return code " + str(rc) + " adding linux user")
    sys.exit(1)

# Kerberos
#
  adduserkerb = pkadmin + " --user " + userid + " --password " + password
  cmd = ssh + " " + skadmin + " " + sudo + " " + adduserkerb
  print("INFO: " + cmd)
  rc = os.system(cmd)
  if rc > 0:
    print("ERROR: Return code " + str(rc) + " adding kerberos user")
    sys.exit(1)

# Keytab
#
  adduserkeytab = pkeytab + " --user " + userid + " --password " + password
  cmd = ssh + " " + skeytab + " " + sudo + " " + adduserkeytab
  print("INFO: " + cmd)
  rc = os.system(cmd)
  if rc > 0:
    print("ERROR: Return code " + str(rc) + " adding keytab")
    sys.exit(1)

# Crontab
#
  addusercron = pcrontab + " --user " + userid
  cmd = ssh + " " + scrontab + " " + sudo + " " + addusercron
  print("INFO: " + cmd)
  rc = os.system(cmd)
  if rc > 0:
    print("ERROR: Return code " + str(rc) + " adding crontab")
    sys.exit(1)

# HDFS
#
  adduserhdfs = phdfs + " --user " + userid
  cmd = ssh + " " + shdfs + " " + sudo + " -u hdfs " + adduserhdfs
  print("INFO: " + cmd)
  rc = os.system(cmd)
  if rc > 0:
    print("ERROR: Return code " + str(rc) + " adding hdfs")
    sys.exit(1)

# Fin
#
  print("INFO: Accounts and objects created for " + userid)

print("INFO: User creation complete")
sys.exit(0)
