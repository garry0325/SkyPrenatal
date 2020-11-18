import time
import requests
import os

databaseIP='192.168.31.182'
idData=str(21006)
print "Recording..."
date=time.strftime("%Y%m%d",time.localtime())
audioFileName=idData+"-"+date+".wav"
recordScript="arecord -D hw:0,0 -d 5 -f cd "+audioFileName+" -c 1"
os.system(recordScript)
print "Recorded."
uploadURL='http://'+databaseIP+'/fetalSoundUpload.php'
files={'audioFile':open(audioFileName, 'rb')}
print "Uploading..."
req=requests.post(uploadURL,files=files)
print "Uploaded."
