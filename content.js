// Function to format and display the processed text in a popup window
// Function to format and display the processed text in a popup window
function showPopupMessage(processedText) {
    // Create HTML content for the popup window
    var popupContent = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Processed Text</title></head><body style="background-color: #FFF; color:  #8e3768; padding: 20px; font-family: \'Roboto\', sans-serif;">';

    // Split the processed text into paragraphs
    var paragraphs = processedText.split('\n\n');

    // Add each paragraph as a <p> element
    paragraphs.forEach(function(paragraph) {
        popupContent += '<p>' + paragraph + '</p>';
    });

    // Close HTML body and document
    popupContent += '</body></html>';

    // Calculate the position of the popup window to center it on the screen
    var popupWidth = 600; // Width of the popup window
    var popupHeight = 400; // Height of the popup window
    var screenWidth = window.screen.availWidth;
    var screenHeight = window.screen.availHeight;
    var popupLeft = (screenWidth - popupWidth) / 2;
    var popupTop = (screenHeight - popupHeight) / 2;

    // Open a new popup window with the formatted content
    var popupWindow = window.open('', 'popupWindow', 'width=' + popupWidth + ', height=' + popupHeight + ', left=' + popupLeft + ', top=' + popupTop);

    // Write the HTML content to the popup window's document
    popupWindow.document.write(popupContent);

    // Close the document stream to ensure the document is fully loaded and parsed
    popupWindow.document.close();
}

// Function to handle text selection and alert message
function handleTextSelection(e) {
    let selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 0) {
        let checkForFakeNews = confirm("Would you like to check if this is fake news?");
        if (checkForFakeNews) {
            chrome.runtime.sendMessage({ text: selectedText }, function(response) {
                var processedText = response.processedText;

                showPopupMessage("Processed Text: " + processedText);
            });
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




