function handleFileInputChange(event) {


  

  

  const selectedFile = event.target.files[0];
  const filename = selectedFile.name;

  if (selectedFile) {
      // Create a FileReader object to read the file
      const reader = new FileReader();

      // Set up a function to run when the file is loaded
      reader.onload = function(e) {
          // Set the source of the image to the loaded file data
          // document.querySelector("#primary_image").src = e.target.result;

          // Store the image data in local storage

          storeImageInLocalStorage(e.target.result, "org_image");
      };

      // Read the selected file as a data URL
      reader.readAsDataURL(selectedFile);
  }
  if (event.target.id === "first-time-input") {
    document.cookie = "myCookie=myValue; path=/; expires=Session; SameSite=None";
    document.querySelector(".main-div").style.display = "flex";
    document.querySelector(".headers").style.display = "flex";
    document.querySelector("#header-upload").style.display = "flex";
    document.querySelector(".first-time").style.display = "none";
    document.querySelector("#home").click();
    home();
    getData();
}else{
  home();
    getData();
}



}


function getCookie(name) {
  function escape(s) { return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1'); }
  var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
  return match ? match[1] : null;
}


// Function to store image data in local storage
function storeImageInLocalStorage(imageData, name) {
  try {
      // Check if local storage is supported
      if (typeof(Storage) !== "undefined") {
          // Store the image data with the specified name
          localStorage.setItem(name, imageData);
          return true; // Success
      } else {
          console.error("Local storage is not supported.");
          return false; // Local storage not supported
      }
  } catch (error) {
      console.error("Error storing image data:", error);
      return false; // Error occurred while storing
  }
}

// Function to retrieve image data from local storage by name
function retrieveImageFromLocalStorage(name) {
  try {
      // Check if local storage is supported
      if (typeof(Storage) !== "undefined") {
          // Retrieve the image data with the specified name
          const imageData = localStorage.getItem(name);
          
          return imageData;
          
      } else {
          console.error("Local storage is not supported.");
          return null; // Local storage not supported
      }
  } catch (error) {
      console.error("Error retrieving image data:", error);
      return null; // Error occurred while retrieving
  }
}


function checkCookie(cookieName) {
var cookies = document.cookie.split(';');
for (var i = 0; i < cookies.length; i++) {
var cookie = cookies[i].trim();

if (cookie.indexOf(cookieName + '=') === 0) {
return true; 
}
}
return false; 
}
if (checkCookie('first')) {
  document.querySelector(".main-div").style.display = "flex";
  document.querySelector(".headers").style.display = "flex";
  document.querySelector("#header-upload").style.display = "flex";
} else {
  
  document.querySelector(".main-div").style.display = "none";
  document.querySelector(".headers").style.display = "none";
  document.querySelector("#header-upload").style.display = "none";    
}  
const fileInputs = document.querySelectorAll('.input-upload-image');  
fileInputs.forEach(input => {
  input.addEventListener('change', handleFileInputChange);
});



function subtype_selected(e){
  
  const container = document.querySelectorAll(".image-selection-container div");
  container.forEach(data=>{
      const c = data.className;

      if(c == "active"){
        data.className="not";
      }

  });
  e.target.className = "active"

  getData(e);
  
}

function home(){
  document.querySelector("#home").className = "active";
  const data = ["Histogram Equalizer", "Edge Detection", "Pseudo Coloring"]
  const container = document.querySelector(".image-selection-container");
  container.innerHTML = "";




  var i=0;
  data.forEach(data=>{
    
    container.innerHTML += '<div onclick="subtype_selected(event)" data-sub-type="'+i+'">'+data+'</div>';
    i++;
  });
  document.querySelector(".image-selection-container div").className="active";

  document.querySelector(".param-input").style="display:none;"

}

function morph(){
  document.querySelector("#morph").className = "active";
  const data = ["Dilation", "Erosion", "Opening", "Closing"]
  const container = document.querySelector(".image-selection-container");
  container.innerHTML = "";
  var i=0;
  data.forEach(data=>{
    
    container.innerHTML += '<div onclick="subtype_selected(event)" data-sub-type="'+i+'">'+data+'</div>';

    i++;
  });
  document.querySelector(".image-selection-container div").className="active";

  document.querySelector(".param-input").style="display:flex;"
  document.querySelector(".param-input").setAttribute("placeholder", "Radius")
  document.querySelector(".wrap input").innerHTML = "";
  

}
function transform(){
  document.querySelector("#transform").className = "active";
  const data = ["Fourier Transform"]
  const container = document.querySelector(".image-selection-container");
  container.innerHTML = "";
  var i=0;
  data.forEach(data=>{

    container.innerHTML += '<div onclick="subtype_selected(event)" data-sub-type="'+i+'">'+data+'</div>';
    i++;
  });
  document.querySelector(".image-selection-container div").className="active";

  document.querySelector(".param-input").style="display:none;"

}
function segment(){



  document.querySelector("#analysis").className = "active";
  const data = ["Result", "Clear Skull", "Without Skull", "Opened Image"]
  const container = document.querySelector(".image-selection-container");
  container.innerHTML = "";
  var i=0;
  data.forEach(data=>{
    
    container.innerHTML += '<div onclick="subtype_selected(event)"data-sub-type="'+i+'">'+data+'</div>';
    i++;
  });
  document.querySelector(".image-selection-container div").className="active";
  document.querySelector(".param-input").setAttribute("placeholder", "Radius")

  if((document.querySelector('[data-sub-type="0"]').className == "active") && (document.querySelector("#param-2") == undefined)){
    alert("f");
    let html = '<div class="wrap"><input style="flex-grow:1;" type="text" id="param-2" class="param" value="5" data-param-type="" placeholder="Kernel Size (Median Filter)">';
    document.querySelector(".wrap input").insertAdjacentHTML("afterend", html);
  }else{
    alert("fo");
    document.querySelector("#param-2").style="display:none;";
  }
  
  document.querySelector(".param-input").style="display:flex;";
  
  

}
function selected(){

  const id = document.querySelector(".active").id;
  
  switch (id) {
    case "home":
      home();
      break;
    case "morph":
      morph();
      break;
    case "transform":
      transform();
      break;
    case "analysis":
      segment();
      break;
  }
  }





function pageChange(e){
  document.querySelector(".active").className="not_active";
  e.target.className = "active";
  selected();
  getData();
  
}

const headers = document.querySelectorAll(".headers section");
headers.forEach(input => {
  input.addEventListener('click', pageChange);
});


function getData(){

  const active = document.querySelectorAll(".active")
  let activeHeader;
  let activeSubtype;

  active.forEach(data=>{
    
    const parent = data.parentElement;
    
    

    if(parent.className == "headers"){

       activeHeader = data.id;

    }else if(parent.className == "image-selection-container"){
       

      activeSubtype = data.getAttribute("data-sub-type");
      


    }else{
      console.log("error")
    }
   

  
    
  });

  switch (activeHeader) {
    case "home":
      getDataHome(activeSubtype);
      break;
    case "morph":
      getDataMorph(activeSubtype);
      break;
    case "transform":
      getDataTrans(activeSubtype);
      break;
    case "analysis":
      getDataAnalysis(activeSubtype);
      break;
    
  }


  
  
}

function postData(subtype, param) {
  const data = {
    securityKey: "app_ender",
    body: {
      subtype: subtype,
      data: retrieveImageFromLocalStorage("org_image"),
      param: param,
    },
  };

  // Convert the JavaScript object to a JSON string
  const jsonString = JSON.stringify(data);

  return jsonString;
}

function getDataHome(type) {
  let subtype;
  let param;
  let text;
  if (type === "0") {
    subtype = "histo";
    text = "Histogram Equalizer"
    param = {};
  }
  if (type === "1") {
    subtype = "canny";
    text = "Edge Detection"
    param = { threshold1: 50, threshold2: 150 };
  }
  if (type === "2") {
    subtype = "pseudo";
    text = "Pseudo Color Mapping"
    param = { colorMap: 0 };
  }

  

  const data = postData(subtype, param);
  sendJSONPostRequest("home", data, function (error, res) {
    if (error) {
      console.error(error);
    } else {
      
      console.log(res);
      showResult(res, text);
    }
  });


}


function getDataMorph(type) {
  let subtype;
  let param;
  let text;
  if (type === "0") {
    subtype = "dilation";
    text = "Dilation"
    param = {radius: document.querySelector("#param").value};
  }
  if (type === "1") {
    subtype = "erosion";
    text = "Erosion"
    param = {radius: document.querySelector("#param").value};
  }
  if (type === "2") {
    subtype = "opening";
    text = "Opened Image"
    param = {radius: document.querySelector("#param").value};
  }
  if (type === "3") {
    subtype = "closing";
    text = "Closed Image"
    param = {radius: document.querySelector("#param").value};
  }

  

  const data = postData(subtype, param);
  sendJSONPostRequest("morph", data, function (error, res) {
    if (error) {
      console.error(error);
    } else {
      
      console.log(res);
      showResult(res, text);
    }
  });


}

function getDataTrans(type) {
  let subtype;
  let param;
  let text;
  if (type === "0") {
    subtype = "fourier";
    text = "Fourier Transform"
    param = {};
  }


  

  const data = postData(subtype, param);
  sendJSONPostRequest("transform", data, function (error, res) {
    if (error) {
      console.error(error);
    } else {
      
      console.log(res);
      showResult(res, text);
    }
  });


}



function getDataAnalysis(type) {
  let subsubtype;
  let subtype;
  let param;
  let text;
  let ksize = document.querySelector("#param-2").value;
  if (type === "0") {
    subtype = "lol";
    text = "Result"
    param = {subsubtype : "clea",radius: document.querySelector("#param").value, ksize: ksize};
  }
  if (type === "1") {
    let subtype = "clear";
    text = "Clear Skull Image"
    param = {subsubtype : "clear",radius: document.querySelector("#param").value, ksize: ksize};
  }
  if (type === "2") {
    let subtype = "output";
    text = "Without Skull Image"
    param = {subsubtype : "output",radius: document.querySelector("#param").value, ksize: ksize};
  }
  if (type === "3") {
    
    
    let subtype = "open";
    text = "Opened Image"
    param = {subsubtype : "open", radius: document.querySelector("#param").value, ksize:ksize};
  }

  

  const data = postData(subtype, param);
  sendJSONPostRequest("segment", data, function (error, res) {
    if (error) {
      console.error(error);
    } else {
      
      console.log(res);
      showResult(res, text);
    }
  });


}





function sendJSONPostRequest(url_, jsonData, callback) {
  
  const xhr = new XMLHttpRequest();
  const url = "http://127.0.0.1:8000/" + url_; // Corrected URL
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onload = function () {
    if (xhr.status === 200) {
      const jsonResponse = JSON.parse(xhr.responseText);
      callback(null, jsonResponse);
    } else {
      callback("Request failed with status: " + xhr.status, null);
    }
  };

  xhr.send(jsonData);
}


function showResult(res, text){
  const parsedData = JSON.parse(res);

  document.querySelector(".main-image-container img").src=parsedData.primary;
  document.querySelector(".detail-image img").src=parsedData.intensity_histogram;
  
  document.querySelector(".image-data-type").innerHTML = text;


}


function result(){
  document.querySelectorAll(".main-div img").forEach(data=>{
    data.src="../static/images/loading_mri.gif"
    document.querySelector(".image-data-type").innerHTML = "Processing";
    getData();
  });


}








