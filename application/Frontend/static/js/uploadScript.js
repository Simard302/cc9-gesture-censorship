const form = document.querySelector("form"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");


form.addEventListener("click", () =>{
  fileInput.click();
});

fileInput.onchange = ({target})=>{
  let file = target.files[0];
  if(file){
    let fileName = file.name;
    if(fileName.length >= 12){
      let splitName = fileName.split('.');
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    if (file.size >= 1073741824) {
      console.log("File is too large");
      doNotUploadFile(fileName, file.size);
    }else{
      uploadFile(fileName);
    }
  }
}

function uploadFile(name){
  console.log("Running Upload");

  let xhr = new XMLHttpRequest();
  console.log("Created Request");

  xhr.open("POST", "api/upload"); // opens request
  console.log("POSTED");

  xhr.upload.addEventListener("progress", ({loaded, total}) =>{

    let fileLoaded = Math.floor((loaded / total) * 100);
    let fileTotal = Math.floor(total / 1000);
    let fileSize;

    (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";
    let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${name} • Uploading</span>
                              <span class="percent">${fileLoaded}%</span>
                            </div>
                            <div class="progress-bar">
                              <div class="progress" style="width: ${fileLoaded}%"></div>
                            </div>
                          </div>
                        </li>`;
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = progressHTML;
    if(loaded == total){
      progressArea.innerHTML = "";
      let uploadedHTML = `<li class="row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="details">
                                <span class="name">${name} • Uploaded</span>
                                <span class="size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;
      uploadedArea.classList.remove("onprogress");
      uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
    }
  });
  let data = new FormData(form); //FormData is an object to easily send form data
  xhr.send(data); //sending form data as the body to the request

  fetchVideoFile();
}

function doNotUploadFile (name, fileSize){
  progressArea.innerHTML = "";
  uploadedArea.classList.add("onprogress");

  fileSize = (fileSize / (1024*1024*1024)).toFixed(2) + " GB";
  let uploadedHTML = `<li class="row">
                        <div class="content upload">
                          <i class="fas fa-file-alt"></i>
                          <div class="details">
                            <span class="name">${name} • Not Uploaded<br>File too large. Max 1 GB.</span>
                            <span class="size">${fileSize}</span>
                          </div>
                        </div>
                        <i class="fas fa-times"></i>
                      </li>`
  uploadedArea.classList.remove("onprogress");
  uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
  console.log("Created File too large prompt")
}

// function fetchVideoFile() {
//   const videoPlayer = document.getElementById("video-player");
//   videoPlayer.src = "api/uploadResponse";
//   videoPlayer.play();
// }



const videoPlayer = document.getElementById("video-player");
const playButton = document.getElementById("play-button");
// var playPromise = document.querySelector("video").play();

playButton.addEventListener("click", function() {
  playVideo();
});

// function fetchVideoFile() {
//   console.log("Attempting to fetch");
//   fetch("api/uploadResponse")
//     .then(response => {
//       console.log(`Response type ${response.type}`);
//       return response.blob();
//     })
//     .then(blob => {
//       console.log(blob);
//       // videoPlayer.src = URL.createObjectURL(blob);
//       const urlCreator = window.URL || window.webkitURL;
//       videoPlayer.src = urlCreator.createObjectURL(blob);
//       console.log(videoPlayer.src);
//       videoPlayer.load();

//       console.log("Loaded Video");
//       playButton.style.display = "block";
//     })
//     .catch(error => {
//       console.error("Error fetching video file:", error);
//     });
// }


function fetchVideoFile() {
  console.log("Attempting to fetch");
  fetch("api/uploadResponse")
    .then(response => {
      console.log(`Response type ${response.type}`);
      return response.arrayBuffer();
    })
    .then(arrayBuffer => {
      const blob = new Blob([arrayBuffer], { type: "video/mp4" });
      const videoURL = URL.createObjectURL(blob);
      videoPlayer.src = videoURL;
      console.log(videoPlayer.src);
      videoPlayer.load();

      console.log("Loaded Video");
      playButton.style.display = "block";
    })
    .catch(error => {
      console.error("Error fetching video file:", error);
    });
}


function playVideo() {
  videoPlayer.play().then(function() {
    // Playback started
    playButton.style.display = "none";
  }).catch(function(error) {
    // Handle playback error
    console.error("Error playing video:", error);
  });
}

window.addEventListener("load", () => {playButton.style.display = "none";});
