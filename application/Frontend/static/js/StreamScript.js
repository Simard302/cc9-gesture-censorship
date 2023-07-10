const form = document.querySelector("form"),
video = document.querySelector("video");

function startup(){
  console.log("Startup");
  navigator.mediaDevices.getUserMedia({
    audio:false,
    video:
    {
      width: { min: 1024, ideal: 1280, max: 1920 },
      height: { min: 576, ideal: 720, max: 1080 },
      frameRate: { ideal: 10, max: 15 },
    }
  }).then(stream => {
    video.srcObject = stream;
    console.log("Stream Set");

    // Start streaming to Django REST API
    var apiEndpoint = 'api/stream';
    var mediaRecorder = new MediaRecorder(stream);
    var frameCount = 0;
    var chunks = [];

    console.log("Variables Set");

    mediaRecorder.ondataavailable = function (e) {
      console.log(`Frame Count: ${frameCount}`);

      chunks.push(e.data);
      frameCount++;

      if (frameCount === 15) {
        mediaRecorder.stop();
      }
    };

    mediaRecorder.onstop = function () {
      var blob = new Blob(chunks, { type: 'video/webm' });
      var formData = new FormData();
      formData.append('video', blob, 'stream.webm');

      // Send the video blob to Django REST API using fetch
      fetch(apiEndpoint, {
        method: 'POST',
        body: formData
      })
        .then(function (response) {
          console.log('Video uploaded successfully!');
          frameCount = 0;
          chunks = [];
          setTimeout(startRecording,1);
        })
        .catch(function (error) {
          console.error('Error uploading video:', error);
          frameCount = 0;
          chunks = [];
          setTimeout(startRecording,1); // Delay for 1 second before starting the next recording
        });
    };

    function startRecording() {
      if (mediaRecorder.state !== 'recording') {
        mediaRecorder.start(10);
      }
    }

    // Start recording the video stream
    startRecording();
  })

  .catch(function (error) {
    console.error('Error accessing camera:', error);
  });
}

window.addEventListener('load',startup, false);


