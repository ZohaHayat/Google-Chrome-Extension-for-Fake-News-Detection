// Function to handle text selection and alert message
function handleTextSelection(e) {
    let selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 0) {
        let checkForFakeNews = confirm("Would you like to check if this is fake news?");
        if (checkForFakeNews) {
            alert("Checking for fake news...");
        }
    }
}

// Function to add or remove the event listener based on extension state
function updateEventListener(extensionState) {
    if (extensionState) {
        document.addEventListener('mouseup', handleTextSelection);
    } else {
        document.removeEventListener('mouseup', handleTextSelection);
    }
}

// Retrieve extension state from storage and add or remove the event listener accordingly
chrome.storage.sync.get('extensionState', function(data) {
    var extensionState = data.extensionState || false; // Default state is false if not set
    updateEventListener(extensionState);
});

// Listen for changes in the extension state and update the event listener accordingly
chrome.storage.onChanged.addListener(function(changes, namespace) {
    if (changes.extensionState) {
        var newExtensionState = changes.extensionState.newValue;
        updateEventListener(newExtensionState);
    }
});




