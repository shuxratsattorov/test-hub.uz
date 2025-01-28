document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Autofillni o'chirish
    emailInput.setAttribute('autocomplete', 'off');
    passwordInput.setAttribute('autocomplete', 'new-password');
});
