#!/usr/bin/env python

"""
Cookie Cutter post generation hook

Initialise git
   Add source code files into git

Create Virtualenv
"""
from __future__ import print_function

import os, sys, shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
TEST_REQ_PATH = os.path.join(PROJECT_DIRECTORY,"test_requirements.txt")
REQ_PATH = os.path.join(PROJECT_DIRECTORY,"requirements.txt")
LICENSE_PATH = os.path.join(PROJECT_DIRECTORY,"LICENSE.rst")

def create_django_project():
    print("\n-------------------------------------")
    print("Creating Django project\n")
    with open('error.txt','w') as error:
    subprocess.call([ '/bin/bash', '-i', '-c', 'workon', '{{cookiecutter.project_repo}}35', ';','django-admin', 'startproject', '{{cookiecutter.project_repo}}', '..'], shell=True,
             stdout=sys.stdout,
             stderr=error)

def apply_license():
    """ Rename appropriate license file, and delete un needed files"""

    license_files={"MIT":"MIT License", "GNU GPL v3.0":"GNU GPL v3.0 License", "Apache Software License 2.0":"Apache Software License 2.0"}

    print("\n-------------------------------------")
    print("Apply chosen license")
    
    for li_name, li_file in license_files.iteritems():
        if li_name == "{{cookiecutter.license}}":
            os.rename(os.path.join(PROJECT_DIRECTORY,li_file), 
                      LICENSE_PATH )
        else:
            os.remove(os.path.join(PROJECT_DIRECTORY,li_file))

def apply_git():
    """Apply the relevant files to git, and create github as required"""

    # Initialise and add files to the git repository
    print("\n--------------------------------------")
    print("Initialising git & github remote repo - {{cookiecutter.project_repo}}")
    os.system( "git init .")
    os.system( "git add {}/*".format(PROJECT_DIRECTORY))
    os.system( "git add *" )

    # Perform initial commit project files
    print("\n--------------")
    print("Initial commit")
    os.system( "git commit -m 'Initial commit with cookiecutter create' >/dev/null")

    # create github repository and link local repository

    print("\n---------------------------")
    print( "Creating remote repository")
    os.system( "git remote add origin {{cookiecutter.project_ghurl}} >/dev/null")
    os.system( "curl -u '{{cookiecutter.author_username}}' https://api.github.com/user/repos -d '{\"name\":\"{{cookiecutter.project_repo}}\",\"description\":\"{{cookiecutter.project_desc}}\"}' >/dev/null")
    os.system( "git push -u origin master" )

def apply_virtualenv():
    print("\n-----------------------")
    print("Initialising virtualenv")
    print("Creating Python 3.5 environment")
    subprocess.call(['/bin/bash', '-i', '-c', "mkvirtualenv -r '{test_req}' -p /usr/bin/python3.5 {{cookiecutter.project_repo}}35".format(test_req=TEST_REQ_PATH)],
         stdout=sys.stdout,
         stderr=subprocess.STDOUT)
    subprocess.call(['/bin/bash', '-i', '-c', 'setvirtualenvproject {virtual_env} {project_path}'.format(
                        virtual_env='$WORKON_HOME/{{cookiecutter.project_repo}}35',
                        project_path=PROJECT_DIRECTORY)],
         stdout=sys.stdout,
         stderr=subprocess.STDOUT)
    print("Creating Python 3.6 environment")
    subprocess.call(['/bin/bash', '-i', '-c', "mkvirtualenv -r '{test_req}' -p /usr/bin/python3.6 {{cookiecutter.project_repo}}36".format(test_req=TEST_REQ_PATH)],
         stdout=sys.stdout,
         stderr=subprocess.STDOUT)
    subprocess.call(['/bin/bash', '-i', '-c', 'setvirtualenvproject {virtual_env} {project_path}'.format(
                        virtual_env='$WORKON_HOME/{{cookiecutter.project_repo}}36',
                        project_path=PROJECT_DIRECTORY)],
         stdout=sys.stdout,
         stderr=subprocess.STDOUT)

def add_bug_reporting():
    """Add the Bug reporting section to the README.rst"""
    section = """
Every care is taken to try to ensure that this code comes to you bug free.
If you do find an error - please report the problem on :
`GitHub <{{cookiecutter.project_gh}}>`_
or
by email to : `{{cookiecutter.author}} <mailto:{{cookiecutter.author_email}}?Subject={{cookiecutter.project_repo}}%20Error>`_
""".split("\n")

    max_len = max(map(len,section))
    max_len = max_len + (max_len % 2)

    with open(os.path.join(PROJECT_DIRECTORY,"README.rst"), "a") as readme:
        readme.write("+" + "-"*max_len + "+\n")
        readme.write("|" + " "*(max_len/2-2) + "Bugs" + " "*(max_len/2-2) + "+\n")
        readme.write("+" + "="*max_len + "+\n")
        for l in section:
            readme.write("|" + l + " "*(max_len-len(l)) + "|\n")
        readme.write("+" + "-"*max_len + "+\n")

apply_license()

add_bug_reporting()

apply_virtualenv()

create_django_project()

apply_git()
