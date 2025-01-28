// Elementlarni olish
const menuToggle = document.getElementById('burger');
const burger = document.getElementById('burger');
const navbar = document.getElementById('navbar');
const overlay = document.getElementById('overlay');

// Menu-toggle bosilganda burger animatsiyasini almashtirish
menuToggle.addEventListener('click', function () {
    const burgerIcon = document.querySelector('.header-menu__burger');
    burgerIcon.classList.toggle('toggle');
});

// Navbarni ochish va yopish funksiyasi
function toggleNavbar() {
    const isNavbarOpen = navbar.classList.contains('open');
    const burgerIcon = document.querySelector('.header-menu__burger');
    if (isNavbarOpen) {
        // Navbarni yopish
        navbar.classList.remove('open');
        overlay.classList.remove('active');
        burgerIcon.classList.remove('toggle'); // Burgerni asl holatiga qaytarish
    } else {
        // Navbarni ochish
        navbar.classList.add('open');
        overlay.classList.add('active');
        burgerIcon.classList.add('toggle'); // Burgerni aktiv holatga o‘tkazish
    }
}

// Hodisalarni tinglash
burger.addEventListener('click', toggleNavbar);
overlay.addEventListener('click', () => {
    const burgerIcon = document.querySelector('.header-menu__burger');
    navbar.classList.remove('open');
    overlay.classList.remove('active');
    burgerIcon.classList.remove('toggle'); // Burgerni asl holatiga qaytarish
});
