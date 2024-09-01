document.addEventListener('DOMContentLoaded', function() {
    var viewEvents = document.getElementById("View");
    viewEvents.addEventListener('click', function() {
        window.location.href = 'viewEvents2';
    });

    var BookEvent = document.getElementById("Book");
    BookEvent.addEventListener('click', function() {
        window.location.href = 'bookEvent';
    });

     var cancelBooking = document.getElementById("Cancel");
    cancelBooking.addEventListener('click', function() {
        window.location.href = 'cancelBooking';
    });

    var viewBooking=document.getElementById("ViewBooking");
     viewBooking.addEventListener('click', function() {
        window.location.href = 'viewBooking';
    });


});
