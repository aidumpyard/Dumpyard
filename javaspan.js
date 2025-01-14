// Find the span element inside the dropdown
var spanElement = document.querySelector('span.tabComboBoxName');

// Check if the span element is found
if (spanElement) {
    // Display the current span value in the browser tab title
    document.title = "Current Value: " + spanElement.innerText.trim();

    // Change the span value to Indonesia if it's Singapore
    if (spanElement.innerText.trim() === 'Singapore') {
        spanElement.innerText = 'Indonesia';
        document.title = "Value Changed to: Indonesia";
    }
} else {
    document.title = "Span element not found.";
}