function toggleLogoutMenu(event) {
    if (window.matchMedia("(max-width: 1024px)").matches) {
        event.stopPropagation();
        var logoutMenu = document.getElementById("logoutMenu");

        if (logoutMenu.style.display === "none" || logoutMenu.style.display === "") {
            logoutMenu.style.display = "block";
        } else {
            logoutMenu.style.display = "none";
        }
    }
}

if (window.matchMedia("(max-width: 1024px)").matches) {
    document.addEventListener("click", function(event) {
        var logoutMenu = document.getElementById("logoutMenu");
        if (logoutMenu && !logoutMenu.contains(event.target)) {
            logoutMenu.style.display = "none";
        }
    });
}