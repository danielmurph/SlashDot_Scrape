__author__ = ''

import mechanize
from bs4 import BeautifulSoup
import datetime
import re
import time

#Function to convert time from page to a timestamp.
def convert_timestamp(date_time):
    date_time = date_time.split(' ', 1)[1]
    date_time = date_time.split(' ', 1)[1]
    date_time = date_time.split('@', 1)
    date2 = date_time[0] + date_time[1]
    timestamp = time.mktime(time.strptime(date2, '%B %d, %Y %I:%M%p'))
    return timestamp





logins = 3
can_continue = 0
results = []
article_dates = []

#This will try to login three times before exiting, asking for a new username and password each time
while logins > 0:

    user_nickname = raw_input('Username:')
    user_password = raw_input('Password:')

    print 'Attempting to login...'

    browser = mechanize.Browser()

    #Open SlashDots login page
    browser.open('https://slashdot.org/my/login')

    #Select login form on page
    browser.select_form(nr=1)

    #Enter logon details to form and submit.
    browser.form['unickname'] = user_nickname
    browser.form['upasswd'] = user_password

    response = browser.submit()
    html = response.read()
    soup = BeautifulSoup(html)

    #Search for error class on page that indicates whether logging in was successful or not
    login_error = 'None'
    try:
        login_error = soup.find(class_='error').text.strip()
    except:
        pass
    login_error_suc = soup.find(class_='error')

    if 'Danger, Will Robinson!' in login_error:
        print login_error
        logins -= 1

    #If login was successful it will break out of the login loop.
    elif login_error_suc is None:
        can_continue = 1
        print 'Login successful!'
        break

if can_continue == 1:
    user_timestamp = str(raw_input('Please enter a timestamp (2014-04-31 20:10):'))

#Try converting the entered date and time
    try:
        user_timestamp = time.mktime(time.strptime(user_timestamp, '%Y-%m-%d %H:%M'))
    except TypeError:
        print 'Invalid timestamp entered.'
        exit()
    except ValueError:
        print 'Invalid timestamp entered.'
        exit()

    print 'Fetching headlines...'
    next_page = soup.find(class_='prevnextbutact')['href']

    while True:
        article_list = soup.find(id='firehoselist')
        #num_articles = len(article_list.find_all(class_='story'))
        article_details = article_list.find_all(class_='details')

        #Gets HTML for article headlines
        article_headlines = article_list.find_all(class_='story')
        break_condition = 0

        #Loops through articles and adds the details to a dictionary, then that dictionary to a list
        for i, j in zip(article_headlines, article_details):

            dict = {'headline': '', 'author': '', 'date': ''}

            headline = i.find('a').text.strip()
            author = j.find('a').text.strip()
            date_time = j.find('time').text.strip()
            timestamp = convert_timestamp(date_time)
            if int(timestamp) <= int(user_timestamp):
                break_condition = 1
                break
            dict['headline'] = headline
            dict['author'] = author
            dict['date'] = int(timestamp)
            results.append(dict)

        if break_condition == 1:
            break

        response = browser.open(next_page)
        html = response.read()
        soup = BeautifulSoup(html)

        #Gets link for the next(older) page
        elems = soup.select('div.menu a')
        for i in elems:
            #if i.text is 'Older &raquo;':
            if 'Older' in i.text:
                #print i.attrs['href']
                next_page = i.attrs['href']
                break


for i in results:
    print i
