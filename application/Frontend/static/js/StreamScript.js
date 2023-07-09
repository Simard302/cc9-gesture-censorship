// // Get access to the camera stream
// navigator.mediaDevices.getUserMedia({ video: true })
//   .then(function(stream) {
//     var videoElement = document.getElementById('video');
//     videoElement.srcObject = stream;
    
//     // Create a WebSocket connection to the server
//     var socket = new WebSocket('ws://localhost:8000/stream/');
    
//     // Send each video frame and camera information to the server
//     var mediaRecorder = new MediaRecorder(stream);
//     mediaRecorder.ondataavailable = function(event) {
//       if (socket.readyState === WebSocket.OPEN) {
//         var cameraInfo = {
//           resolution: {
//             width: videoElement.videoWidth,
//             height: videoElement.videoHeight
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
//   .catch(function(error) {
//     console.error('Error accessing camera:', error);
//   });
