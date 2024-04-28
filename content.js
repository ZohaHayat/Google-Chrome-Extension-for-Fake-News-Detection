// Function to format and display the processed text in a popup window
// Function to format and display the processed text in a popup window
function showPopupMessage(processedTex, rating, popupWindow) {
    // Create HTML content for the popup window
    var popupContent = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Processed Text</title></head><body style="background-color: #FFF; color:  #8e3768; padding: 20px; font-family: \'Roboto\', sans-serif;">';

    popupContent += '<div style="margin-bottom: 20px;">';
    popupContent += '<div style="display: flex; flex-direction: row; width: 100%; height: 20px; background: #e0e0e0; border-radius: 5px;">';

    // Create 5 sections, coloring the one representing the rating
    for (var i = 0; i < 5; i++) {
        var sectionColor = i < rating ? '#f00' : '#ddd'; // Highlight with red if less than rating, otherwise light gray
        popupContent += '<div style="flex: 1; background: ' + sectionColor + '; border-right: 1px solid white;"></div>';
    }

    popupContent += '</div>'; // Close fuel bar
    popupContent += '</div>'; // Close containing div

    // Add the processed text
    popupContent += '<h3>Rating: ' + rating + '</h3>'; // Display the rating value

    // Split the processed text into paragraphs
    var paragraphs = processedTex.split('\n\n');

    // Add each paragraph as a <p> element
    paragraphs.forEach(function(paragraph) {
        popupContent += '<p>' + paragraph + '</p>';
    });

    // Close HTML body and document
    popupContent += '</body></html>';

    // // Calculate the position of the popup window to center it on the screen
    // var popupWidth = 600; // Width of the popup window
    // var popupHeight = 400; // Height of the popup window
    // var screenWidth = window.screen.availWidth;
    // var screenHeight = window.screen.availHeight;
    // var popupLeft = (screenWidth - popupWidth) / 2;
    // var popupTop = (screenHeight - popupHeight) / 2;

    // // Open a new popup window with the formatted content
    // var popupWindow = window.open('', 'popupWindow', 'width=' + popupWidth + ', height=' + popupHeight + ', left=' + popupLeft + ', top=' + popupTop);

    // // Write the HTML content to the popup window's document
    popupWindow.document.write(popupContent);

    // // Close the document stream to ensure the document is fully loaded and parsed
    // popupWindow.document.close();
}

function showLoadingPopup() {
    // Create the loading popup content with a spinner
    var popupContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Processing...</title>
            <style>
                /* Basic style for the spinner */
                .spinner {
                    border: 4px solid #f3f3f3; /* Light grey */
                    border-top: 4px solid #3498db; /* Blue */
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    animation: spin 1s linear infinite; /* Infinite rotation */
                }

                /* Animation for the spinner */
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body style="background-color: #FFF; color: #8e3768; padding: 20px; font-family: 'Roboto', sans-serif;">
            <div class="spinner" style="margin-bottom: 20px;"></div> <!-- Loading spinner -->
            <div id="content">Processing...</div> <!-- Placeholder content -->
        </body>
        </html>
    `;

    var popupWidth = 600; // Width of the popup window
    var popupHeight = 400; // Height of the popup window
    var screenWidth = window.screen.availWidth;
    var screenHeight = window.screen.availHeight;
    var popupLeft = (screenWidth - popupWidth) / 2;
    var popupTop = (screenHeight - popupHeight) / 2;

    // Open a new popup window with the initial content
    var popupWindow = window.open('', 'popupWindow', 'width=' + popupWidth + ', height=' + popupHeight + ', left=' + popupLeft + ', top=' + popupTop);

    // Write the initial content
    popupWindow.document.write(popupContent);

    // Close the document stream
    popupWindow.document.close();

    return popupWindow; // Return the popup reference
}

// Function to handle text selection and alert message
function handleTextSelection(e) {
    let selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 0) {
        let checkForFakeNews = confirm("Would you like to check if this is fake news?");
        if (checkForFakeNews) {
            let popupWindow  = showLoadingPopup()
            chrome.runtime.sendMessage({ text: selectedText }, function(response) {
                var processed = response.processedText;

                var pt = processed.split('.')
                var rating = parseInt(pt.slice(-2).join(""), 10)
                var mainText = pt.slice(0, -2).join(".") + "\""
        
                // showPopupMessage("Processed Text: " + mainText, rating);
                showPopupMessage(mainText, rating, popupWindow);
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




