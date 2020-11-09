# Changelog #

## v1.0.0-beta7 ##

- add resolution option in `BBB_RESOLUTION`
- add additional debug info is `DEBUG` env variable is set
- remove zerolatency from ffmpeg options
- export ffmpeg options to env variables
  - `FFMPEG_STREAM_THREADS`
  - `FFMPEG_STREAM_VIDEO_BITRATE`
  - `FFMPEG_INPUT_THREAD_QUEUE_SIZE`
  - `FFMPEG_STREAM_OPTIONS`
  - `FFMPEG_DOWNLOAD_OPTIONS`
