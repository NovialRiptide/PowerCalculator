from flask import Flask
from flask import render_template
from flask import request

from selenium.common.exceptions import NoSuchElementException

import pyps

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login_page():
    gpa = None
    
    if request.method == 'POST':
        usr = request.form['username']
        pwd = request.form['password']
        
        try:
            school = pyps.pypowerschool(usr, pwd, "https://ps2.millburn.org")
        except:
            return render_template("homepage.html")
        student_name = school.get_student_name()
        gpa = school.get_student_gpa()
        name = school.get_student_name()
        school.end()
        return render_template("infopage.html", student_gpa=gpa, student_name=name)
    return render_template("homepage.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80, threaded=True)
