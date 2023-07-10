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
    uploadedArea.innerHTML = ""; //uncomment this line if you don't want to show upload history
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = progressHTML;
    if (loaded == total) {
      progressArea.innerHTML = "";
      let uploadedHTML = `<li class="row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="details">
                                <span class="name">${name} • Ready to Download</span>
                                <span class="size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-download download-icon"></i>
                          </li>`;
      uploadedArea.classList.remove("onprogress");
      uploadedArea.innerHTML = uploadedHTML; //uncomment this line if you don't want to show upload history
      // uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
    
      // Add a click event listener to the download icon
      const downloadIcon = uploadedArea.querySelector(".download-icon");
      downloadIcon.addEventListener("click", downloadFile);
    }
  });
  let data = new FormData(form); //FormData is an object to easily send form data
  xhr.responseType = 'blob';
  xhr.onreadystatechange = function() {
    console.log('Received file');
    if (xhr.readyState === XMLHttpRequest.DONE){
        if (xhr.status == 200) {
            var blob = this.response;
        
            // Create a temporary link and trigger the file download
            var downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(blob);
            downloadLink.download = 'video.mp4'; // Set the desired filename
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            const videoElement = document.createElement('video');
            const sourceElement = document.createElement('source');
            sourceElement.src = window.URL.createObjectURL(blob);
            sourceElement.type = 'video/mp4';

            videoElement.appendChild(sourceElement);
            videoElement.autoplay = true;
            videoElement.controls = true;
            videoElement.preload = 'auto';
            videoElement.width = 320;
            videoElement.height = 180;

            document.body.children[1].appendChild(videoElement);
            videoElement.load();
        }
    }
  };

  xhr.send(data); //sending form data as the body to the request

  // fetchVideoFile();
}

function downloadFile() {
  const downloadURL = "/api/uploadResponse"; // Replace with the correct URL for your Django endpoint
  window.open(downloadURL, "_blank");
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



