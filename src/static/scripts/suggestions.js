document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('suggestions');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value;

            if (query.length > 0) {
                fetch(`/autocomplete?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        const suggestions = data.suggestions;

                        if (suggestions.length > 0) {
                            suggestionsBox.innerHTML = suggestions
                                .map(s => `<li class="suggestion-item">${s}</li>`)
                                .join('');
                            suggestionsBox.classList.remove('hidden');

                            // Add click event listener to each suggestion item
                            const suggestionItems = document.querySelectorAll('.suggestion-item');
                            suggestionItems.forEach(item => {
                                item.addEventListener('click', function () {
                                    searchInput.value = this.textContent; // Replace search bar text
                                    suggestionsBox.classList.add('hidden'); // Hide suggestions list
                                });
                            });
                        } else {
                            suggestionsBox.innerHTML = '';
                            suggestionsBox.classList.add('hidden');
                        }
                    })
                    .catch(() => {
                        suggestionsBox.innerHTML = '';
                        suggestionsBox.classList.add('hidden'); // Hide on error
                    });
            } else {
                suggestionsBox.innerHTML = '';
                suggestionsBox.classList.add('hidden'); // Hide when input is empty
            }
        });
    } else {
        console.error("Search input element not found.");
    }
});
