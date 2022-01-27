#!/bin/sh

. /usr/src/app/nsswrapper.sh

STREAM_MEETING="";
if [ "${BBB_STREAM_URL}" != "" ]
then
   STREAM_MEETING="-l -t ${BBB_STREAM_URL}";
fi 
 
CHAT_STREAM_MESSAGE="";
if [ "${BBB_CHAT_STREAM_MESSAGE}" != "" ]
then
   CHAT_STREAM_MESSAGE="--chatMsg ${BBB_CHAT_STREAM_MESSAGE}";
fi 

CHAT_STREAM_URL="";
if [ "${BBB_CHAT_STREAM_URL}" != "" ]
then
   CHAT_STREAM_URL="--chatUrl ${BBB_CHAT_STREAM_URL}";
fi 

DOWNLOAD_MEETING="";
if [ "${BBB_DOWNLOAD_MEETING}" = "true" ]
then
   DOWNLOAD_MEETING="-d";
fi 

SHOW_CHAT="";
if [ "${BBB_SHOW_CHAT}" = "true" ]
then
   SHOW_CHAT="-c";
fi

INTRO="";
if [ "${BBB_INTRO}" != "" ]
then
   INTRO="-I ${BBB_INTRO}";
fi 

BEGIN_INTRO="";
if [ "${BBB_BEGIN_INTRO_AT}" != "" ]
then
   BEGIN_INTRO="-B ${BBB_BEGIN_INTRO_AT}";
fi 

END_INTRO="";
if [ "${BBB_END_INTRO_AT}" != "" ]
then
   END_INTRO="-E ${BBB_END_INTRO_AT}";
fi 

START_MEETING="";
if [ "${BBB_START_MEETING}" = "true" ]
then
   START_MEETING="-S";
fi 

ATTENDEE_PASSWORD="";
if [ "${BBB_ATTENDEE_PASSWORD}" != "" ]
then
   ATTENDEE_PASSWORD="-A ${BBB_ATTENDEE_PASSWORD}";
fi 

MODERATOR_PASSWORD="";
if [ "${BBB_MODERATOR_PASSWORD}" != "" ]
then
   MODERATOR_PASSWORD="-M ${BBB_MODERATOR_PASSWORD}";
fi 

MEETING_TITLE="";
if [ "${BBB_MEETING_TITLE}" != "" ]
then
   MEETING_TITLE="${BBB_MEETING_TITLE}";
fi 

RESOLUTION="1920x1080"
if [ "${BBB_RESOLUTION}" != "" ]
then
   RESOLUTION="${BBB_RESOLUTION}"
fi

DEV_SHM_USAGE="";
if [ "${BROWSER_DISABLE_DEV_SHM_USAGE}" = "true" ]
then
   DEV_SHM_USAGE='--browser-disable-dev-shm-usage'
fi

if [ "${BBB_ENABLE_CHAT}" = "true" ]
then
   xvfb-run -n 133 --server-args="-screen 0 1280x720x24" python3 chat.py -s ${BBB_URL} -p ${BBB_SECRET} -i "${BBB_MEETING_ID}" -r ${BBB_REDIS_HOST} -u "${BBB_CHAT_NAME}" -c ${BBB_REDIS_CHANNEL} $START_MEETING $ATTENDEE_PASSWORD $MODERATOR_PASSWORD $DEV_SHM_USAGE -T "$MEETING_TITLE" &
   sleep 10
fi 

CUSTOM_STYLE="";
if [ "${BBB_CUSTOM_STYLE}" != "" ]
then
   CUSTOM_STYLE="${BBB_CUSTOM_STYLE}";
fi 

xvfb-run -n 122 --server-args="-screen 0 ${RESOLUTION}x24" python3 stream.py -s ${BBB_URL} -p ${BBB_SECRET} -i "${BBB_MEETING_ID}" -u "${BBB_USER_NAME}" -r "${RESOLUTION}" ${SHOW_CHAT} $START_MEETING $ATTENDEE_PASSWORD $MODERATOR_PASSWORD $DEV_SHM_USAGE -T "$MEETING_TITLE" --customStyle "$CUSTOM_STYLE" $STREAM_MEETING $CHAT_STREAM_URL $CHAT_STREAM_MESSAGE $INTRO $BEGIN_INTRO $END_INTRO $DOWNLOAD_MEETING;
