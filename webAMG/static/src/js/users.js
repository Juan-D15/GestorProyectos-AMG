// Modal functions
function openModal(type) {
    document.getElementById(type + 'Modal').classList.remove('hidden');
}

function closeModal(type) {
    document.getElementById(type + 'Modal').classList.add('hidden');
}

// Select user function
function selectUser(row) {
    event.stopPropagation();
    
    // Remove selection from all rows
    document.querySelectorAll('.user-row').forEach(r => {
        r.classList.remove('bg-[#8a4534]/10');
    });
    
    // Add selection to clicked row
    row.classList.add('bg-[#8a4534]/10');
}

// Edit user function
function editUser(event, button) {
    event.stopPropagation();
    const userId = button.getAttribute('data-user-id');
    document.getElementById('editUserId').value = userId;
    document.getElementById('editUsername').value = button.getAttribute('data-username');
    document.getElementById('editEmail').value = button.getAttribute('data-email');
    document.getElementById('editFullName').value = button.getAttribute('data-full-name');
    document.getElementById('editRole').value = button.getAttribute('data-role');
    document.getElementById('editIsActive').checked = button.getAttribute('data-is-active') === 'true';
    document.getElementById('editForm').action = '/dashboard/usuarios/editar/';
    openModal('edit');
}

// Delete user function
function deleteUser(event, button) {
    event.stopPropagation();
    const userId = button.getAttribute('data-user-id');
    document.getElementById('deleteUserId').value = userId;
    document.getElementById('deletePassword').value = '';
    openModal('delete');
}

// Password visibility toggle for create modal
function toggleCreatePassword() {
    const passwordInput = document.getElementById('createPassword');
    const eyeIcon = document.getElementById('createPasswordEye');
    const eyeSlashIcon = document.getElementById('createPasswordEyeSlash');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.style.display = 'none';
        eyeSlashIcon.style.display = 'inline';
    } else {
        passwordInput.type = 'password';
        eyeIcon.style.display = 'inline';
        eyeSlashIcon.style.display = 'none';
    }
}

// Password visibility toggle for edit modal
function toggleEditPassword() {
    const passwordInput = document.getElementById('editPassword');
    const eyeIcon = document.getElementById('editPasswordEye');
    const eyeSlashIcon = document.getElementById('editPasswordEyeSlash');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.style.display = 'none';
        eyeSlashIcon.style.display = 'inline';
    } else {
        passwordInput.type = 'password';
        eyeIcon.style.display = 'inline';
        eyeSlashIcon.style.display = 'none';
    }
}

// Password visibility toggle for delete modal
function toggleDeletePassword() {
    const passwordInput = document.getElementById('deletePassword');
    const eyeIcon = document.getElementById('deletePasswordEye');
    const eyeSlashIcon = document.getElementById('deletePasswordEyeSlash');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.style.display = 'none';
        eyeSlashIcon.style.display = 'inline';
    } else {
        passwordInput.type = 'password';
        eyeIcon.style.display = 'inline';
        eyeSlashIcon.style.display = 'none';
    }
}

// Filter users by username
function filterUsers() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const userRows = document.querySelectorAll('.user-row');
    
    userRows.forEach(row => {
        const username = row.getAttribute('data-username').toLowerCase();
        if (username.includes(searchInput)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Close modals when clicking outside
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('fixed')) {
        event.target.classList.add('hidden');
    }
});
