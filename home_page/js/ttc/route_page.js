var WebApp = window.Telegram.WebApp;

WebApp.expand()
function handleClick(element) {{
    event.preventDefault();
    var stopID = element.innerText;
    console.log('Stop ID clicked: ' + stopID);
    WebApp.sendData(stopID)
    WebApp.close();
}}
