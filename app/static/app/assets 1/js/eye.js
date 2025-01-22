function togglePassword() {
    const passwordInput = document.getElementById("password");
    const eyeIcon = document.getElementById("eye-icon");

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