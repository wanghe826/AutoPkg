#!/usr/bin/python

'''
@date 2016-12-30
'''

'''scheme default is the workspace prefix '''

import os
import sys
import shutil
import getopt

def createPlist(isEnterprise, method):
    fp = os.open("%s/Desktop/AutoPkg.plist" % (os.path.expanduser("~")),os.O_CREAT|os.O_RDWR|os.O_APPEND)
    if fp != None:
        os.write(fp,"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        os.write(fp,"<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
        os.write(fp,"<plist version=\"1.0\">\n")
        os.write(fp,"<dict>\n")
        # method
        os.write(fp,"<key>method</key>\n")
        os.write(fp,"<string>%s</string>\n" % method)
        # uploadSymbols
        os.write(fp,"<key>uploadSymbols</key>\n")
        os.write(fp,"<false/>\n")
        # uploadBitcode
        os.write(fp,"<key>uploadBitcode</key>\n")
        os.write(fp,"<false/>\n")
        # compileBitcode
        os.write(fp,"<key>compileBitcode</key>\n")
        os.write(fp,"<true/>\n")
        # embedOnDemandResourcesAssetPacksInBundle
        os.write(fp,"<key>embedOnDemandResourcesAssetPacksInBundle</key>\n")
        os.write(fp,"<true/>\n")
        # iCloudContainnerEnvironment
        os.write(fp,"<key>iCloudContainnerEnvironment</key>\n")
        os.write(fp,"<true/>\n")
        os.write(fp,"</dict>\n")
        os.write(fp,"</plist>\n")
        os.close(fp)
        return "~/Desktop/AutoPkg.plist"

def printMsg(type,msg):
    if type == 1:       #Error
        print("\033[1;31;40m")
        print("Error: %s" % msg)
        print("\033[0m")
    elif type == 2:     #Warning
        print("\033[1;33;40m")
        print("Warning: %s" % msg)
        print("\033[0m")


workPath = None      # project  path
ipaOutputPath = None    #ipa output path

opts, args = getopt.getopt(sys.argv[1:], "i:o:")
for op, value in opts:
    if op == "-i":
        workPath = value
    elif op == "-o":
        ipaOutputPath = value
if workPath == None:
    printMsg(1,"You shuold specify the workPath use -i options!")
    sys.exit()

try:
    os.system("cd %s" % workPath)
except IOError:
    printMsg(1, "No such path was found !")
    sys.exit()
if ipaOutputPath == None:
    printMsg(2, "The default ipa output path is Desktop if you doesn't appoint it.")
    ipaOutputPath = "~/Desktop"

workFiles = os.listdir(workPath)
workspaceName = None
projectName = None

for eachFile in workFiles:
    if "xcworkspace" in eachFile:
        workspaceName = eachFile
        break

if workspaceName != None:
    scheme = workspaceName.split(".")[0]
    xcarchiveFilePath = "%sbuild/%s.xcarchive" % (workPath, scheme)
    ret = os.system("cd %s; xcodebuild clean; xcodebuild -workspace %s -scheme %s -configuration Release -archivePath %s archive" % (workPath, workspaceName, scheme, xcarchiveFilePath))
    if ret == 0:
        os.system("cd %s; xcodebuild -configuration Release -archivePath %s -exportArchive -exportPath %s -exportOptionsPlist %s" % (workPath, xcarchiveFilePath, ipaOutputPath,createPlist(True,"development")))
             #if error with no applicable device , you can run shell 'rvm system'
             
        os.system("rm -rf %sbuild/" % workPath)
