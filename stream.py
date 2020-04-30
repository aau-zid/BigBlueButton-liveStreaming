#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse, time, subprocess, shlex, logging, os

from bigbluebutton_api_python import BigBlueButton

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

browser = None
timeout = 5

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", help="Big Blue Button Server URL")
parser.add_argument("-p","--secret", help="Big Blue Button Secret")
parser.add_argument("-i","--id", help="Big Blue Button Meeting ID")
parser.add_argument("-m","--moderator", help="Join the meeting as moderator",action="store_true")
parser.add_argument("-u","--user", help="Name to join the meeting",default="Live")
parser.add_argument("-t","--target", help="RTMP Streaming URL")
args = parser.parse_args()

bbb = BigBlueButton(args.server,args.secret)

def set_up():
    global browser

    options = Options()  
    #options.set_headless(headless=True)
    #options.add_argument("--headless")
    #options.add_argument('--enable-logging=stderr')
    #options.add_argument('--disable-gpu') 
    #options.add_argument('--enable-usermedia-screen-capturing') 
    #options.add_argument('--allow-http-screen-capture') 
    #options.add_argument('--auto-select-desktop-capture-source=bbbrecorder') 
    options.add_argument('--disable-infobars') 
    options.add_argument('--no-sandbox') 
    options.add_argument('--kiosk') 
    options.add_argument('--window-size=1280,720')
    options.add_argument('--window-position=0,0')
    options.add_experimental_option("excludeSwitches", ['enable-automation']);   
    #options.add_argument('--shm-size=1gb') 
    #options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--start-fullscreen') 
    
    logging.info('Starting browser!!')

    browser = webdriver.Chrome(executable_path='./chromedriver',options=options)

def bbb_browser():
    global browser

    logging.info('Open BBB and hide elements!!')
    browser.get(get_join_url())
    element = EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Listen only"]'))
    WebDriverWait(browser, timeout).until(element)
    browser.find_elements_by_css_selector('[aria-label="Listen only"]')[0].click()

    element = EC.invisibility_of_element((By.CSS_SELECTOR, '.ReactModal__Overlay'))
    WebDriverWait(browser, timeout).until(element)
    browser.find_elements_by_id('chat-toggle-button')[0].click()
    browser.find_elements_by_css_selector('button[aria-label="Users and messages toggle"]')[0].click()

def get_join_url():
    minfo = bbb.get_meeting_info(args.id)
    if args.moderator:
        pwd = minfo.get_meetinginfo().get_moderatorpw()
    else:
        pwd = minfo.get_meetinginfo().get_attendeepw()
    return bbb.get_join_meeting_url(args.user,args.id,pwd)

def watch():
    while True:
        time.sleep(60)

def stream():
    logging.info('Starting Stream with cmd: ffmpeg -fflags +igndts -f x11grab -s 1280x720 -r 24 -draw_mouse 0 -i :%d -f alsa -i pulse -ac 2 -preset ultrafaset -crf 0 -pix_fmt yuv420p -s 1280x720 -c:a aac -b:a 160k -ar 44100 -threads 0 -f flv "%s"' % (122, args.target))
    ffmpeg_stream = 'ffmpeg -fflags +igndts -f x11grab -s 1280x720 -r 24 -draw_mouse 0 -i :%d -f alsa -i pulse -ac 2 -preset ultrafaset -pix_fmt yuv420p -s 1280x720 -c:a aac -b:a 160k -ar 44100 -threads 0 -f flv "%s"' % (122, args.target)
    ffmpeg_args = shlex.split(ffmpeg_stream)
    p = subprocess.Popen(ffmpeg_args)



while bbb.is_meeting_running(args.id).is_meeting_running() != True:
    logging.info("Meeting isn't running. We will try again in %d seconds!" % timeout)
    time.sleep(timeout)
set_up()
bbb_browser()
stream()
watch()
browser.quit()