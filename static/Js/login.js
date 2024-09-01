document.addEventListener('DOMContentLoaded', function() {
    var resetpass = document.getElementById("forgotpass");
    resetpass.addEventListener('click', function() {
        window.location.href = 'emailPassReset';
    });
});