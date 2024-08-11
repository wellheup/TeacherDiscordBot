function getUrlSuffix() {
	return new URL(window.location.href).searchParams.get('url_suffix') || '';
}
// Function to load tab content
function loadTabContent(tabName) {
	const url_suffix = getUrlSuffix();
	const url = `/${tabName}?url_suffix=${url_suffix}`;
	$.get(url, function(data) {
		$('#tab-content-container').html(data);
		toggleColumnVisibility();
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
// Function to toggle column visibility based on checkboxes
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

// Function to handle form submission via AJAX
function handleFormSubmit(e) {
	e.preventDefault();
	const form = $(this);

	console.log('Handling form submission for action:', form.attr('action'));
	const url_suffix = getUrlSuffix();
	$.post(form.attr('action'), form.serialize(), function(response) {
		if (response.html) {
			$('#tab-content-container').html(response.html);
			toggleColumnVisibility();
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
	$('a[data-tabname]').on('click', function(e) {
		e.preventDefault();
		const tabName = $(this).data('tabname');
		const url_suffix = getUrlSuffix();
		window.location.hash = tabName; // Update URL hash
		loadTabContent(tabName);
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
	});
	$(window).on('hashchange', function() {
		loadInitialTab();
	});
	toggleColumnVisibility();
	attachFormSubmitHandler(); // Attach form submit handler initially


	// Show modal for new bug with a single event listener
	$('#newBugButton').off('click').on('click', function() {
		$('#newBugForm').modal('show');
	});

	// Show modal for new bug with a single event listener
	$('#newAssignmentButton').off('click').on('click', function() {
		$('#newAssignmentButton').modal('show');
	});
});