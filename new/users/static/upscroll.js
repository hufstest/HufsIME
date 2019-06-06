var amountScrolled = 220;
    	var duration = 500;
$(window).scroll(function() {
	if ( $(window).scrollTop() > amountScrolled ) {
		$('a.back-to-top').fadeIn(duration);
	} else {
		$('a.back-to-top').fadeOut(duration);
	}
});

 $('a.back-to-top').click(function() {
	$('body, html').animate({
		scrollTop: 0
	}, 700);
	return false;
});