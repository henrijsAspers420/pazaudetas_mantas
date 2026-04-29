document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Attēla priekšskatījuma loģika lapā add_item.html
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const uploadPlaceholder = document.getElementById('upload-placeholder');

    if (dropZone && fileInput) {
        // Atver failu pārlūku uzspiežot uz laukuma
        dropZone.addEventListener('click', () => fileInput.click());

        // Apstrādā izvēlēto failu
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    previewContainer.classList.remove('hidden');
                    uploadPlaceholder.classList.add('hidden');
                }
                
                reader.readAsDataURL(file);
            }
        });
    }

    // 2. Mobilās izvēlnes loģika
    const mobileBtn = document.getElementById('mobile-menu-btn');
    if(mobileBtn) {
        mobileBtn.addEventListener('click', () => {
            // Šeit varat pievienot loģiku izvēlnes atvēršanai (modāla vai sānjoslas parādīšanai)
            alert("Atvērt mobilo izvēlni (tiks iestrādāts)");
        });
    }
});