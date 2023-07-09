const form = document.querySelector("form"),
video = document.querySelector("video");

// form.addEventListener("click", () =>{
//   startup();
// });

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
  }).catch(console.error)
}

window.addEventListener('load',startup, false);


