// tab switching
// function openTab(evt, tabName) {
// 	var i, tabcontent, tablinks, listItems;

// 	tabcontent = document.getElementsByClassName("tabcontent");
// 	for (i = 0; i < tabcontent.length; i++) {
// 		tabcontent[i].style.display = "none";
// 	}

// 	tablinks = document.getElementsByClassName("nav-link");
// 	for (i = 0; i < tablinks.length; i++) {
// 		tablinks[i].style.backgroundColor = "white";
// 		tablinks[i].className = tablinks[i].className.replace(" active", "");
// 	}

// 	document.getElementById(tabName).style.display = "block";
// 	evt.currentTarget.style.backgroundColor = "lightgrey";
// 	evt.currentTarget.className += " active";

// }

//retreive tab content by tabname for ajax style insertion
// function loadTabContent(tabName) {
// 	$.get('/' + tabName, function(data) {
// 		$('#' + tabName).html(data);
// 	}).fail(function(jqXHR, textStatus, errorThrown) {
// 		console.error('Failed to load content: ', textStatus, errorThrown);
// 	});
// }
// when ready to switch to ajax, make a route return for each tab, remove/adjust the if current_tab clauses, inject into a single div

$(document).ready(function(){
	$('a[data-tabname]').on('click', function (e) {
		e.preventDefault();
		var tabName = $(this).data('tabname');
		$('.nav-link').removeClass('active');
		$(this).addClass('active');

		$('.tab-pane').removeClass('show active');
		$('.tab-pane').css('display', 'none');
		$('#' + tabName).addClass('show active');
		$('#' + tabName).css('display', 'block');
		loadTabContent(tabName);
	});
});

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

