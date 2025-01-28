function togglePassword(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const eyeIcon = document.getElementById(iconId);

    if (passwordInput.type === "password") {
        passwordInput.type = "text"; // Parolni ko'rinadigan qilish
        eyeIcon.src = "assets/icon/eye closed.svg"; // Ko'zcha tasvirini o'zgartirish
        eyeIcon.alt = "Hide Password";
    } else {
        passwordInput.type = "password"; // Parolni yashirish
        eyeIcon.src = "assets/icon/eye opened.svg"; // Dastlabki ko'zcha tasviri
        eyeIcon.alt = "Show Password";
    }
}
