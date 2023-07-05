var WebApp = window.Telegram.WebApp;


document.getElementById('mystop').addEventListener('click', function (event) {{
    event.preventDefault();
    var stopID = event.target.innerText;
    WebApp.sendData(stopID)
    console.log('Stop ID clicked: ' + {stop[2]});
}});