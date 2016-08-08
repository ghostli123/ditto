import pyshark
import threading
import Queue
import time
from collections import defaultdict 

from threading import Thread
import time
import random

from Queue import Queue
import glob
import os
import re

lock_merge = threading.Lock()
httpRequestQueue = Queue(-1)
httpResponse = Queue(-1)
dnsResponseQueue = Queue(-1)
smtpQueue = Queue(-1)
ftpQueue = Queue(-1)
writeToFile = open("log.txt","w")
#maxNumber = -1
maxNumberHttpRequestInQueue = -1
wocao = -100
flowNumber = 0
flowFlag = False
totalPcapNumber = 0
validPcapNumber = 0

finishSniffing = False
packetIndex = 0


def is_valid_ip(ip):
    """Validates IP addresses.
    """
    return is_valid_ipv4(ip)

def is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None


def hostnameTop2LevelDomain(hostname):
    if is_valid_ip(hostname):
        return hostname
    reverse = hostname[::-1]
    position = reverse.find('.')
    position2 = (reverse[position+1:]).find('.')
    if position2 == -1:
        return hostname
    top2 = reverse[:position+position2+1]
    return top2[::-1]

def log(str):
    writeToFile.writelines(str)
    writeToFile.flush()

def allFiles(path, filelist):
    for fn in glob.glob( path + os.sep + '*' ):
        if os.path.isdir( fn ):
            pass
        else:
            filelist.append(fn)

