var redirectUrl = document.currentScript.getAttribute('data-redirect-url');
setTimeout(function () {
    window.location.href = redirectUrl;
}, 2500);
