#!/usr/bin/python
#---------------------------------------
# ovpn-to-certificates.py
# (c) Jansen A. Simanullang
# 27.03.2016 13:26
#---------------------------------------
# usage: python ovpn-to-certificates.py
#
# example:
# python ovpn-to-certificates.py
#
# features:
# grab ovpn files and create certificates
# ca.crt, client.crt, client.key
#

import os, re, sys

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = "."

path = os.path.abspath(os.path.expanduser(path)) + '/'



def fileFilter(path, fileExtension):

  dirContents  = os.listdir(path)
  selectedFiles = []
  
  count = 0

  for filename in dirContents:

    if fileExtension in filename:
    
      print filename.strip()
      
      count = count + 1
      
      selectedFiles.append(path+filename)
      
  print "\nThere are ", count, fileExtension + " files\n\n"

  return selectedFiles
  

  
def replaceBetweenTag(tagName, fileContents, fn):
  tagRegEx = re.compile('<'+tagName+'>.*\n(^.*$.*\n[\S\n]+.*$\n)</'+tagName+'>', re.MULTILINE)
  newContents = tagRegEx.sub("%s %s" % (tagName, fn), fileContents)
  return newContents

def grabBetweenTag(tagName, fileContents):

  betweentag = re.findall('<'+tagName+'>.*\n(^.*$.*\n[\S\n]+.*$\n)</'+tagName+'>', fileContents, re.MULTILINE)

  if len(betweentag) > 0:
      return betweentag[0]
  else:
      return None
  
 

def fileCreate(strNamaFile, strData):
  #--------------------------------
  # fileCreate(strNamaFile, strData)
  # create a text file
  #
  try:
  
    f = open(strNamaFile, "w")
    f.writelines(str(strData))
    f.close()
  
  except IOError:
  
    strNamaFile = strNamaFile.split(os.sep)[-1]
    f = open(strNamaFile, "w")
    f.writelines(str(strData))
    f.close()
    
  print "file created: " + strNamaFile + "\n"
  
  
  
def readTextFile(strNamaFile):

  f = open(strNamaFile, "r")
  
  print "file being read: " + strNamaFile + "\n"
  
  return f.read()
  


def ovpnToCertificate(strNamaFile):

  fileContents = readTextFile(strNamaFile)
  
  strData = ""
  
  tagFile = {
      'ca':'ca.crt',
      'cert':'client.crt',
      'crl-verify': 'crl.pem',
      'key':'client.key'
      }
  
  for tag, file in tagFile.iteritems():
  
    tagData = grabBetweenTag(tag, fileContents)
    destFn = "%s-%s" % (os.path.basename(strNamaFile).replace(".ovpn",""), file)

    fileContents = replaceBetweenTag(tag, fileContents, destFn)

    if tagData:
        strData = strData + tagData
        
        print tag, destFn
        
        fileCreate(destFn, strData)

  fileCreate(os.path.relpath(strNamaFile).replace(".ovpn", "") + ".conf", fileContents)
  
  
def main():

  fileExtension = ".ovpn"
  
  selectedFiles = fileFilter(path, fileExtension)

  for files in selectedFiles:
    
    ovpnToCertificate(files)

  
main()
