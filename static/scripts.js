function loadTabContent(tabName, url_suffix) {
	$.get('/' + tabName, function(data) {
		$('#tab-content-container').html(data);
	})
	.fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Failed to load content for tab ' + tabName + ':', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to load content. Please try again. If the issue persiststs, try resetting cache data for this website.');
	});
}

$(document).ready(function() {
	// Initial load
	if (typeof current_tab !== 'undefined') {
		loadTabContent(current_tab);
	} else {
		loadTabContent('syllabus');
	}

	// Handle tab clicks
	$('a[data-tabname]').on('click', function(e) {
		e.preventDefault();
		var tabName = $(this).data('tabname');
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
		loadTabContent(tabName);
	});

});