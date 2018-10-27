#!/usr/bin/env python
# coding=utf-8

import sys, os
import re
import math
import json
from bs4 import BeautifulSoup
import time
import shutil
# import decimal
# import unicodedata


def checkForRequiredFilesAndUpdateJson(parentApp):
#In this function, the user will provide a valid path for both test appplications sys argv 1 and 2. 
#The program will the locate the files and proceed to edit the required lines needed to upload the new version and trigger the update
    for r, d, f in os.walk(parentApp):
        for files in f:
            if files == "manifest.json":
                manifest = os.path.join(parentApp, "manifest.json")

                jsonManifestFile = open(manifest, 'r')
                manifest_data = json.load(jsonManifestFile)
                jsonManifestFile.close()
                for key, value in manifest_data["kiosk"].iteritems():
                    if value != platform_version:
                    	manifest_data["kiosk"].update({'required_platform_version': platform_version})

                string_conversion = str(manifest_data['version'])
                split_1 = string_conversion[0:6]
                split_2 = string_conversion[6:]
                json_version_update =  (int(split_2) + 1)
                final_combo = str(split_1) + str(json_version_update)
                manifest_data.update({'version':final_combo})
                # code used for updating the edited file
                try:
                    jsonManifestFile = open(manifest,'w+')
                    jsonManifestFile.write(json.dumps(manifest_data, indent=4, sort_keys=True))
                    jsonManifestFile.close()
                except IOError as e:
                    print("could not open or write to file (%s)."% e) 
    print("Json write successful!")


def check_path_for_required_files(parentApp,required_files):
    for r,d,f in os.walk(parentApp):
        for files in f:
            if files == required_files[0]:
                print("found the manifest.json")
            if files == required_files[1]:
                print("found the document.html")
            return True
    return False

def checkForRequiredFilesAndUpdateHtml(parentApp):
#Now the program is opening and editing the html file to reflect the updated values given by the user
    html_doc = 'document.html'

    for r, d, f in os.walk(parentApp):
        print f
        for files in f:
            if files == "document.html":
                print 'found the html file'
                newPathdocument = os.path.join(parentApp,html_doc)
                html_document = open(newPathdocument,'r')
                soup = BeautifulSoup(html_document,'html.parser')
                print soup
          #       with open(newPathdocument,'r+') as document:
          #           print("file is opened")
    	    	# #document = open(newPathdocument,'r')
    	    	# #document.close()
          #           soup = BeautifulSoup(document,"html.parser")
          #           html_version_line = soup.find('div',{'id':'version'})
    	    	#     # stripped_html_version_line = html_version_line.text.strip
    	    	#     # print stripped_html_version_line
    	    	# #print type(stringHTML)
          #           rePattern = re.compile(r'\d\d\d\d\d\.?\d\d\.?\d')
          #           match = re.search(rePattern,str(html_version_line))
    	    	# #print ('stringHTML is', type(match))
          #           if match:
          #               print 'found the pattern. updating it with the platform_version you provided'
          #               html_version_line = re.sub(rePattern,platform_version,str(html_version_line))
          #               document.close()
          #               #print update_value
          #           #print soup
          #           #print soup
    	    	# 	    #print updated_string
          #               with open(newPathdocument,'wb') as file:
          #                   file.write(html_version_line)
            else:
                print "document.html file not found. Do you even have it in there?"
                sys.exit()
    	    		#print "looks good"
    	    		#print soup

    	    		#print updated_string

def navigate_file_struct(parentApp):
    pass

def zip_both_directories(mikeApp):
#check if existing zip files with the same app name exist. If they do, rename the files. this should work on linux only.
    extension = '.zip'
    zipped_apps = []
    x = ''
    dst = str(time + extension)
    for r,d,f in os.walk(mikeApp):
        for items in f:
            if items.endswith(extension):
            	#os.rename(items,dst)
            	confirmed_zips = os.path.join(mikeApp,items)
                zipped_apps.append(confirmed_zips)
    for items in zipped_apps:
        
    	shutil.copyfile(items,os.path.join(dst,mikeApp))
    	print x
    print x

def main():
	#zip_both_directories(sys.argv[1])
    #checkForRequiredFilesAndUpdateJson(sys.argv[1])
	checkForRequiredFilesAndUpdateHtml(sys.argv[1])


if __name__ == "__main__":
#Error checking against user answers
    user_path = ()
    time = time.strftime('%a%H:%M:%S')
    required_files = ["manifest.json","document.html"]
    release_channel = int(input('Please select the build\n1. dev\n2. beta \n3. stable \n\nchoice: '))
    release_dict = {1:'dev',2:'beta',3:'stable'}
    user_channel = ''

    while release_channel not in release_dict:
        print "answer is not a valid. Try again: \n"
        release_channel = int(input('Please select the build\n1. dev\n2. beta \n3. stable \n\nchoice: '))

    for key, value in release_dict.iteritems():
        if release_channel == key:
        	user_channel = value

    platform_version = raw_input(("Please enter platform version currently being served by \nomaha E.G 10574.48.0: "))
    while len(platform_version) < 10:
    	print("oops did you forget to add the decimals?\n")
        platform_version = raw_input(("Please enter platform version currently being served by \nomaha E.G 10574.48.0: "))
    
    main()