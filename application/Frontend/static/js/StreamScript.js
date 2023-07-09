
// function startup(){
//   console.log("Startup");
//   navigator.mediaDevices.getUserMedia({
//     audio:false,
//     video:true
//     // {
//     //   width: { min: 1024, ideal: 1280, max: 1920 },
//     //   height: { min: 576, ideal: 720, max: 1080 },
//     //   frameRate: { ideal: 10, max: 15 },
//     // },
//   })  
//   .then(stream => {
//     console.log("in then");
//     video.srcObject = stream;
//     // Create a WebSocket connection to the server
//     var socket = new WebSocket('ws://localhost:8000/api/stream/');
      
//     // Send each video frame and camera information to the server
//     var mediaRecorder = new MediaRecorder(stream);
//     mediaRecorder.ondataavailable = function(event) {
//       if (socket.readyState === WebSocket.OPEN) {
//         var cameraInfo = {
//           resolution: {
//             width: video.videoWidth,
//             height: video.videoHeight
//           },
//           // Add any additional camera information here
//         };
        
//         var data = {
//           cameraInfo: cameraInfo,
//           videoFrame: event.data
//         };
        
//         socket.send(JSON.stringify(data));
//       }
//     };
    
//     // Start recording video frames
//     mediaRecorder.start(1000); // Adjust the interval between frames as needed
//   })
//   .catch(error => {
//     console.error("Get user media error", error);
//   })
// }

// window.addEventListener('load',startup, false);


videoContainer = document.querySelector(".video-container");
async function startCapture(displayMediaOptions) {
  let stream = null;

  try {
      stream = await navigator.mediaDevices.getUserMedia(displayMediaOptions);
      video = document.createElement("video");
      video.srcObject = stream;
      videoContainer.appendChild(video);
  } catch(err) {
      console.error(err);
  }
}
document.getElementById("shareBtn").addEventListener("click", () => {
  console.log("Call start Capture");
  startCapture({ video:true });
});
