document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Autofillni o'chirish
    emailInput.setAttribute('autocomplete', 'off');
    passwordInput.setAttribute('autocomplete', 'new-password');
    
    // Ko'zcha tugmasini bosganda parol ko'rinishini o'zgartirish
    const eyeIcon = document.getElementById("eye-icon");
    if (eyeIcon) {
        eyeIcon.addEventListener('click', togglePassword);
    }

    // Bildirishnoma sahifasini ochish/yopish uchun tugma
    const notificationBtn = document.getElementById("notificationBtn");
    if (notificationBtn) {
        notificationBtn.addEventListener('click', toggleNotificationPage);
    }
    
    // Sahifa bo'sh joyiga bosilganda bildirishnomani yopish
    document.addEventListener("click", function (event) {
        const notification = document.querySelector(".notification");
        const notificationPage = document.getElementById("notificationPage");

        if (notificationPage && notification && !notification.contains(event.target) && 
            !notificationPage.contains(event.target) && 
            notificationPage.style.display === "block") {
            notificationPage.style.display = "none";
        }
    });
});

// Parol ko'rinishini o'zgartirish funksiyasi
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

// Bildirishnoma sahifasini ochish/yopish funksiyasi
function toggleNotificationPage(event) {
    event.stopPropagation(); // Tashqi bosishlarni bloklash
    const notificationPage = document.getElementById("notificationPage");

    if (notificationPage) {
        if (notificationPage.style.display === "none" || notificationPage.style.display === "") {
            notificationPage.style.display = "block";
        } else {
            notificationPage.style.display = "none";
        }
    }
}
