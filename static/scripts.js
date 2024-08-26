let isSubmitting = false;

function getUrlSuffix() {
	return new URL(window.location.href).searchParams.get('url_suffix') || '';
}

function loadTabContent(tabName) {
	const url_suffix = getUrlSuffix();
	const url = `/${tabName}?url_suffix=${url_suffix}`;
	console.log(`Loading content for tab: ${tabName} with URL: ${url}`);
	$.get(url, function(data) {
		$('#tab-content-container').html(data);
		console.log('Content loaded. Attaching form submit handler.');
		attachFormSubmitHandler(); // Re-attach form submit handler after loading new content
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Failed to load content: ', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to load content. Please try again.');
	});
}

function loadInitialTab() {
	const tabName = window.location.hash.substr(1) || 'syllabus'; // Get the hash fragment and remove '#'
	console.log(`Initial tab to load: ${tabName}`);
	$('.nav-link').removeClass('active');
	$(`.nav-link[data-tabname="${tabName}"]`).addClass('active');
	loadTabContent(tabName);
}

function handleFormSubmit(e) {
	e.preventDefault();
	const form = $(this);

	if (isSubmitting) {
		console.log('Form submission blocked due to pending submission.');
		return;
	}
	isSubmitting = true;
	console.log('Handling form submission for action:', form.attr('action'));

	const url_suffix = getUrlSuffix();
	$.post(form.attr('action'), form.serialize(), function(response) {
		console.log('Form submission success for action:', form.attr('action'));

		if (response.html) {
			$('#tab-content-container').html(response.html);
			console.log('Re-attaching form submit handler after content reload.');
			attachFormSubmitHandler(); // Re-attach for dynamically loaded content
		}

		if (response.close_modal) {
			$('.modal').modal('hide');
			$('.modal-backdrop').remove();
		}

		isSubmitting = false;
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Form submission failed:', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to submit form. Please try again.');
		isSubmitting = false;
	});
}

function attachFormSubmitHandler() {
	console.log('Attaching form submit handler...');
	$(document).off('submit', 'form');
	$(document).on('submit', 'form', handleFormSubmit);
}

function initializeEventListeners() {
	console.log('Initializing event listeners...');
	$('a[data-tabname]').off('click').on('click', function(e) {
		e.preventDefault();
		const tabName = $(this).data('tabname');
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
		console.log(`Tab clicked: ${tabName}`);
		loadTabContent(tabName);
	});

	attachFormSubmitHandler();

	$(window).off('hashchange').on('hashchange', function() {
		console.log('Hash changed. Loading initial tab.');
		loadInitialTab();
	});
}

$(document).ready(function() {
	console.log('Document ready. Loading initial tab.');
	loadInitialTab();
	initializeEventListeners();
});