const scrollTexts = document.querySelectorAll('.scroll-text');
const speed = 0.5; // Matn harakat tezligi

function animateText(scrollText) {
    let position = 0;
    const containerWidth = scrollText.parentElement.clientWidth;
    const textWidth = scrollText.scrollWidth;

    function animate() {
        // Agar matn to'liq o'ng tomonga chiqib ketsa, yana chapdan boshlanadi
        if (position >= containerWidth) {
            position = -textWidth; // Matnni chap tomonga tashlaymiz
        }

        // Matnni harakatlantirish
        position += speed;
        scrollText.style.transform = `translateX(${position}px)`;

        // Har 20ms da qaytadan chaqiramiz
        requestAnimationFrame(animate, 30);
    }

    animate();
}

// Barcha .scroll-text elementlari uchun animatsiyani boshlaymiz
scrollTexts.forEach(scrollText => animateText(scrollText));
