
document.addEventListener('DOMContentLoaded', function () {
    const menuButtons = document.querySelectorAll('.menu-btn');
    let activeMenu = null;

    menuButtons.forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.stopPropagation();

            const menu = this.nextElementSibling;

            if (activeMenu && activeMenu !== menu) {
                activeMenu.classList.remove('show-menu');
            }

            menu.classList.toggle('show-menu');
            activeMenu = menu.classList.contains('show-menu') ? menu : null;

            // Tashqi bosishlarda menyuni yopish
            document.addEventListener('click', function closeMenu(e) {
                if (activeMenu && !menu.contains(e.target)) {
                    activeMenu.classList.remove('show-menu');
                    activeMenu = null;
                    document.removeEventListener('click', closeMenu);
                }
            });
        });
    });
});
