// Find the container div with the class name
var dropdown = document.querySelector('div.tabComboBoxNameContainer.tab-ctrl-formatted-fixedsize');

// Check if the dropdown is found
if (dropdown) {
    // Click the dropdown to open it
    dropdown.click();

    // Find the span element inside the dropdown with the value 'Singapore'
    var spanElement = document.querySelector('span.tabComboBoxName');

    // Change the inner text to 'Indonesia'
    if (spanElement && spanElement.innerText.trim() === 'Singapore') {
        spanElement.innerText = 'Indonesia';

        // Trigger a change event to notify the page of the update
        var event = new Event('change', { bubbles: true });
        spanElement.dispatchEvent(event);
    }
}