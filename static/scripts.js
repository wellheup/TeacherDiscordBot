let isSubmitting = false;
let lastRandomTodoSeries = null;

function renderRandomTodoSeries() {
	const seriesItems = Array.from(
		document.querySelectorAll('#todo .todo-series-item'),
	);
	if (!seriesItems.length) {
		return false;
	}

	let choices = seriesItems;
	if (seriesItems.length > 1 && lastRandomTodoSeries) {
		const differentSeries = seriesItems.filter(
			(item) => item !== lastRandomTodoSeries,
		);
		if (differentSeries.length > 0) {
			choices = differentSeries;
		}
	}

	const selected = choices[Math.floor(Math.random() * choices.length)];
	lastRandomTodoSeries = selected;

	const seriesName = selected
		.querySelector('.todo-series-name')
		.textContent.trim();
	document.getElementById('randomSeriesModalLabel').textContent = seriesName;
	document.getElementById('randomSeriesAuthor').textContent =
		selected.dataset.author || '';

	const booksList = document.getElementById('randomSeriesBooks');
	booksList.replaceChildren();
	const books = selected.querySelectorAll('.todo-series-books > li');
	books.forEach((book) => {
		const listItem = document.createElement('li');
		listItem.textContent = book.textContent.trim();
		booksList.appendChild(listItem);
	});

	if (!books.length) {
		const emptyMessage = document.createElement('li');
		emptyMessage.textContent = 'No books are currently listed for this series.';
		booksList.appendChild(emptyMessage);
	}
	return true;
}

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

	$(document)
		.off('click', '#pickRandomSeriesButton')
		.on('click', '#pickRandomSeriesButton', function() {
			if (renderRandomTodoSeries()) {
				$('#randomSeriesModal').modal('show');
			}
		});

	$(document)
		.off('click', '#rerollRandomSeriesButton')
		.on('click', '#rerollRandomSeriesButton', function() {
			renderRandomTodoSeries();
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