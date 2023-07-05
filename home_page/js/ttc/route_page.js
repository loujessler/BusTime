var WebApp = window.Telegram.WebApp;
var MainButton = WebApp.MainButton;

MainButton.show();

MainButton.setText("Close")

MainButton.onClick(function() {
  WebApp.close();
});
WebApp.onEvent('mainButtonClicked', function() {
  /* also */
});
