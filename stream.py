#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse, time, subprocess, shlex, logging, os, re

from bigbluebutton_api_python import BigBlueButton, exception
from bigbluebutton_api_python import util as bbbUtil 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from datetime import datetime
import time

browser = None
selenium_timeout = 30
connect_timeout = 5

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO' if not os.environ.get('DEBUG') else 'DEBUG'))

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", help="Big Blue Button Server URL")
parser.add_argument("-p","--secret", help="Big Blue Button Secret")
parser.add_argument("-i","--id", help="Big Blue Button Meeting ID")
parser.add_argument("-I","--intro", help="Intro file to play before streaming")
parser.add_argument("-B","--beginIntroAt", help="begin intro at position (e.g. 00:01:05)")
parser.add_argument("-E","--endIntroAt", help="End intro at position (e.g. 01:00:04)")
parser.add_argument("-l","--stream", help="live stream a BigBlueButton meeting",action="store_true")
parser.add_argument("-d","--download", help="download / save a BigBlueButton meeting",action="store_true")
parser.add_argument("-S","--startMeeting", help="start the meeting if not running",action="store_true")
parser.add_argument("-A","--attendeePassword", help="attendee password (required to create meetings)")
parser.add_argument("-M","--moderatorPassword", help="moderator password (required to create a meeting)")
parser.add_argument("-T","--meetingTitle", help="meeting title (required to create a meeting)")
parser.add_argument("-u","--user", help="Name to join the meeting",default="Live")
parser.add_argument("-t","--target", help="RTMP Streaming URL")
parser.add_argument("--chatUrl", help="Streaming URL to display in the chat", default=False)
parser.add_argument("--chatMsg", nargs='+', help="Message to display in the chat before Streaming URL", default=False)
parser.add_argument("-c","--chat", help="Show the chat",action="store_true")
parser.add_argument("-r","--resolution", help="Resolution as WxH", default='1920x1080')
parser.add_argument('--ffmpeg-stream-threads', help='Threads to use for ffmpeg streaming', type=int,
                    default=os.environ.get('FFMPEG_STREAM_THREADS', '') or 0)
parser.add_argument('--ffmpeg-stream-video-bitrate', help='Video birate to use for ffmpeg streaming (in k)', type=int,
                    default=os.environ.get('FFMPEG_STREAM_VIDEO_BITRATE', '') or 4000)
parser.add_argument(
    '--ffmpeg-stream-options',
    help='ffmpeg stream options (can be set using env FFMPEG_STREAM_OPTIONS)',
    default=os.environ.get('FFMPEG_STREAM_OPTIONS', '') or '\
        -c:a aac -b:a 160k -ar 44100 \
        -threads "$FFMPEG_STREAM_THREADS" \
        -c:v libx264 -x264-params "nal-hrd=cbr" -profile:v high -level:v 4.2 -vf format=yuv420p \
        -b:v "${FFMPEG_STREAM_VIDEO_BITRATE}k" -maxrate "${FFMPEG_STREAM_VIDEO_BITRATE}k" -minrate "${FFMPEG_STREAM_VIDEO_BITRATE/2}k" -bufsize "${FFMPEG_STREAM_VIDEO_BITRATE*2}k" -g 60 \
        -preset ultrafast \
        ')
parser.add_argument(
    '--ffmpeg-download-options',
    help='ffmpeg download options (can be set using env FFMPEG_DOWNLOAD_OPTIONS)',
    default=os.environ.get('FFMPEG_DOWNLOAD_OPTIONS', '') or '-c:v libx264rgb -crf 0 -preset ultrafast'
)
parser.add_argument(
    '--ffmpeg-input-thread-queue-size',
    type=int,
    help='ffmpeg thread_queue_size options to be applied to all inputs (can be set using env)',
    default=os.environ.get('FFMPEG_INPUT_THREAD_QUEUE_SIZE', '1024')
)
parser.add_argument(
   '--browser-disable-dev-shm-usage', action='store_true', default=False,
   help='do not use /dev/shm',
)

