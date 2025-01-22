// *** Notification Page Toggles ***
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

// *** Input Management ***
const maxInputs = 5;
let inputCount = 1;

document.getElementById('add-input').addEventListener('click', function () {
    if (inputCount < maxInputs) {
        const inputContainer = document.getElementById('input-container');
        const newInputDiv = document.createElement('div');
        newInputDiv.classList.add('input-radio-pair');

        const nameIndex = inputCount;

        newInputDiv.innerHTML = `
            <input class="add-test__answer-input add-test__answer-input-js" type="text" name="answers-${nameIndex}-answer" placeholder="Variant ${inputCount + 1} ni kiriting">
            <label class="custom-checkbox">
            <input class="single-select" type="checkbox" id="option${nameIndex}" name="answers-${nameIndex}-is_correct" value="${nameIndex}">
            <span class="checkmark"></span>
            </label>
            <button type="button" class="delete-btn"><img src="assets/icon/delete.svg"></button>
            <div class="answer-error">
                <p>error answer</p>
            </div>
        `;

        inputContainer.appendChild(newInputDiv);
        inputCount++;

        const deleteButton = newInputDiv.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function () {
            newInputDiv.remove();
            inputCount--;
            updateInputNames();
        });

        newInputDiv.querySelector('.single-select').addEventListener('change', handleSingleSelect);
    } else {
        alert('Maksimal 5 ta variant qo\'shishingiz mumkin');
    }
});

function handleSingleSelect() {
    const checkboxes = document.querySelectorAll('.single-select');
    checkboxes.forEach((checkbox) => {
        if (checkbox !== this) {
            checkbox.checked = false;
        }
    });
}

function updateInputNames() {
    const inputPairs = document.querySelectorAll('.input-radio-pair');
    inputPairs.forEach((pair, index) => {
        const textInput = pair.querySelector('input[type="text"]');
        const checkboxInput = pair.querySelector('input[type="checkbox"]');

        textInput.name = `answers-${index}-answer`;
        checkboxInput.id = `option${index}`;
        checkboxInput.value = index;
    });
}

// Checkbox change listeners
document.querySelectorAll('.single-select').forEach((checkbox) => {
    checkbox.addEventListener('change', handleSingleSelect);
});

// *** Scroll Text Animation ***
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

// *** Dropdown Menu Toggles ***
document.addEventListener('DOMContentLoaded', function () {
    const menuButtons = document.querySelectorAll('.menu-btn');
    let activeMenu = null;

    menuButtons.forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.stopPropagation();

            const menu = this.nextElementSibling;

            // Oldingi ochilgan menyuni yopish
            if (activeMenu && activeMenu !== menu) {
                activeMenu.classList.remove('show-menu');
            }

            // Hozirgi menyuni ochish yoki yopish
            menu.classList.toggle('show-menu');
            activeMenu = menu.classList.contains('show-menu') ? menu : null;

            // Tashqariga bosilganda menyuni yopish
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

