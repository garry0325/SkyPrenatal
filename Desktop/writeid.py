import RPi.GPIO as GPIO
import MFRC522
import signal
import sys

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def toHex(s):
    lst = []
    for ch in s:
        hv = ord(ch)
        lst.append(hv)
    return lst

arguments=["","Name","Age","Blood","Last Test"]

signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()

legal=True
for a in range(1,len(sys.argv)-1):
    if len(sys.argv[a])>16:
        print "\""+sys.argv[a]+"\" should be less than 16 characters."
        legal=False
        break
if len(sys.argv)!=5:
    print "More or less arguments expected."
    legal=False

block=1
par=1
print "Now scanning..."

while legal and par<=len(sys.argv)-1:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    
    if status == MIFAREReader.MI_OK:

        print "Writing, do not leave card..."
        
        #print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
    
        # default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)

        if status == MIFAREReader.MI_OK:
  
            data=toHex(sys.argv[par])
            for x in range(len(data),16):
                data.append(0x00)

            # Write the data
            MIFAREReader.MFRC522_Write(block, data)
            
            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            par=par+1
            if (block+2)%4==0:
                block=block+2
            else:
                block=block+1
        else:
            print "Authentication error"

if par==len(sys.argv):
    for a in range(1,len(sys.argv)):
        print arguments[a]+": "+sys.argv[a]
    print "\nData written."
