#!/usr/bin/env python
import hashlib
import sqlite3
from sys import argv
from platform import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if(system()=='Linux'):
    geckopath = 'gecko/geckodriver'
else: geckopath = 'gecko\geckodriver.exe'
conn = sqlite3.connect('lsdl.db')
c = conn.cursor()
dbrootpassw = c.execute("SELECT pass FROM lsdl WHERE login='root'").fetchall()[0][0]
login = ''
password = ''

def show_usage():
    print("example: script.py rootpass f")
    print("how to add account: script.py add f login pass")
    print("f    - login to your facebook account")
    print("g    - log in to your google account")
    print("chg  - change master password")
    print("add  - add account to lsdL database")
    print("rm    - remove account from database")
def browser():
    browser = webdriver.Firefox(executable_path=geckopath)
    return browser

def add_site_to_db(login, password, site):
    c.execute("INSERT INTO lsdl VALUES(?,?,?)", (login, password, site))
    conn.commit()
    conn.close()

def db_select_login(loginsite):
    global login
    global password
    login = c.execute("SELECT login FROM lsdl WHERE site=?", (loginsite,)).fetchall()[0][0]
    password = c.execute("SELECT pass FROM lsdl WHERE login=? AND site=?", (login, loginsite,)).fetchall()[0][0]

def change_password(newpassword):
    c.execute("UPDATE lsdl SET pass=? WHERE login='chuj'", (newpassword,))
    conn.commit()
    conn.close()

def fb_login(browser, null):
    browser.get('https://facebook.com')
    fmail = browser.find_element_by_id("email")
    fpass = browser.find_element_by_id("pass")
    fmail.send_keys(login)
    fpass.send_keys(password, Keys.ENTER)

#def google_login(browser):
 #   login = c.execute("SELECT login FROM lsdl WHERE site='g'").fetchall()[0][0]
 #   password = c.execute("SELECT pass FROM lsdl WHERE site='g' AND login=?", (login,)).fetchall()[0][0]
 #   browser.get('https://accounts.google.com')
 #   gmail = browser.find_element_by_id("identifierId")
 #   gmail.send_keys(login, Keys.ENTER)
 #   gpass = browser.find_element_by_xpath("//input[@jsname='YPqjbf']")
 #   gpass.send_keys(password, Keys.ENTER)

def hash_pass(password):
    hpass = hashlib.sha512(password).hexdigest()
    return hpass

masterPassword = argv[1].encode("utf-8")
if (hash_pass(masterPassword) == dbrootpassw):
    if (argv[2] == 'f'):
        fb_login(browser(), db_select_login(argv[2]))
    #elif (argv[2] == 'g'):
    #    google_login(browser())
    elif (argv[2] == 'chg'):
        change_password(hashlib.sha512(argv[3].encode()).hexdigest())
    elif (argv[2] == 'add'):
        add_site_to_db(argv[3], argv[4], argv[5])
    else: show_usage()
else:
    print("Bad master password! Try again")
