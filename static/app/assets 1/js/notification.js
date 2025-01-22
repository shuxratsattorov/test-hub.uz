function toggleNotificationPage(event) {
    event.stopPropagation(); // Tashqi bosishlarni bloklash
    var notificationPage = document.getElementById("notificationPage");

    if (notificationPage.style.display === "none" || notificationPage.style.display === "") {
        notificationPage.style.display = "block";
    } else {
        notificationPage.style.display = "none";
    }
}

// Sahifa bo'sh joyiga bosilganda yopish
document.addEventListener("click", function(event) {
    var notification = document.querySelector(".header-menu__notification");
    var notificationPage = document.getElementById("notificationPage");

    // Faqat .notification yoki notificationPage ichida bo'lmagan joylarga bosilsa
    if (!notification.contains(event.target) && !notificationPage.contains(event.target) && notificationPage.style.display === "block") {
        notificationPage.style.display = "none";
    }
});
