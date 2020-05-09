# BBB Live Streaming

Streams a given BBB Meeting to an RTMP Server.

## Getting Started

### Prerequisites

All you need is Docker running on your machine and a media server to stream to.

### Configuration

You need to set some environment variables to run the container.

#### Required settings
* BBB_URL - URL to BBB including http/https e.g. https://your_BigBlueButton_server/bigbluebutton/api
* BBB_MEETING_ID - ID of the BBB Meeting (You can get the ID via an API call: https://your_bbb_server/bigbluebutton/api/getMeetings?checksum=<checksum>)
* BBB_SECRET - Secret of your BBB installation (You can get the secret with: bbb-conf --secret)
* BBB_STREAM_URL - Stream URL to your streaming server including rtmp. (e.g. rtmp://media_server_url/stream/stream_key)

#### Optional settings
* BBB_AS_MODERATOR - if set to "true" the meeting will be joined as moderator
* BBB_USER_NAME - the username to join the meeting. (Default: Live)

#### Chat settings
* BBB_ENABLE_CHAT - Enable Chat feedback channel
* BBB_REDIS_HOST - Set REDIS host (Default: redis)
* BBB_REDIS_CHANNEL - Set REDIS channel (Default: chat)
* BBB_CHAT_NAME - the username to join the meeting for chatting. (Default: Chat)

### Starting liveStreaming
* wget -O docker-compose.yml https://raw.github.com/aau-zid/BigBlueButton-liveStreaming/1.0.0-beta.2/examples/docker-compose.yml.example
* (change configuration)
* docker-compose up -d
* docker-compose down 

## Known Limitations
* You must extract and provide the meetingID, which is not visible within the room.
* ffmpeg settings to be improved
