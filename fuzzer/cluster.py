#! /usr/bin/env python
# coding=utf8

import sys
import subprocess
import json

def main(argv):

    #Open the file containing list of core dumps
    coreDumps = open(argv[0],'r')

    configCoreFileDict = {}
    for line in coreDumps:
        line = line.strip()
        if line != "":
            tokens = line.split()
            configCoreFileDict[tokens[0].strip()] = tokens[1].strip()

    hexValDict = {}
    for key,value in configCoreFileDict.iteritems():
        coreStr = "core-file "+value
        p = subprocess.Popen(["gdb","/usr/bin/pdftotext","-batch", "-ex",coreStr,"-ex",'bt'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = p.communicate()
        hexVal = out.strip().split('\n')[-1].split()[1]
        if hexVal in hexValDict.keys():
            hexValDict[hexVal].append(key)
        else:
            keyList = []
            keyList.append(key)
            hexValDict[hexVal] = keyList

            #print "key : ",key, "Val : ", hexVal
    clusterDict = {}
    clusterDict["clusters"] = []

    for key,val in hexValDict.iteritems():
        clusterDict["clusters"].append(val)

    print json.dumps(clusterDict,indent = 4)

    #p.wait()
    #print "Out : ", out
    #p.terminate()


if __name__ == "__main__":
    main(sys.argv[1:])

