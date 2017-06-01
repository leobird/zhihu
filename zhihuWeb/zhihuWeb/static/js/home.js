$.fn.scrollTo = function( target, options, callback ){
  if(typeof options == 'function' && arguments.length == 2){ callback = options; options = target; }
  var settings = $.extend({
    scrollTarget  : target,
    offsetTop     : 50,
    duration      : 500,
    easing        : 'swing'
  }, options);
  return this.each(function(){
    var scrollPane = $(this);
    var scrollTarget = (typeof settings.scrollTarget == "number") ? settings.scrollTarget : $(settings.scrollTarget);
    var scrollY = (typeof scrollTarget == "number") ? scrollTarget : scrollTarget.offset().top + scrollPane.scrollTop() - parseInt(settings.offsetTop);
    scrollPane.animate({scrollTop : scrollY }, parseInt(settings.duration), settings.easing, function(){
      if (typeof callback == 'function') { callback.call(this); }
    });
  });
}

$(function(){
	var windowHeight = $(window).height()
	var checkScroll = function() {
		var offset = $(window).scrollTop()
		var selectedIndex = offset >= 470?0:1
		$('.top-nav-link > a').each(function(a){
			$(this).removeClass('active')
		}).eq(selectedIndex).addClass('active')

		if (offset > windowHeight/2) {
			$('.back-to-top').addClass('show')
		} else {
			$('.back-to-top').removeClass('show')
		}
	}
	$(window).on('scroll', function() {
		if (window.checkScrollTrigger) {
			clearTimeout(window.checkScrollTrigger)
		}
		window.checkScrollTrigger = setTimeout(checkScroll, 500)
	})

	$('.top-nav-link > a').on('click', function(){
		var targetOffset = $(this).data('offset')
		$('body').scrollTo(targetOffset, {duration: 600})
	})

	$('.back-to-top').on('click', function(){
		$('body').scrollTo(0, {duration: 600})
	})

	$('.read-more').on('click', function(){
		$('body').scrollTo(0, {duration: 600})
	})

	// $('.sample').one('load', function(){
	// 	$(this).addClass('loaded')
	// 	$('.download .inner').addClass('loaded')
	// }).each(function(){
	// 	if (this.complete) {
	// 		$(this).trigger('load')
	// 	}
	// })
	
	setTimeout(function(){
		$('.sample').addClass('loaded')
		$('.download .inner').addClass('loaded')
	}, 300)


	// $(".preview-image").lazyload();
/*
	$('.preview-image').each(function(index, img){
		$(this).one('load', function(){
			$(this).addClass('loaded')
			var linkButton = $(this).closest('a')
			var mask = linkButton.find('.mask')
			mask.height($(this).height())
		})
	}).each(function(){
		if (this.complete) {
			$(this).trigger('load')
		}
	})
*/


	
})
