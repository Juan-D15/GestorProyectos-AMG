// Toggle password visibility in login form
function togglePassword() {
    const passwordInput = document.querySelector('input[name="password"]');
    const eyeIcon = document.getElementById('eyeIcon');
    const eyeOffIcon = document.getElementById('eyeOffIcon');
    
    if (passwordInput && eyeIcon && eyeOffIcon) {
        const isPassword = passwordInput.getAttribute('type') === 'password';
        passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
        
        // Toggle visibility using display property for more reliable behavior
        if (isPassword) {
            eyeIcon.style.display = 'none';
            eyeOffIcon.style.display = 'inline-block';
        } else {
            eyeIcon.style.display = 'inline-block';
            eyeOffIcon.style.display = 'none';
        }
    }
}

// Redirect after logout message (3 seconds)
// This function is called from the Django template when logout_message is present
function redirectAfterLogout() {
    setTimeout(function() {
        window.location.href = '/login/';
    }, 3000);
}
