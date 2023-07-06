var WebApp = window.Telegram.WebApp;

function handleClick(element) {{
    event.preventDefault();
    var stopID = element.innerText;
    console.log('Stop ID clicked: ' + stopID);
    WebApp.sendData(stopID)
    WebApp.close();
}}
