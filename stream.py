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
selelnium_timeout = 30
connect_timeout = 5

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", help="Big Blue Button Server URL")
parser.add_argument("-p","--secret", help="Big Blue Button Secret")
parser.add_argument("-i","--id", help="Big Blue Button Meeting ID")
parser.add_argument("-m","--moderator", help="Join the meeting as moderator",action="store_true")
parser.add_argument("-u","--user", help="Name to join the meeting",default="Live")
parser.add_argument("-t","--target", help="RTMP Streaming URL")
parser.add_argument("-c","--chat", help="Show the chat",action="store_true")
args = parser.parse_args()

bbb = BigBlueButton(args.server,args.secret)

def set_up():
    global browser

    options = Options()  
    options.add_argument('--disable-infobars') 
    options.add_argument('--no-sandbox') 
    options.add_argument('--kiosk') 
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--window-position=0,0')
    options.add_experimental_option("excludeSwitches", ['enable-automation']);   
    options.add_argument('--shm-size=1gb') 
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--start-fullscreen') 
    
    logging.info('Starting browser!!')

    browser = webdriver.Chrome(executable_path='./chromedriver',options=options)

def bbb_browser():
    global browser

    logging.info('Open BBB and hide elements!!')
    browser.get(get_join_url())
    element = EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Listen only"]'))
    WebDriverWait(browser, selelnium_timeout).until(element)
    browser.find_elements_by_css_selector('[aria-label="Listen only"]')[0].click()

    element = EC.invisibility_of_element((By.CSS_SELECTOR, '.ReactModal__Overlay'))
    WebDriverWait(browser, selelnium_timeout).until(element)
    browser.find_element_by_id('message-input').send_keys("This meeting will be stream to the following address: %s" % args.target)
    browser.find_elements_by_css_selector('[aria-label="Send message"]')[0].click()
    
    if args.chat:
        browser.execute_script("document.querySelector('[aria-label=\"User list\"]').parentElement.style.display='none';")
    else:
        browser.find_elements_by_id('chat-toggle-button')[0].click()
        browser.find_elements_by_css_selector('button[aria-label="Users and messages toggle"]')[0].click()
        
    browser.execute_script("document.querySelector('[aria-label=\"Users and messages toggle\"]').style.display='none';")
    browser.execute_script("document.querySelector('[aria-label=\"Options\"]').style.display='none';")
    browser.execute_script("document.querySelector('[aria-label=\"Actions bar\"]').style.display='none';")
    browser.execute_script("document.getElementById('container').setAttribute('style','margin-bottom:30px');")

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
    audio_options = '-f alsa -i pulse -ac 2 -c:a aac -b:a 160k -ar 44100'
    #video_options = ' -c:v libvpx-vp9 -b:v 2000k -crf 33 -quality realtime -speed 5'
    video_options = '-c:v libx264 -x264-params "nal-hrd=cbr" -profile:v high -level:v 4.2 -vf format=yuv420p -b:v 4000k -maxrate 4000k -minrate 2000k -bufsize 8000k -g 60 -preset ultrafast -tune zerolatency'
    ffmpeg_stream = 'ffmpeg -thread_queue_size 1024 -f x11grab -draw_mouse 0 -s 1920x1080  -i :%d %s -threads 0 %s -f flv -flvflags no_duration_filesize "%s"' % ( 122, audio_options, video_options, args.target)
    ffmpeg_args = shlex.split(ffmpeg_stream)
    p = subprocess.Popen(ffmpeg_args)



while bbb.is_meeting_running(args.id).is_meeting_running() != True:
    logging.info("Meeting isn't running. We will try again in %d seconds!" % connect_timeout)
    time.sleep(connect_timeout)
set_up()
bbb_browser()
stream()
watch()
browser.quit()