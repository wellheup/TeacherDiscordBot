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
	loadTabContent('syllabus');

	// Handle tab clicks
	$('a[data-tabname]').on('click', function(e) {
		e.preventDefault();
		var tabName = $(this).data('tabname');
		console.log('Tab clicked:', tabName);
		$('.nav-link').removeClass('active');
		$(this).addClass('active');
		loadTabContent(tabName);
	});

	// new assignment pop-up
	$('#newAssignmentButton').on('click', function() {
		$('#newAssignmentForm').modal('show');
	});

	// new book pop-up
	$('#addNewBookButton').on('click', function() {
		$('#newEntryForm').modal('show');
	});

	// edit book button
	$('[id^="edit-"]').on('click', function() {
		const popup = $('#editEntryForm');
		const row = $(this).closest('tr')[0];
		const cells = row.querySelectorAll('td > div');
		popup.find('input, checkbox, select').each(function() {
			const inputName = $(this).attr('name');
			const cell = Array.from(cells).find(cell => cell.getAttribute('name') === inputName);
			if ($(this).is(':checkbox')) {
				$(this).prop('checked', cell.textContent.trim() === '✔');
			} else {
				$(this).val(cell.textContent.trim());
			}
		});
		popup.modal('show');
	});

	// delete book button
	$('[id^="delete-"]').on('click', function() {
		const index = $(this).attr('id').split('-')[1];
		const popup = $('#confirmDeleteForm');
		popup.find('input[type="number"]').val(index);
		popup.modal('show');
	});

	// new bug pop-up
	$('#newBugButton').on('click', function() {
		$('#newBugForm').modal('show');
	});
});