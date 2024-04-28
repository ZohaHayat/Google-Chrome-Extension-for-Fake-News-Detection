chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  fetch('http://127.0.0.1:5000/process_text', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: request.text })
  })
  .then(response => response.text())
  .then(result => {
      sendResponse({ processedText: result });
  })
  .catch(error => console.log('Error:', error));
  return true; // To indicate asynchronous response
});