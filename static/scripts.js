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

function openEditEntryPopup(button, index) {
	const popup = document.getElementById('editEntryForm');
	const row = button.closest('tr');
	const cells = row.querySelectorAll('td > div');
	const popupInputs = popup.querySelectorAll('input');

	popupInputs.forEach(input => {
		const columnName = input.name;
		const cell = Array.from(cells).find(cell => cell.getAttribute('name') === columnName);

		if (input.type === 'checkbox') {
			input.checked = cell.textContent.trim() === '✔';
		} else if(input.type === 'date') {
			input.value = cell.textContent.trim() || '';
		} else if (input.tagName.toLowerCase() === 'input') {
			input.value = cell.textContent.trim();
		}
	});

	popup.style.display = 'block';
}

function openConfirmDeletePopup(button, index) {
	const popup = document.getElementById('confirmDeleteForm');
	const unique_id = popup.querySelector('input[type="number"]');
	unique_id.value = index;
	
	popup.style.display = 'block';
}

function openNewAssignmentPopup(button) {
	const popup = document.getElementById('newAssignmentForm');

	popup.style.display = 'block';
}

function openNewBugPopup(button) {
	const popup = document.getElementById('newBugForm');

	popup.style.display = 'block';
}

function closePopup(popup) {
	popup.style.display = 'none';
}