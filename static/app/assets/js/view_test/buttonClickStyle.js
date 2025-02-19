document.querySelectorAll('.view-test-answer').forEach(button => {
        button.addEventListener('click', () => {
        // Qo'shimcha CSS sinfini qo'shish
        button.classList.add('view-test-red-temporary');

        // 3 soniyadan so'ng CSS sinfini olib tashlash
        setTimeout(() => {
            button.classList.remove('view-test-red-temporary');
        }, 1000); // 3000 millisekund = 3 soniya
        });
    });