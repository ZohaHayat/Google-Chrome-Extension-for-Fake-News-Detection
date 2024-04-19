document.addEventListener('mouseup', function(e) {
    let selectedText = window.getSelection().toString().trim();
    if (selectedText.length > 0) {
        let checkForFakeNews = confirm("Would you like to check if this is fake news?");
        if (checkForFakeNews) {
            alert("Checking for fake news...");
        }
    }
});
