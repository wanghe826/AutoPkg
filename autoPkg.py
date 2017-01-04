#!/usr/bin/python

'''
@date 2016-12-30
'''

'''scheme default is the workspace prefix '''

import os
import shutil

def createPlist(isEnterprise, method):
    fp = os.open("/Users/wanghe/Desktop/AutoPkg.plist",os.O_CREAT|os.O_RDWR|os.O_APPEND)
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



workPath = "/Users/wanghe/Documents/ADPlatform/"
try:
    os.system("cd %s" % workPath)
except IOError:
    print("no such directory")
    sys.exit()


workFiles = os.listdir(workPath)
print(workFiles)
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
        os.system("cd %s; xcodebuild -configuration Release -archivePath %s -exportArchive -exportPath ~/Desktop/ExportPath/ -exportOptionsPlist %s" % (workPath, xcarchiveFilePath, createPlist(True,"development")))      #if error with no applicable device , you can run shell 'rvm system'
