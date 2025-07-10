function loadContent(slug) {
    fetch(`/csharp/${slug}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('contentDetail').innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('contentDetail').innerHTML = 'İçerik yüklenirken bir hata oluştu.';
        });
}
