__author__ = 'tomas'
import json
import urllib
import constants
students = []
studentsPresent = []
rfids = []
error = -1
maxstus = -1
def get_file():
    f = open('id.txt', 'w+')
    f.write(urllib.urlopen(constants.url).read())
    f.close

def init():
    get_file()
    file=open('id.txt')
    data = json.load(file)
    error = -1
    try:
        error = data['error']
        print error
    except:
        print "No Server Error!"
    if error == -1 and data[0]["attendees"] != None:
	for lists in range(0,len(data)):
	    
	    
            maxstus = data[lists]["maxstus"]
	    if data[lists]["attendees"] != None:
            	for i in range(len(data[lists]["attendees"])):
                    students.append(data[lists]["attendees"][i]["stu"]["name"])
	            rfids.append(data[lists]["attendees"][i]["stu"]["rfid"])
                    try:
                    	if data[lists]["attendees"][i]["attent"] == True:
                            studentsPresent.append("Aanwezig")
                    	else:
                            studentsPresent.append("Afwezig")
                    except:
                        studentsPresent.append("Afwezig")

        file.close()
    else:
        print error

def getMinTillStart():
    file= open('id.txt')
    data = json.load(file)
    min = data[0]["mintillstart"]
    file.close()
    return min






