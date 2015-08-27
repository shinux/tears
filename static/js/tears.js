
function backToTop(){
    $('html, body').animate({scrollTop:0}, 'slow');
}


$(window).on('scroll', function() {
	if (document.body.scrollTop > 200) {
		$('.glyphicon-triangle-top').show();
	} else {
		$('.glyphicon-triangle-top').hide();
	}
})