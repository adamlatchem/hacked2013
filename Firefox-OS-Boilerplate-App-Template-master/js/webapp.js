i(function () {
  
    function handleOrientation(event) {
  var x = event.beta;  // In degree  [-180,180]
  var y = event.gamma; // In degree  [-90,90]
  var z = event.aplha; // whateveeerrr z axis
  
   x = (x+90)/180;
  y = (y+90)/180;
      
      if(y < 0){
      y = 0;}
      
      if (y>1){
      y = 1;}

document.getElementById('xaxis').innerHTML = x;
    
document.getElementById('yaxis').innerHTML = y;
      
      
function getXMLHttpRequestObject()
{
  var xmlhttp;
   if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
    try {
      xmlhttp = new XMLHttpRequest();
    } catch (e) {
      xmlhttp = false;
    }
  }
  return xmlhttp;
}
      
var http = new getXMLHttpRequestObject();
  
var url = "http://192.168.2.158/index.html";
var parameters = "x="+x+"&y="+y;
http.open("GET", url+"?"+parameters, true);
     
    
   
http.send(null);

    }

 window.addEventListener('deviceorientation', handleOrientation);



})(); 
