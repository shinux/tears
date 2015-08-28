
function backToTop() {
    $('html, body').animate({scrollTop:0}, 'slow');
}


$(window).on('scroll', function() {
	if (document.body.scrollTop > 200) {
		$('.glyphicon-triangle-top').show();
	} else {
		$('.glyphicon-triangle-top').hide();
	}
});


function showSearchField() {
	if ($('.search').css("display") == 'none') {
		$('.search').show()
	} else {
		$('.search').hide()
	}
}

$(function() {
	$('.search').bind('keypress', function(event) {
		if(event.keyCode == "13") {
			window.open('https://www.google.com.hk/search?q=site:sinux.me%20' + $('.search').val() + '&gws_rd=cr,ssl');
		}
	});
});
