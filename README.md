# LMSUNSW

### Utilising Wireless Devices in Lecture-Based Education

LMSUNSW has been developed as part of a thesis project by Jason Huang and Sheryl Shi.

#### Abstract

Student interactions are limited within a traditional lecture environment and as modern day progresses, the overall quality of the students' learning experience decreases.

This thesis will examine and determine the different methods for increasing student interactions in a traditional lecture based environment through the use of technology.

A system based on the design and implementation of a web application that would utilise the use of wireless devices present. This system provides lecturers with the ability to actively engage student learning with technology used within a lecture environment.

This repo is a prototype implemented solution used to investigate and evaluate utilising wireless based devices to augment the lecture teaching model.

Thesis documents:

<a href="https://github.com/sixthshift/lmsunsw/blob/master/docs/Thesis%20A%20Report.pdf">Thesis A Report</a>

<a href="https://github.com/sixthshift/lmsunsw/blob/master/docs/Thesis%20B%20Report.pdf">Thesis B Report</a>
# Setup

This app has been configured to run on AWS Elastic Beanstalk.

There are some settings configuration made so that it will function with AWS.

If you are using AWS, an RDS and Memcached is also used.

To setup the app, you will need to create a virtualenv to run the app

when you have run the git clone command, run 'virtualenv env' to create an env folder alongside the lmsunsw repo

type 'source env/bin/activate' to set the env into PATH.

cd into lmsunsw and run 'pip install -r requirements.txt' to configure the env with packages

run 'python manage.py runserver' to start the webserver locally
