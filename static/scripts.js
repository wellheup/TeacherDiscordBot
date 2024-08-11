// static/scripts.js

function getUrlSuffix() {
	return new URL(window.location.href).searchParams.get('url_suffix') || '';
}

function loadTabContent(tabName) {
	const url_suffix = getUrlSuffix();
	const url = `/${tabName}?url_suffix=${url_suffix}`;

	$.get(url, function(data) {
		$('#tab-content-container').html(data);
		toggleColumnVisibility();
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Failed to load content: ', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to load content. Please try again.');
	});
}

function loadInitialTab() {
	const tabName = window.location.hash.substr(1) || 'syllabus';
	$('.nav-link').removeClass('active');
	$(`.nav-link[data-tabname="${tabName}"]`).addClass('active');
	loadTabContent(tabName);
}

function toggleColumnVisibility() {
	const checkboxes = document.querySelectorAll('.column-toggle');
	checkboxes.forEach(checkbox => {
		const columnClass = 'col-' + checkbox.dataset.column;
		const elements = document.querySelectorAll('.' + columnClass);
		elements.forEach(el => {
			el.style.display = checkbox.checked ? '' : 'none';
		});
	});
}

function handleFormSubmit(e) {
	e.preventDefault();
	const form = $(this);
	const url_suffix = getUrlSuffix();
	const tabName = $('.nav-link.active').data('tabname');
}

$(document).ready(function() {
	loadInitialTab();

	$('a[data-tabname]').on('click', function(e) {
		e.preventDefault();
		const tabName = $(this).data('tabname');
		const url_suffix = getUrlSuffix();
		window.location.hash = tabName;
		loadTabContent(tabName);
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
	});

	$(window).on('hashchange', function() {
		loadInitialTab();
	});

	toggleColumnVisibility();

	$(document).on('change', '.column-toggle', function() {
		toggleColumnVisibility();
	});

	// Handle form submissions via AJAX
	$(document).off('submit').on('submit', 'form', handleFormSubmit);

	// Show modal for new bug
	$('#newBugButton').on('click', function() {
		$('#newBugForm').modal('show');
	});
});