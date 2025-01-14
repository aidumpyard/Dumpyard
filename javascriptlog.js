// Find the dropdown container div
var dropdown = document.querySelector('div.tabComboBoxNameContainer.tab-ctrl-formatted-fixedsize');

// Check if the dropdown is found
if (dropdown) {
    // Alert to show that the dropdown element is found
    alert("Dropdown found: " + dropdown.outerHTML);
    
    // Click the dropdown to open it
    dropdown.click();

    // Find the span element inside the dropdown
    var spanElement = document.querySelector('span.tabComboBoxName');

    // Check if the span element is found
    if (spanElement) {
        // Alert to show the current value in the span element
        alert("Current span value: " + spanElement.innerText.trim());

        // If the value is 'Singapore', change it to 'Indonesia'
        if (spanElement.innerText.trim() === 'Singapore') {
            spanElement.innerText = 'Indonesia';
            alert("Value changed to Indonesia");
        } else {
            alert("Value is not Singapore, no change made.");
        }

        // Trigger a change event
        var event = new Event('change', { bubbles: true });
        spanElement.dispatchEvent(event);
    } else {
        alert("Span element not found.");
    }
} else {
    alert("Dropdown element not found.");
}