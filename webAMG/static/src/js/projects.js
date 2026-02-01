// Modal functions
function openModal(type) {
    document.getElementById(type + 'Modal').classList.remove('hidden');
}

function closeModal(type) {
    document.getElementById(type + 'Modal').classList.add('hidden');
}

// Image preview function
function previewImage(input) {
    const previewContainer = document.getElementById('imagePreviewContainer');
    const preview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeImageBtn');
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            removeBtn.classList.remove('hidden');
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Remove cover image function
function removeCoverImage() {
    const input = document.getElementById('coverImageInput');
    const previewContainer = document.getElementById('imagePreviewContainer');
    const preview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeImageBtn');
    
    input.value = '';
    preview.src = '';
    previewContainer.classList.add('hidden');
    removeBtn.classList.add('hidden');
}
