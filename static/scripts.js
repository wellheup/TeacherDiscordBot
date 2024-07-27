// tab switching
function openTab(evt, tabName) {
	var i, tabcontent, tablinks;

	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
	tabcontent[i].style.display = "none";
	}

	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
	tablinks[i].className = tablinks[i].className.replace(" active", "");
	}

	document.getElementById(tabName).style.display = "block";
	evt.currentTarget.className += " active";
}

// new assignment pop-up
$(document).ready(function () {
	$('#newAssignmentButton').on('click', function () {
		$('#newAssignmentForm').modal('show');
	});
});

// new book pop-up
$(document).ready(function () {
	$('#addNewBookButton').on('click', function () {
		$('#newEntryForm').modal('show');
	});
});

// edit book button
$(document).ready(function () {
	$('[id^="edit-"]').on('click', function () {
		const popup = $('#editEntryForm');
		const row = $(this).closest('tr')[0];
		const cells = row.querySelectorAll('td > div');
		popup.find('input, checkbox, select').each(function () {
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
});

// delete book button
$(document).ready(function () {
	$('[id^="delete-"]').on('click', function () {
		const index = $(this).attr('id').split('-')[1];
		const popup = $('#confirmDeleteForm');
		popup.find('input[type="number"]').val(index);
		popup.modal('show');
	});
});

// new bug pop-up
$(document).ready(function () {
	$('#newBugButton').on('click', function () {
		$('#newBugForm').modal('show');
	});
});

