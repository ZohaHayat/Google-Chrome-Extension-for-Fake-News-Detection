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