<<<<<<< HEAD
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
=======
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action == "processText") {
      fetch('http://127.0.0.1:5000/process_text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any required headers for your LLM API
        },
        body: JSON.stringify({ prompt: request.text }),
      })
      .then(response => response.json())
      .then(data => sendResponse({result: data}))
      .catch(error => console.error('Error:', error));
      return true; // Indicates you wish to send a response asynchronously.
    }
  });
>>>>>>> 9500ee75a4eb3dbcfa536eafa580140a4619ea98
