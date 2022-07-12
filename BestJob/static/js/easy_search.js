function easySearch() {
    var searchText = document.getElementById('search-keywords').value;
    var link = 'search/?q='
    if (searchText === '') {
        window.location.href = link + 'разработчик'
    } else {
        window.location.href = link + searchText
    }
}

// Get the input field
var input = document.getElementById("search-keywords");

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("search_button").click();
  }
});