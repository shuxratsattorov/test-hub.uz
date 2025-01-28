const scrollTexts = document.querySelectorAll('.scroll-text');
const speed = 0.5;

function animateText(scrollText) {
    let position = 0;
    const containerWidth = scrollText.parentElement.clientWidth;
    const textWidth = scrollText.scrollWidth;

    function animate() {
        if (position >= containerWidth) {
            position = -textWidth;
        }
        position += speed;
        scrollText.style.transform = `translateX(${position}px)`;
        requestAnimationFrame(animate, 30);
    }
    animate();
}

scrollTexts.forEach(scrollText => animateText(scrollText));
