```javascript
// ...existing code...
function loadContent(url) {
    $.ajax({
        url: url,
        type: 'GET',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function(response) {
            if (response.status === 'success') {
                $('#content-area').html(response.content);
                document.title = response.title;
                history.pushState({}, response.title, url);
            } else {
                console.error('Error loading content:', response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', error);
        }
    });
}
// ...existing code...
```