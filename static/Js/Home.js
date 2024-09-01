document.addEventListener('DOMContentLoaded', function() {
    var loginButton = document.getElementById("login");
    loginButton.addEventListener('click', function() {
        window.location.href = 'login';
    });

    var registerButton = document.getElementById("register");
    registerButton.addEventListener('click', function() {
        window.location.href = 'register';
    });

    var cancelledEvents = document.getElementById("cancelledEvents");
     cancelledEvents.addEventListener('click', function() {
        window.location.href = 'cancelledEvents';
    });




});

