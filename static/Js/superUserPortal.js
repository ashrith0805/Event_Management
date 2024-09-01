document.addEventListener('DOMContentLoaded', function() {
    var viewEvents = document.getElementById("View");
    viewEvents.addEventListener('click', function() {
        window.location.href = 'viewEvents';
    });

    var createEvent = document.getElementById("Create");
    createEvent.addEventListener('click', function() {
        window.location.href = 'createEvent';
    });

     var deleteEvent = document.getElementById("Delete");
    deleteEvent.addEventListener('click', function() {
        window.location.href = 'DeleteEvent';
    });

    var editEvent=document.getElementById("Editcap");
     editEvent.addEventListener('click', function() {
        window.location.href = 'editEvent';
    });

    var logView=document.getElementById("logbutton");
    logView.addEventListener('click', function() {
        window.location.href = 'transactionLog';
    });

   var logOut=document.getElementById("logout");
    logOut.addEventListener('click', function() {
        window.location.href = 'logout';
    });
});
