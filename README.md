# Recipe App - Command Line Version

## Overview
The Recipe App - Command Line Version is a simple app that allows the user to create recipes, store them in a local MySQL database, view, edit, and search recipes by ingredients as well as delete recipes. It is built with Python, MySQL, and SQLAlchemy. The app is fully controled via terminal. 

In this repository, the final application is stored in the `Achievement1\Exercise 1.7` folder. The resources in the other folders (Exercise 1.1 - 1.6) document the learning progress and partial deliverables leading to the final version.

## Installation & Execution
### Prerequisites
1. [Python 3.8.7](https://www.python.org/downloads/release/python-387/) is used for this project, make sure you have this version installed. 
2. Install a virtual environment wrapper extension unless you have one on your system already. For Mac & Linux, it is for example the `virtualenvwrapper` extenstion: `pip3.8 install virtualenvwrapper`
3. Create a new virtual environment, such as: `mkvirtualenv recipe-app-base` 
4. Install the required dependencies in your new environment, using the `Achievement1/requirements.txt` file: `pip install -r requirements.txt`
5. [Download](https://dev.mysql.com/downloads/mysql/) and install MySQL on your computer and check that your MySQL server is running (It depends on the OS you are using, for MacOS, open Spotlight Search with Command + Space, search for Preferences, and open it. You’ll find MySQL at the bottom. Open it up and you should see green icons beside your MySQL instances.)
6. Then open your terminal and through mysql, [set up a new user](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql) for MySQL. Grant all permissions to this user. For host, use `localhost` and for user and password select your values.
7. Still in the mysql command line interface, create a new database: `CREATE DATABASE database_name`

### Clone Repository
Clone the entire repository first:
```
git clone https://github.com/vdevhub/python-spec.git
```

### Database Connection Setup
Open the project in your chosen IDE, such as VSCode. In `python-spec/Achievement1/Exercise 1.7/1.7-Task/`, you'll have to create a new file `.env` and update it with your values as follows:

```
DBMS = 'mysql'
USER_NAME = '<your_db_user_name>'
PASSWORD = '<password_for_the_user>'
HOST = 'localhost'
DATABASE = '<database_name>'
```

Use the user name, password, and database name you created when setting up your MySQL using the guidance in the `Prerequisites` section (or another MySQL user and database you had used before and want to use for this app too).

### Change Directory
Then, in the terminal, navigate to the last exercise's task folder:
```
cd python-spec/Achievement1/Exercise\ 1.7/1.7-Task/
```

And run the app:
```
python recipe_app.py
```
