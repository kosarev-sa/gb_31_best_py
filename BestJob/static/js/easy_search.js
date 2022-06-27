function easySearch() {
    var searchText = document.getElementById('search-keywords').value;
    var link = 'search/?q='
    if (searchText === '') {
        window.location.href = link + 'разработчик'
    } else {
        window.location.href = link + searchText
    }
}