// document.addEventListener("DOMContentLoaded", function() {
//     var extensionToggle = document.getElementById('extension-toggle');

//     // Retrieve extension state from storage and update the toggle switch accordingly
//     chrome.storage.sync.get('extensionState', function(data) {
//         var extensionState = data.extensionState || false; // Default state is false if not set
//         console.log('Retrieved extension state:', extensionState);
//         // updateToggleState(extensionState);
//     });

//     // Toggle switch state when clicked
//     extensionToggle.addEventListener('change', function() {
//         var extensionState = this.checked; // Get the current state of the toggle switch
//         console.log('Toggling extension state to:', extensionState);
        
//         // Update toggle switch state
//         // updateToggleState(extensionState);
        
//         // Store the updated state
//         chrome.storage.sync.set({ extensionState: extensionState }, function() {
//             console.log('Extension state updated successfully.');
//         });
//     });   

//     // Function to update toggle switch label based on extension state
//     // function updateToggleState(extensionState) {
//     //     if (extensionState) {
//     //         // Toggle switch is ON
//     //         extensionToggle.labels[0].innerText = 'Extension is ON';
//     //     } else {
//     //         // Toggle switch is OFF
//     //         extensionToggle.labels[0].innerText = 'Turn On Extension';
//     //     }
//     // }
// });
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // Check if the message contains processed text
    if (message.processedText) {
        // Update the content of the processedText element with the processed text answer
        document.getElementById('processedText').textContent = "Processed Text: " + message.processedText;
    }
});



document.addEventListener("DOMContentLoaded", function () {
    var extensionToggle = document.getElementById('extension-toggle');

    // Retrieve extension state from chrome.storage.sync
    chrome.storage.sync.get('extensionState', function (data) {
        var extensionState = data.extensionState || false; // Default to false if not set
        extensionToggle.checked = extensionState; // Set toggle to the stored state
        // updateToggleLabel(extensionState); // Update label based on state
    });

    // Event listener for toggle switch change
    extensionToggle.addEventListener('change', function () {
        var extensionState = this.checked; // Get current state of toggle switch
        console.log('Toggling extension state to:', extensionState);

        // Store the updated state
        chrome.storage.sync.set({ extensionState: extensionState }, function () {
            console.log('Extension state updated successfully.');
        });

        // updateToggleLabel(extensionState); // Update label based on state
    });

    // // Function to update toggle switch label based on extension state
    // function updateToggleLabel(extensionState) {
    //     var toggleLabel = extensionToggle.parentNode.querySelector('.slider');
    //     if (extensionState) {
    //         toggleLabel.innerText = 'Extension is ON';
    //     } else {
    //         toggleLabel.innerText = 'Turn On Extension';
    //     }
    // }
});
