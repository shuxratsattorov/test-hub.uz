// Tugmalar uchun animatsiya effekti

document.querySelectorAll('.animation-button').forEach(button => {
    button.addEventListener('click', function (event) {
        const rect = button.getBoundingClientRect();

        const circle = document.createElement('span');
        const diameter = Math.max(rect.width, rect.height);
        const radius = diameter / 2;

        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - rect.left - radius}px`;
        circle.style.top = `${event.clientY - rect.top - radius}px`;

        button.appendChild(circle);

        setTimeout(() => {
            circle.remove();
        }, 300);
    });
});

// Jadval satrlari uchun rang berish

// HTML elementlarini tanlash
const rows = document.querySelectorAll('.table-row');

// Har bir satrni tekshirish va rang berish
rows.forEach((row, index) => {
    if (index % 2 === 0) {
        // Juft satrlar (0, 2, 4...) uchun fon rangi
        row.style.backgroundColor = '#E0E4EA'; 
    } else {
        // Toq satrlar (1, 3, 5...) uchun fon rangi
        row.style.backgroundColor = '#ffffff'; 
    }
});