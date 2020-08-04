from flask import Flask, jsonify, request, send_from_directory, abort
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
import json
import shutil
import os
import glob

from bs4 import BeautifulSoup
app = Flask(__name__)


@app.route('/')
def hello():
    username = '190905191'
    password = '2001@Billion'

    chrome_options = Options()
    chrome_options.add_argument('headless')
    # To Remove chrome from popping up, Uncomment the previous line
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9191')
    browser = webdriver.Chrome(
        "/Users/srathakjha/Desktop/MTTN-SLCM-Notices/chromedriver")

    # Login
    browser.get('https://slcm.manipal.edu/')
    user_bar = browser.find_element_by_name('txtUserid')
    print(user_bar)
    pass_bar = browser.find_element_by_name('txtpassword')
    login_btn = browser.find_element_by_name('btnLogin')
    user_bar.send_keys(username)
    pass_bar.send_keys(password)
    login_btn.click()
    time.sleep(5)

    # Open Notices
    browser.get('https://slcm.manipal.edu/ImportantDocuments.aspx')
    page = 1
   # contentTitles = []
    contentTitleDict = []
    k = 0
    while(page < 5):
        time.sleep(5)
       # page = page + 1
        table = browser.find_element_by_id('ContentPlaceHolder1_grvDocument')
        tra = table.find_elements_by_tag_name('tr')
        tra = tra[1:]
        page_row = tra[len(tra)-1]
        two_button = page_row.find_elements_by_tag_name('td')
        tra = tra[:len(tra)-2]
        for i in tra:
            k = k+1
            downloadbtn = i.find_element_by_tag_name('a')
            source = i.get_attribute('innerHTML')
            tr = BeautifulSoup(source, 'html.parser')
            all_td = tr.find_all('td')
            index = all_td[0].text.strip()
            name = all_td[1].text.strip()
            link = all_td[2].find('a')['href']
            titleDict = {
                "title": name,
                "index": int(index),
                "page": page
            }
            print(k)
            contentTitleDict.append(titleDict)
        nextl = two_button[page].find_element_by_tag_name('a')
        nextl.click()
        page = page + 1
    return jsonify({
        "contentTitles": contentTitleDict,
        "contentLength": len(contentTitleDict)
    })


# sends specific pdf

@app.route('/getpdf/<int:page>/<file_name>', methods=['GET'])
def getPDF(file_name, page):
    print(page)
    pdfRoute = "/Users/srathakjha/Desktop/flask_slcm_MTTN/notices/" + \
        str(page)
    print(pdfRoute)
    try:
        print("sending pdf")
        return send_from_directory(pdfRoute, filename=file_name, as_attachment=False)
    except:
        print("aborting")
        abort(404)


if __name__ == '__main__':
    app.run()
