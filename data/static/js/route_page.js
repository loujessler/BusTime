var WebApp = window.Telegram.WebApp;
var MainButton = WebApp.MainButton;
var BackButton = WebApp.BackButton;

MainButton.text("Back")
MainButton.show();
BackButton.show();

MainButton.onClick(function() {
  WebApp.close();
});
WebApp.onEvent('mainButtonClicked', function() {
  /* also */
});

BackButton.onClick(function() {
  WebApp.close();
});
WebApp.onEvent('backButtonClicked', function() {
  /* also */
});