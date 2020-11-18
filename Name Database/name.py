import urllib2
import random
import time
url=urllib2.urlopen("https://www.behindthename.com/random/random.php?number=2&gender=both&surname=&all=no&usage_eng=1")


def getName():
	url=urllib2.urlopen("https://www.behindthename.com/random/random.php?number=2&gender=both&surname=&all=no&usage_eng=1")
	content=url.read()
	
	content=content[content.find("href=\"/name/"):]
	content=content[content.find(">")+1:]
	firstName=content[:content.find("<")]
	content=content[content.find("href=\"/name/"):]
	content=content[content.find(">")+1:]
	lastName=content[:content.find("<")]

	return firstName+" "+lastName

def getAge():
	return random.randint(18,50)

def getBlood():
	num=random.randint(0,3)
	if num==0:
		return "A"
	elif num==1:
		return "B"
	elif num==2:
		return "AB"
	elif num==3:
		return "O"

def getWeight():
	return random.randint(40,100)

def getPressure():
	sys=random.randint(80,200)
	dia=200
	while sys<=dia:
		dia=random.randint(40,150)
	return str(sys)+"|"+str(dia)


def getFetal():
	return random.randint(30,170)

def getDate():
	monthN=random.randint(1,12)
	dateN=random.randint(1,30)

	if monthN==1:
		month="January"
	elif monthN==2:
		month="February"
	elif monthN==3:
		month="March"
	elif monthN==4:
		month="April"
	elif monthN==5:
		month="May"
	elif monthN==6:
		month="June"
	elif monthN==7:
		month="July"
	elif monthN==8:
		month="August"
	elif monthN==9:
		month="September"
	elif monthN==10:
		month="October"
	elif monthN==11:
		month="November"
	else:
		month="December"

	return month+" "+str(dateN)



times=0
fileDatabase=open("index.txt","w")

dataDatabase=""

while times<100:
	#time.sleep()
	id=random.randint(21000,22000)
	
	
	file=open(str(id)+".txt","w")
	name=getName()
	print name
	
	dataDatabase=dataDatabase+str(id)+"|"+name+"|"
	
	age=getAge()
	blood=getBlood()

	data="|"+name+"|"+str(id)

	dataTimes=0
	
	while dataTimes<8:
		data=data+"|"+str(age)+"|"+str(blood)+"|"+str(getWeight())+"|"+str(getPressure())+"|"+str(getFetal())+"|"+getDate()
		dataTimes=dataTimes+1
	data=data+"|"

	file.write(data)
	file.close()

	times=times+1


fileDatabase.write(dataDatabase)
fileDatabase.close()
