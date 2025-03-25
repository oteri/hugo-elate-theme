// Enable keyboard navigation for the blogs carousel
$(document).ready(function() {
    var $carousel = $('#blogs-carousel');
    
    $(document).on('keydown', function(e) {
        if (!$carousel.is(':visible')) return;
        
        // Left arrow key
        if (e.keyCode === 37) {
            $carousel.carousel('prev');
        }
        // Right arrow key
        else if (e.keyCode === 39) {
            $carousel.carousel('next');
        }
    });

    // Prevent automatic cycling
    $carousel.carousel({
        interval: false
    });
});
