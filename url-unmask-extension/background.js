// Add an event listener for when a short URL is copied to the clipboard
document.addEventListener('copy', function(event) {
  // Get the text that was copied to the clipboard
  var clipboardData = event.clipboardData || window.clipboardData;
  var copiedText = clipboardData.getData('text');

  // Check if the copied text is a short URL
  if (copiedText.startsWith('http://bit.ly/') || copiedText.startsWith('https://goo.gl/')) {
    // Send a message to the extension to open
    chrome.runtime.sendMessage('hjcdjaabkieehhnmmabnmnomhglhlpjm', function(response) {
      console.log(response);
    });
  }
});