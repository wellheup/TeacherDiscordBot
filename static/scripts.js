function getUrlSuffix() {
	return new URL(window.location.href).searchParams.get('url_suffix') || '';
}
// Function to load tab content
function loadTabContent(tabName) {
	const url_suffix = getUrlSuffix();
	const url = `/${tabName}?url_suffix=${url_suffix}`;
	$.get(url, function(data) {
		$('#tab-content-container').html(data);
		attachFormSubmitHandler(); // Re-attach form submit handler after loading new content
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Failed to load content: ', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to load content. Please try again.');
	});
}

// Function to load the initial tab based on the hash fragment
function loadInitialTab() {
	const tabName = window.location.hash.substr(1) || 'syllabus'; // Get the hash fragment and remove '#'
	$('.nav-link').removeClass('active');
	$(`.nav-link[data-tabname="${tabName}"]`).addClass('active');
	loadTabContent(tabName);
}

// Function to handle form submission via AJAX
function handleFormSubmit(e) {
	e.preventDefault();
	const form = $(this);

	console.log('Handling form submission for action:', form.attr('action'));
	const url_suffix = getUrlSuffix();
	$.post(form.attr('action'), form.serialize(), function(response) {
		if (response.html) {
			$('#tab-content-container').html(response.html);
		}
		if (response.close_modal) {
			$('.modal').modal('hide');
			$('.modal-backdrop').remove();
		}
		console.log('Form submission completed for action:', form.attr('action'));
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.error('Form submission failed: ', textStatus, errorThrown);
		$('#tab-content-container').html('Failed to submit form. Please try again.');
	});
}

// Ensure single event listener for form submissions via AJAX
function attachFormSubmitHandler() {
	$(document).off('submit', 'form').on('submit', 'form', handleFormSubmit);
}

$(document).ready(function() {
	loadInitialTab();

	// Handle tab clicks
	$('a[data-tabname]').on('click', function(e) {
		e.preventDefault();
		const tabName = $(this).data('tabname');
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
		loadTabContent(tabName);
	});

	$(window).on('hashchange', function() {
		loadInitialTab();
	});

	attachFormSubmitHandler(); // Attach form submit handler initially

	// Show modal for new bug with a single event listener
	$('#newBugButton').off('click').on('click', function() {
		$('#newBugForm').modal('show');
	});

	// Show modal for new assignment with a single event listener
	$('#newAssignmentButton').off('click').on('click', function() {
		$('#newAssignmentForm').modal('show');
	});
});