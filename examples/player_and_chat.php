<head>
  <link href="https://vjs.zencdn.net/7.6.5/video-js.css" rel="stylesheet">
  <script
  src="https://code.jquery.com/jquery-3.5.1.min.js"
  integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0="
  crossorigin="anonymous"></script>

  <!-- If you'd like to support IE8 (for Video.js versions prior to v7) -->


</head>

<body>

    <h1>Live Stream</h1>
    <div style="float:left; width:49%">
  <video id='my-video-live' class="video-js vjs-default-skin" width='760' height='400'>
        <source src="LIVE_STREAM_URL">
      <p class='vjs-no-js'>
        To view this video please enable JavaScript, and consider upgrading to a web browser that
        <a href='http://videojs.com/html5-video-support/' target='_blank'>supports HTML5 video</a>
      </p>
    </video>
    </div>
    <div id="container" style=" float:right; width:49%">
    <form method="post" action="" id="contactform">
      <div class="form-group">
        <h2 >Send Question</h2>
        <textarea name="message" rows="15" cols="60" class="form-control" id="message"></textarea>
      </div>
      <button type="submit" class="btn btn-primary send-message">Submit</button>
    </form>
    </div>

  <script src='https://vjs.zencdn.net/7.6.6/video.js'></script>
  <script type="application/javascript">
    

    $(document).ready(function () {
        $('.send-message').click(function (e) {
        e.preventDefault();
        var message = $('#message').val();
        $.ajax
            ({
            type: "POST",
            url: "sendChatMessage.php",
            data: { "message": message },
            success: function (data) {
                $('#contactform')[0].reset();
            }
            });
        });
    });


    </script>

</body>