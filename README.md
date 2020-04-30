# BBB Live Streaming

Streams a given BBB Meeting to an RTMP Server.

## Getting Started

All you need is Docker running on your machine

### Running Docker

You need to set some environment variables to run the container.

#### Required
* BBB_URL - URL to BBB including http/https 
* BBB_MEETING_ID - ID of the BBB Meeting
* BBB_SECRET - Secret of your BBB installation
* BBB_STREAM_URL - Stream URL to your streaming server including rtmp.

#### Optional
* BBB_AS_MODERATOR - if set to "true" the meeting will joined as moderator
* BBB_USER_NAME - the Username to join the meeting. Default = Live