args = parser.parse_args()
# some ugly hacks for additional options
args.ffmpeg_stream_options = args.ffmpeg_stream_options.replace(
   '$FFMPEG_STREAM_THREADS', str(args.ffmpeg_stream_threads),
).replace(
   '${FFMPEG_STREAM_VIDEO_BITRATE}', str(args.ffmpeg_stream_video_bitrate),
).replace(
   '${FFMPEG_STREAM_VIDEO_BITRATE/2}', str(args.ffmpeg_stream_video_bitrate // 2),
).replace(
   '${FFMPEG_STREAM_VIDEO_BITRATE*2}', str(args.ffmpeg_stream_video_bitrate * 2),
)

bbb = BigBlueButton(args.server,args.secret)
bbbUB = bbbUtil.UrlBuilder(args.server,args.secret)

def set_up():
    global browser

    assert re.fullmatch(r'\d+x\d+', args.resolution)

    options = Options()  
    options.add_argument('--disable-infobars') 
    options.add_argument('--no-sandbox') 
    options.add_argument('--kiosk') 
    options.add_argument('--window-size=%s' % args.resolution.replace('x', ','))
    options.add_argument('--window-position=0,0')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('prefs', {'intl.accept_languages':'{locale}'.format(locale='en_US.UTF-8')})
    options.add_argument('--start-fullscreen') 
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    if args.browser_disable_dev_shm_usage:
        options.add_argument('--disable-dev-shm-usage')
    else:
        dev_shm_size = int(subprocess.run('df /dev/shm/ --block-size=1M --output=size | tail -n 1', shell=True, stdout=subprocess.PIPE).stdout or '0')
        required_dev_shm_size = 500  # in MB, 1024MB is recommended
        if dev_shm_size < required_dev_shm_size:
            logging.error(
                'The size of /dev/shm/ is %sMB (minimum recommended is %sMB), '
                'consider increasing the size of /dev/shm/ (shm-size docker parameter) or disabling /dev/shm usage '
                '(see --browser-disable-dev-shm-usage or BROWSER_DISABLE_DEV_SHM_USAGE env variable).',
                dev_shm_size, required_dev_shm_size
            )
            sys.exit(2)

    logging.info('Starting browser!!')

    browser = webdriver.Chrome(executable_path='./chromedriver',options=options)

def bbb_browser():
    global browser
    logging.info('Open BBB and hide elements!!')
    if args.startMeeting is True:
        try:
            logging.info("create_meeting...")
            create_meeting()
        except exception.bbbexception.BBBException as ERR:
            logging.info(ERR)
    logging.info("get_join_url...")
    join_url = get_join_url()
    logging.info(join_url)
    browser.get(join_url)


    try:
        # Wait for the input element to appear
        logging.info("Waiting for chat input window to appear.")
        element = EC.presence_of_element_located((By.ID, 'message-input'))
        WebDriverWait(browser, selenium_timeout).until(element)

        element = browser.find_element_by_id('message-input')
        chat_send = browser.find_elements_by_css_selector('[aria-label="Send message"]')[0]
        # ensure chat is enabled (might be locked by moderator)
        if element.is_enabled() and chat_send.is_enabled():
           tmp_chatMsg = os.environ.get('BBB_CHAT_MESSAGE', "This meeting is streamed to")
           tmp_chatCustomMsg = os.environ.get('BBB_CHAT_CUSTOM_MESSAGE', "This meeting is streamed to")
           if not tmp_chatMsg in [ 'false', 'False', 'FALSE' ]:
               if args.target is not None:
                   tmp_chatUrl = args.target.partition('//')[2].partition('/')[0]
                   if args.chatUrl:
                       tmp_chatUrl = args.chatUrl
                   if args.chatMsg:
                       tmp_chatMsg = ' '.join(args.chatMsg).strip('"')
                   tmp_chatMsg = "{0}: {1}".format(tmp_chatMsg, tmp_chatUrl)
               elif tmp_chatCustomMsg != '':
                   tmp_chatMsg = tmp_chatCustomMsg
               else:
                   tmp_chatMsg = "Recording in progress!"
               
               element.send_keys(tmp_chatMsg)
               chat_send.click()

        if args.chat:
            try:
                browser.execute_script("document.querySelector('[aria-label=\"User list\"]').parentElement.style.display='none';")
            except JavaScriptException:
                browser.execute_script("document.querySelector('[aria-label=\"Users list\"]').parentElement.style.display='none';")
        else:
            element = browser.find_elements_by_id('chat-toggle-button')[0]
            if element.is_enabled():
                element.click()
    except NoSuchElementException:
        # ignore (chat might be disabled)
        logging.info("could not find chat input or chat toggle")
    except ElementClickInterceptedException:
        # ignore (chat might be disabled)
        logging.info("could not find chat input or chat toggle")

    time.sleep(10)
    if not args.chat:
        try:
            element = browser.find_elements_by_css_selector('button[aria-label^="Users and messages toggle"]')[0]
            if element.is_enabled():
                element.click()
        except NoSuchElementException:
            logging.info("could not find users and messages toggle")
        except ElementClickInterceptedException:
            logging.info("could not find users and messages toggle")
 
    try:
        browser.execute_script("document.querySelector('[aria-label=\"Users and messages toggle\"]').style.display='none';")
    except JavascriptException:
        browser.execute_script("document.querySelector('[aria-label=\"Users and messages toggle with new message notification\"]').style.display='none';")
    browser.execute_script("document.querySelector('[aria-label=\"Options\"]').style.display='none';")
    browser.execute_script("document.querySelector('[aria-label=\"Actions bar\"]').style.display='none';")
    try:
        browser.execute_script("document.getElementById('container').setAttribute('style','margin-bottom:30px');")
    except JavascriptException:
        browser.execute_script("document.getElementById('app').setAttribute('style','margin-bottom:30px');")

def create_meeting():
    create_params = {}
    if args.moderatorPassword:
        create_params['moderatorPW'] = args.moderatorPassword
    if args.attendeePassword:
        create_params['attendeePW'] = args.attendeePassword
    if args.meetingTitle:
        create_params['name'] = args.meetingTitle
    return bbb.create_meeting(args.id, params=create_params)

def get_join_url():
    minfo = bbb.get_meeting_info(args.id)
    pwd = minfo.get_meetinginfo().get_attendeepw()
    joinParams = {}
    joinParams['meetingID'] = args.id
    joinParams['fullName'] = args.user
    joinParams['password'] = pwd
    joinParams['userdata-bbb_auto_join_audio'] = "true" 
    joinParams['userdata-bbb_enable_video'] = 'true' 
    joinParams['userdata-bbb_listen_only_mode'] = "true" 
    joinParams['userdata-bbb_force_listen_only'] = "true" 
    joinParams['userdata-bbb_skip_check_audio'] = 'true' 
    joinParams['joinViaHtml5'] = 'true'
    return bbbUB.buildUrl("join", params=joinParams) 

def stream_intro():
    introBegin = ""
    if args.beginIntroAt:
        introBegin = "-ss %s"%(args.beginIntroAt)
    introEnd = ""
    if args.endIntroAt:
        introEnd = "-to %s"%(args.endIntroAt)
    ffmpeg_stream = 'ffmpeg -re %s %s -thread_queue_size "%s" -i %s -thread_queue_size %s -f pulse -i default -ac 2 %s -f flv "%s"' % (
        introBegin, introEnd, args.ffmpeg_input_thread_queue_size, args.intro, args.ffmpeg_input_thread_queue_size, args.ffmpeg_stream_options, args.target
    )
    logging.debug('Preparing to execute %r' % ffmpeg_stream)
    ffmpeg_args = shlex.split(ffmpeg_stream)
    logging.info("streaming intro...")
    p = subprocess.call(ffmpeg_args)

def stream():
    ffmpeg_outputs = []

    if args.download:
        downloadFile = "/video/meeting-%s.mkv" % fileTimeStamp
        ffmpeg_outputs.extend(shlex.split(args.ffmpeg_download_options))
        ffmpeg_outputs.append(downloadFile)
        logging.info("saving meeting as %s" % downloadFile)

    if args.stream:
        ffmpeg_outputs.extend(shlex.split(args.ffmpeg_stream_options))
        ffmpeg_outputs.extend([
            "-f", "flv",
            "-flvflags", "no_duration_filesize",
            args.target,
        ])
        logging.info("streaming meeting...")

    ffmpeg_cmd = [
        "ffmpeg",
        "-thread_queue_size", str(args.ffmpeg_input_thread_queue_size),
        "-f", "x11grab",
        "-draw_mouse", "0",
        "-s", args.resolution,
        "-i", ":122",
        "-thread_queue_size", str(args.ffmpeg_input_thread_queue_size),
        "-f", "pulse",
        "-i", "default",
        "-ac", "2",
    ] + ffmpeg_outputs

    logging.debug('Preparing to execute %r' % ffmpeg_cmd)
    p = subprocess.call(ffmpeg_cmd)

if args.startMeeting is False:
    while bbb.is_meeting_running(args.id).is_meeting_running() != True:
        logging.info("Meeting isn't running. We will try again in %d seconds!" % connect_timeout)
        time.sleep(connect_timeout)

# current date and time
now = datetime.now()
fileTimeStamp = now.strftime("%Y%m%d%H%M%S")

set_up()
if args.stream and args.intro:
    stream_intro()
if args.stream or args.download:
    bbb_browser()
    stream()
if browser:
    browser.quit()
