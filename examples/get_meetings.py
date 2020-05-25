#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### to use this script you will need to ###
# apt install pip3
# pip3 install bigbluebutton_api_python
# pip3 install pyyaml

import argparse, sys, os, logging, yaml, urllib, json
from bigbluebutton_api_python import BigBlueButton

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", help="Big Blue Button Server URL")
parser.add_argument("-c","--config", help="path to config file in yaml format e.g. your docker-compose.yml", default="./docker-compose.yml")
parser.add_argument("-u","--user", help="fullName to use for joinUrls of showMeetings command", default="system administrator")
parser.add_argument("-p","--secret", help="Big Blue Button Secret")
args = parser.parse_args()

def get_config_item(list_item):
    try:
        with open(args.config) as file:
            config = yaml.load(file)
    except FileNotFoundError as ERR:
        logging.error(ERR)
        sys.exit()

    docker_environment = config['services']['bbb-streamer']['environment']
    for line in docker_environment:
        if line.strip().startswith(list_item):
            return line.partition('=')[2]

def get_join_url(id, name, role='attendee', pw=None):
    pwd = None
    if pw:
        pwd = pw
    elif bbb.get_meeting_info(id):
        minfo = bbb.get_meeting_info(id)
        if role == 'moderator':
            pwd = minfo.get_meetinginfo().get_moderatorpw()
        elif role == 'attendee':
            pwd = minfo.get_meetinginfo().get_attendeepw()
    if pwd:
        return bbb.get_join_meeting_url(name, id, pwd)

def get_meetings():
    logging.info("fetching meetings from {}".format(args.server))
    try:
        return bbb.get_meetings()
    except urllib.error.URLError as ERR:
        logging.error(ERR)
        sys.exit()

if args.server != None and args.secret != None:
    logging.info("using server and password provided")
elif args.config:
    logging.info("using server and password from config file")
    args.server = get_config_item('BBB_URL')
    args.secret = get_config_item('BBB_SECRET')
else:
    logging.error("Error: Please specify server and password or the path to the config file")
    sys.exit()

def get_meetings(server):
    logging.info("fetching meetings from {}".format(server))
    try:
        meetingsXML = bbb.get_meetings()
        if meetingsXML.get_field('returncode') == 'SUCCESS':
            if  meetingsXML.get_field('meetings') == '':
                logging.info("no meetings running on {}".format(server))
                return []
            else:
                rawMeetings = meetingsXML.get_field('meetings')['meeting']
                if isinstance(rawMeetings, list):
                    logging.info("meetings found on {}".format(server))
                    return json.loads(json.dumps(rawMeetings))
                else:
                    logging.info("meeting found on {}".format(server))
                    return [json.loads(json.dumps(rawMeetings))]
        else:
            logging.error("api request failed")
            return []
    except urllib.error.URLError as ERR:
        logging.error(ERR)
        return []

def find_meeting(server, title):
    meetings = get_meetings(server)
    for meeting in meetings:
        if title in meeting['meetingName']:
            meeting['joinAttendeeUrl'] = get_join_url(meeting['meetingID'], args.user, 'attendee')
            meeting['joinModeratorUrl'] = get_join_url(meeting['meetingID'], args.user, 'moderator')
            return meeting

def show_meetings(server):
    meetings = get_meetings(server)
    for meeting in meetings:
        print(meeting['meetingName'])
        print("ID: {}".format(meeting['meetingID']))
        print("ATTENDEE_PASSWORD: {}".format(meeting['attendeePW']))
        joinAttendeeUrl = get_join_url(meeting['meetingID'], args.user, 'attendee')
        print("JOIN_ATTENDEE_URL: {}".format(joinAttendeeUrl))
        print("MODERATOR_PASSWORD: {}".format(meeting['moderatorPW']))
        joinModeratorUrl = get_join_url(meeting['meetingID'], args.user, 'moderator')
        print("JOIN_MODERATOR_URL: {}".format(joinModeratorUrl))
        print("")


bbb = BigBlueButton(args.server,args.secret)
show_meetings(args.server)
