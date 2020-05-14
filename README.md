# BBB Live Streaming

Streams a given BBB Meeting to an RTMP Server.

*License:*   [GNU GPL v3 or later](http://www.gnu.org/copyleft/gpl.html)

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
* BBB_SHOW_CHAT - shows the chat on the left side of the window (Default: false)

#### Chat settings
* BBB_ENABLE_CHAT - Enable Chat feedback channel
* BBB_REDIS_HOST - Set REDIS host (Default: redis)
* BBB_REDIS_CHANNEL - Set REDIS channel (Default: chat)
* BBB_CHAT_NAME - the username to join the meeting for chatting. (Default: Chat)

### Starting liveStreaming
* wget -O docker-compose.yml https://raw.github.com/aau-zid/BigBlueButton-liveStreaming/1.0.0-beta.3/examples/docker-compose.yml.example
* (change configuration)
* docker-compose up -d
* docker-compose down 

## Known Limitations
* You must extract and provide the meetingID, which is not visible within the room.
* the streamer cannot join meetings, that where not started yet
* the streamer does not reconnect, if the connection to BigBlueButton gets lost
* when using breakoutrooms, the streamer will show the popup of the invitation and not be able to get back to the conference

## privacy policy and legal notes

Please try to follow best practices for data protection and privacy.
Take all steps to comply with privacy law principles that prohibit unlawful, opaque and limitless capture and processing of personal data. 

The GDPR (General Data Protection Regulation) provides individual rights to EU citizens in relation to personal Data.
To find out more about GDPR, please visit the [European Union’s website](https://ec.europa.eu).

The California Consumer Privacy Act (CCPA) provides certain rights to California residents in relation to their personal information. 

Similar to the GDPR and  the CCPA, other local privacy law principles  also may institute penalties for businesses that suffer data breaches due to poor security procedures.
Always be transparent and act upon privacy rights and federal law Regulations.

## License
    BigBlueButton-liveStreaming is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    BigBlueButton-liveStreaming is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with BigBlueButton-liveStreaming.  If not, see [GNU website](https://www.gnu.org/licenses)
