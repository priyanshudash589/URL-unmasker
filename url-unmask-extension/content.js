// document.addEventListener("DOMContentLoaded", function() {
//   var sendUrlButton = document.getElementById("send-url");
//   sendUrlButton.addEventListener("click", function() {
//     chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
//       var currentUrl = tabs[0].url;
//       console.log(currentUrl)

//       var xhr = new XMLHttpRequest();
// xhr.open('POST', 'http://127.0.0.1:8000/extreq/', true);
// xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
// xhr.onload = function () {
//     // do something to response
//     console.log(this.responseText);
// };
// data = {url:currentUrl}
// xhr.send('url='+currentUrl);

     
//     });
//   });
// });


document.addEventListener("DOMContentLoaded", function() {
  var sendUrlButton = document.getElementById("send-url");
  sendUrlButton.addEventListener("click", function() {
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
      var currentUrl = tabs[0].url;
      console.log(currentUrl)

      var xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://127.0.0.1:8000/extreq/', true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      xhr.onload = function () {
        // create a Blob object with the response data
        var blob = new Blob([this.responseText], { type: 'text/html' });
        // create a URL for the Blob object
        var url = URL.createObjectURL(blob);
        // open the URL in a new tab
        chrome.tabs.create({url: url});
      };
      xhr.send('url=' + currentUrl);
    });
  });
});
