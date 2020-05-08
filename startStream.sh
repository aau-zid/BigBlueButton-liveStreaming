#!/bin/sh

JOIN_AS_MODERATOR="";
if [ "${BBB_AS_MODERATOR}" = "true" ]
then
   JOIN_AS_MODERATOR="-m";
fi   

if [ "${BBB_ENABLE_CHAT}" = "true" ]
then
   xvfb-run -n 133 --server-args="-screen 0 1920x1080x24" python3 chat.py -s ${BBB_URL} -p ${BBB_SECRET} -i ${BBB_MEETING_ID} -r ${BBB_REDIS_HOST} -u ${BBB_CHAT_NAME} -c ${BBB_REDIS_CHANNEL} $JOIN_AS_MODERATOR &
   sleep 10
fi 

xvfb-run -n 122 --server-args="-screen 0 1920x1080x24" python3 stream.py -s ${BBB_URL} -p ${BBB_SECRET} -i ${BBB_MEETING_ID} -t ${BBB_STREAM_URL} -u ${BBB_USER_NAME} $JOIN_AS_MODERATOR;
