$(document).ready(function() {
    function setBodyHeight() {
        $('body').height(window.innerHeight);
    }
    setBodyHeight();
    $(window).resize(setBodyHeight);
});
