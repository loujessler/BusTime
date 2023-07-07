var WebApp = window.Telegram.WebApp;

WebApp.expand()
function handleClick(element) {
    event.preventDefault();
    var spanElement = element.querySelector('span'); // get the span element
    if(spanElement) { // check if the span element exists
        var stopID = spanElement.innerText; // get the text from the span
        console.log('Stop ID clicked: ' + stopID);
        WebApp.sendData(stopID)
        WebApp.close();
    } else {
        console.log('Span element not found');
    }
}
