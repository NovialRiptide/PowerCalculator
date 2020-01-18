from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sys
import urllib3
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

def convert_grade_to_gpa(grade, level):
    with open('gpa.json') as json_file:
        gpa_data = json.load(json_file)
    return float(gpa_data[level][grade])
def find_level(course_name):
    if "Accel" in course_name:
        return "honors"
    if "AP" in course_name:
        return "college"
    else:
        return "default"
    

class pypowerschool:
    """
    ONLY WORKS WITH MILLBURN'S POWERSCHOOL WEBSITE
    """
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.url_homepage = f"{self.url}/guardian/home.html"
        self.url_profile = f"{self.url}/guardian/accountmanagement_profile.html"
        self.url_school_info = f"{self.url}/guardian/schoolinformation.html"
        
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.get(self.url)
        userElem = self.browser.find_element_by_id("fieldAccount")
        passElem = self.browser.find_element_by_id("fieldPassword")

        userElem.send_keys(self.username)
        passElem.send_keys(self.password)
        passElem.submit()
    def get_student_name(self):
<<<<<<< HEAD
        name = self.html_homepage.xpath("/html/body/div[1]/div[4]/div[2]/h1/text()")
        name = name[0].replace("Grades and Attendance: ", "").split(", ")
=======
        self.browser.get(self.url_homepage)
        name = self.browser.find_element_by_xpath("//*[@id='content-main']/h1").text
        name = name.replace("Grades and Attendance: ", "")
        name = name.split(", ")
>>>>>>> parent of befdf4a... get_student_name() rewrite
        name = f"{name[1]} {name[0]}"

        return name
    def get_number_of_quarters(self):
        columns = int(len(self.browser.find_elements_by_tag_name("tr")))
        column_positions = []
        for column_number in range(columns):
            column_element = self.browser.find_elements_by_tag_name("tr")[column_number]
            column_positions.append(column_element.text)
        if "Q4" in column_positions[1]:
            return 4+2
        elif "Q3" in column_positions[1]:
            return 3
    def get_student_grades(self):
        courses = {}
        number_of_courses = int(len(self.browser.find_elements_by_tag_name("td"))/21)
        for course_number in range(number_of_courses-1):
            course_name = self.browser.find_elements_by_tag_name("td")[11+21*course_number].text
                
            # removes teacher's name
            course_name = course_name.split("\n")
            course_name = course_name[0]

            # adds course to a dictionary
            courses[course_number] = {"course_name": course_name, "grades": []}
            
            for grade_number in range(self.get_number_of_quarters()):
                course_grade = self.browser.find_elements_by_tag_name("td")[11+grade_number+21*course_number].text
                if "i" in course_grade:
                    pass
                elif "Rm" not in course_grade:
                    course_grade = course_grade.split("\n")
                    course_grade = course_grade[0]
                    courses[course_number]["grades"].append(course_grade)
        return courses
    def get_student_gpa(self): 
        # + 21 to the "td" tag name to go down a row
        # 11 is to get the class name
        # do not go after row 12
        self.browser.get(self.url_homepage)
        show_dropped_classes = self.browser.find_elements_by_xpath("/html/body/div[1]/div[4]/div[2]/div[3]/div/table[2]/tbody/tr/td/a")[0]
        show_dropped_classes.click()
        
        grades = self.get_student_grades()
        all_gpa_values = []
        with open('gpa.json') as json_file:
            gpa_data = json.load(json_file)
        if self.get_number_of_quarters() == 6:
            for quarter in range(4):
                course_counted = 0
                gpa = 0
                try:
                    for course in range(len(grades)):
                        try:
                            if grades[course]["grades"][quarter] != " ":
                                if "Phys Ed" not in grades[course]["course_name"]:
                                    course_gpa = convert_grade_to_gpa(grades[course]["grades"][quarter], find_level(grades[course]["course_name"]))
                                    course_counted += 1
                                    gpa = gpa + course_gpa
                        except IndexError:
                            pass
                    try:
                        all_gpa_values.append(gpa/course_counted)
                    except ZeroDivisionError:
                        pass
                except KeyError:
                    pass

        return all_gpa_values
        
    def get_school_name(self):
        self.browser.get(self.url_school_info)
        xpath = self.browser.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[3]/table[1]/tbody/tr[1]/td[2]")

        return xpath.text
    def end(self):
        self.browser.quit()