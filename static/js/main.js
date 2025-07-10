$(document).ready(function() {
    $(document).on('click', '.content-link', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        loadContent(url);
    });
});

function loadContent(url) {
    $.ajax({
        url: url,
        type: 'GET',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function(response) {
            if (response.status === 'success') {
                $('#content-area').html(response.html);
                document.title = response.title;
                window.history.pushState({path: url}, response.title, response.url);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            $('#content-area').html('<div class="alert alert-danger">İçerik yüklenirken bir hata oluştu</div>');
        }
    });
}
