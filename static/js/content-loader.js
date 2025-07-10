$(document).ready(function() {
    // Sayfa içi linklere tıklandığında
    $(document).on('click', '.page-link', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        loadPageContent(url);
    });
});

function loadPageContent(url) {
    $.ajax({
        url: url,
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        success: function(response) {
            $('#main-content').html(response.content);
            document.title = response.title;
            history.pushState({}, '', url);
        },
        error: function() {
            alert('İçerik yüklenirken hata oluştu!');
        }
    });
}
