from bs4 import BeautifulSoup
import urllib2
from easygui import *
import winsound
import threading
import sys
import time
import smtplib

DEPARTMENTS = ["CS" , "EEE", "HUM","MATH", "IE"]

def get_course_quota(department_code, course_key, isAvailable=False):
    """course_key can be the instructor or coursename or coursecode"""

    ##CONSTANTS##    
    COURSE_QUOTA_AVAILABLE = -1
    COURSE_CODE = 1
    COURSE_NAME = 2
    COURSE_INSTRUCTOR = 3
    COURSE_CREDIT = 4
    #COURSE_CREDIT_ECTS = 5
    COURSE_INFO = 6

    offerings_url = "https://stars.bilkent.edu.tr/homepage/print/plainOfferings.php?COURSE_CODE=" + DEPARTMENTS[department_code] + "&SEMESTER=20161"
    offerings = urllib2.urlopen(offerings_url).read()
    soup = BeautifulSoup(offerings)

    tbody = soup.find("tbody")
    rows = tbody.find_all('tr')
    course_data_list = []

    for row in rows:
        course_data_list.append((row.text).splitlines())


    # Finds the target courses and available sections
    target_courses = []
    target_courses_available = []
    for course in course_data_list:
        if course_key.lower() in course[COURSE_NAME].lower() : #or course[COURSE_CODE] or  course[COURSE_INSTRUCTOR].lower() 
            target_courses.append(course)
    
    if len(target_courses) == 0:
        print "Course Not Found!"

    target_courses_string = ""    
    for course in target_courses:
        target_courses_string +=course[COURSE_NAME] + " " + course[COURSE_CODE] + " :" + course[COURSE_INFO][COURSE_QUOTA_AVAILABLE] + "\n"
        if int(course[COURSE_INFO][COURSE_QUOTA_AVAILABLE]) > 0:            
            target_courses_available.append(course)
            isAvailable = True



    return {'target_courses_string':target_courses_string, 'target_courses_available':target_courses_available, 'isAvailable':isAvailable } 

def query():
 
    # TODO: Get input from user and allow multiple queries simultaneously
    list_of_target_courses = [] 
    #list_of_target_courses.append(getCourseQuota(0, "computer network"))
    list_of_target_courses.append(getCourseQuota(4, "Engineering Management"))
   
    # quota > 0
    for course in list_of_target_courses:
        if course["isAvailable"] == True:
            print "available quota... sending email..."
            send_mail(course["target_courses_string"])
            sys.exit()

    threading.Timer(30, query).start()
   

def send_mail(msg):
    fromaddr = ''
    toaddrs  = ''

    # Credentials (if needed)
    username = ''
    password = ''

    
    # The actual mail send
    server = smtplib.SMTP('smtp.live.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
   

def main():
    query()

    
if __name__ == "__main__": main()




        
        
    
