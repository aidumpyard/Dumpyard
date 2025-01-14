var dropdown = document.querySelector('div.tabs.tab-ctrl');
if (dropdown) {
    var options = dropdown.querySelectorAll('li');
    options.forEach(function(option) {
        if (option.innerText === 'Indonesia') {
            option.click();
        }
    });
}