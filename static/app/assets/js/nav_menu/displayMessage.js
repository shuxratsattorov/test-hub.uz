const notification = document.getElementById("notification-message");
    if (notification) {
        // Show the notification with slide-down effect
        notification.classList.add("show");

        // Set timeout to hide the notification after 3 seconds
        setTimeout(function() {
            notification.classList.remove("show");
        }, 3000);  // Adjust time as needed (3000 ms = 3 seconds)
    }