from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    from lxml import html
    from lxml import etree
    from bs4 import BeautifulSoup
except:
    print("Lxml or BeautifulSoup is not installed.")
    
import sys
import urllib3
import json
import string
import re
import math

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

def convert_grade_to_gpa(grade, level):
    with open('gpa.json') as json_file:
        gpa_data = json.load(json_file)
    return float(gpa_data[level][grade])
def find_level(course_name):
    if " Accel" in course_name:
        return "honors"
    if "AP " in course_name:
        return "college"
    else:
        return "default"
    

class pypowerschool:
    """ONLY WORKS WITH MILLBURN'S POWERSCHOOL WEBSITE"""
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.get(self.url)
        userElem = self.browser.find_element_by_id("fieldAccount")
        passElem = self.browser.find_element_by_id("fieldPassword")

        userElem.send_keys(self.username)
        passElem.send_keys(self.password)
        passElem.submit()

        show_dropped_classes = self.browser.find_elements_by_xpath("/html/body/div[1]/div[4]/div[2]/div[3]/div/table[2]/tbody/tr/td/a")[0]
        show_dropped_classes.click()

        self.html_homepage = self.__copy(self.browser.current_url)
        self.browser.get(self.browser.current_url)
        self.url_homepage = self.browser.current_url
        self.bs4_homepage = BeautifulSoup(self.browser.page_source, "lxml")
    def __copy(self, url):
        output = self.browser.get(url)
        output = html.fromstring(self.browser.page_source)
        return output
    def get_student_name(self):
        name = self.html_homepage.xpath("/html/body/div[1]/div[4]/div[2]/h1/text()")
        name = name[0].replace("Grades and Attendance: ", "").split(", ")
        name = f"{name[1]} {name[0]}"
        return name
    def get_number_of_quarters(self):
        columns = int(len(self.bs4_homepage.find_all("tr")))
        column_positions = []
        for column_number in range(columns):
            column_element = self.bs4_homepage.find_all("tr")[column_number]
            column_positions.append(column_element.text)
        if "Q4" in column_positions[1]:
            return 4+2
        elif "Q3" in column_positions[1]:
            return 3
    def get_student_grades(self):
        # + 21 to the "td" tag name to go down a row
        # 11 is to get the class name
        # do not go after row 12
        courses = []
        course_counted = 0
        number_of_courses = int(len(self.bs4_homepage.find_all("td"))/21)
        for course_number in range(number_of_courses-1):
            course_name = repr(self.bs4_homepage.find_all("td")[11+21*course_number].get_text())
            if "Physical Education" in course_name or "Phys Ed" in course_name:
                pass
            else:
                # removes teacher's name
                course_name = course_name.split("\'")
                course_name = course_name[1]
                course_name = course_name.split("\\xa0")
                course_name = course_name[0]
                # adds course to a dictionary
                courses.append({"course_name": course_name, "grades": []})
                
                for grade_number in range(self.get_number_of_quarters()):
                    course_grade = self.bs4_homepage.find_all("td")[11+grade_number+21*course_number].get_text()
                    if " i " in course_grade:
                        pass
                    elif "Rm" not in course_grade:
                        if repr(course_grade) == "\'\\xa0\'":
                            courses[course_counted]["grades"].append("")
                        else:
                            course_grade = re.split('(\d+)',course_grade)
                            course_grade = course_grade[0]
                            courses[course_counted]["grades"].append(course_grade)
                course_counted += 1
        return courses
    def get_student_gpa(self):
        grades = self.get_student_grades()
        all_gpa_values = []
        with open('gpa.json') as json_file:
            gpa_data = json.load(json_file)
        if self.get_number_of_quarters() == 6:
            # finds gpa for each quarter
            for quarter in range(4):
                course_counted = 0
                gpa = 0
                try:
                    # finds gpa for 1 course
                    for course in range(len(grades)):
                        try:
                            if grades[course]["grades"][quarter] != "":
                                course_gpa = convert_grade_to_gpa(grades[course]["grades"][quarter], find_level(grades[course]["course_name"]))
                                course_counted += 1
                                gpa = gpa + course_gpa
                        except IndexError:
                            pass
                    try:
                        # finds gpa average (unweighted)
                        gpa_average = (gpa/course_counted)
                        output = math.ceil(gpa_average*100) / 100
                        all_gpa_values.append(output)
                    except ZeroDivisionError:
                        pass
                except KeyError:
                    pass
        return all_gpa_values
    def end(self):
        self.browser.quit()
