function fetchAuthorBooks(author) {
	const url_suffix = new URLSearchParams(window.location.search).get('url_suffix');
	$.get('/author_books', { author: author, url_suffix: url_suffix }, function(data) {
		$('#author-content-container .modal-content').html(data);
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.log('Failed to fetch author books: ', textStatus, errorThrown);
		$('#author-content-container .modal-content').html('<p>Failed to fetch author books. Please try again.</p>');
	});
}

$(document).ready(function() {
	const columnsToKeep = ['book', 'author', 'series', 'is_completed', 'date_completed', 'num_in_series'];
	// Initialize the toggle switch
	$("[name='column-visibility-toggle']").bootstrapSwitch({
		onText: "Less",
		offText: "More",
		labelText: "Columns",
		onColor: "info",
		offColor: "primary",
		state: false  // Default state is off
	});
	// Set initial hidden state for columns
	toggleColumnVisibilityBySwitchState(false);
	// Listen for switch state change
	$("[name='column-visibility-toggle']").on('switchChange.bootstrapSwitch', function (event, state) {
		toggleColumnVisibilityBySwitchState(state);
	});
	
	function toggleColumnVisibilityBySwitchState(state) {
	  const elements = document.querySelectorAll('.table td, .table th');
	  elements.forEach(el => {
		const columnClasses = Array.from(el.classList).filter(c => c.startsWith('col-'));
		columnClasses.forEach(columnClass => {
		  const columnName = columnClass.replace('col-', '');
		  if (!columnsToKeep.includes(columnName)) {
			el.style.display = state ? '' : 'none';
		  }
		});
	  });
	}

	// new assignment pop-up
	$('#newAssignmentButton').on('click', function() {
		$('#newAssignmentForm').modal('show');
	});

	
	// new book pop-up
	$('#addNewBookButton').on('click', function() {
		$('#newEntryForm').modal('show');
	});

	// bulk add pop-up
	$('#bulkAddButton').on('click', function() {
		$('#bulkAddForm').modal('show');
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

	// Handle the author link click event
	$(document).on('click', '.author-link', function(e) {
		e.preventDefault();
		const authorName = $(this).data('author');
		fetchAuthorBooks(authorName);
		$('#author-content-container').modal('show');
	});
});