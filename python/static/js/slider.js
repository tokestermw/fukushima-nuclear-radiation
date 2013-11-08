// Code adapted from Marc Neuwirth
// http://marcneuwirth.com/blog/2010/02/21/using-a-jquery-ui-slider-to-select-a-time-range/


$(function() {
    $( "#dateslider" ).slider({
	orientation: "horizontal",
	range: "min",
	min: 0,
	max: 100,
	value: 60,
	slide: function( event, ui ) {
            $( "#amount" ).val( ui.value );
	}
    });
    $( "#amount" ).val( $( "#dateslider" ).slider( "value" ) );
});

// add a date
$(function() {
    $( "#datepicker" ).datepicker({ 
	defaultDate: new Date(2011, 9-1, 24),
	minDate: new Date(2011, 2-1, 28), 
	maxDate: new Date(2011, 11-1, 18),
	onSelect: function(dateText) {
	    demoinit();
	}
    });
});
