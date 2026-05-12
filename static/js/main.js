document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const uploadPlaceholder = document.getElementById('upload-placeholder');

    if (dropZone && fileInput) {
        dropZone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.src = e.target.result;
                    previewContainer.style.display = 'block';
                    uploadPlaceholder.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
// Funkcija mantas atvēršanai
function openModal(card) {
    const modal = document.getElementById('item-modal');
    
    // Iegūstam datus no kartītes
    document.getElementById('modal-img').src = card.querySelector('img').src;
    document.getElementById('modal-title').innerText = card.querySelector('.card-title').innerText;
    document.getElementById('modal-badge').innerText = card.querySelector('.badge').innerText;
    document.getElementById('modal-desc').innerText = card.querySelector('.card-desc').innerText;
    document.getElementById('modal-date').innerText = card.querySelector('.card-date').innerText;

    modal.style.display = 'flex';
}

// Funkcija loga aizvēršanai
function closeModal(event) {
    document.getElementById('item-modal').style.display = 'none';
}

//Click event visām kartītēm
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card').forEach(card => {
        card.onclick = () => openModal(card);
    });
});