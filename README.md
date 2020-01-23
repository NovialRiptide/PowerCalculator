// PowerCalculator 1.0.0
Designed & Developed by Andrew Hong (insta: @andrew_hong_)

Calculate your GPA without manually putting your grades in a calculator. In addition,
you can also check your tests and homework average by each course. The gpa scale being
used by this calculator is the 4.0 scale. 

This website uses the Python selenium API library to simulate a web browser to access
the client's PowerSchool account. This does not use the requests library to prevent
PowerSchool blocking the program's webscraping method. Although, it does use the lxml
API library to copy PowerSchool's HTML code to find xpaths faster. Flask is used to
host the actual server, which will later be replaced by a web-hosting service for
reliability.
