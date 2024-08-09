function loadTabContent(tabName, newTabName) {
	let params = new URLSearchParams(window.location.search);
	let url_suffix = params.get('url_suffix') || '';
	let current_tab = newTabName || params.get('current_tab') || 'syllabus';
	let url = `/${tabName}?url_suffix=${url_suffix}&current_tab=${current_tab}`;

	$.get(url, function(data) {
		$('#tab-content-container').html(data);
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Failed to load content for tab ' + tabName + ':', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to load content. Please try again.');
	});
}

$(document).ready(function() {
	// Initial load
	loadTabContent('syllabus');

	$('a[data-tabname]').on('click', function(e) {
		e.preventDefault();
		var tabName = $(this).data('tabname');
		console.log('Tab clicked:', tabName);
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
		loadTabContent(tabName, tabName);
	});
});