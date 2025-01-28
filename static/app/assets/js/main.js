// Bildirishnoma sahifasini ochish/yopish uchun ishlatiladi
function toggleNotificationPage(event) {
    event.stopPropagation(); // Tashqi bosishlarni bloklash
    var notificationPage = document.getElementById("notificationPage");

    if (notificationPage.style.display === "none" || notificationPage.style.display === "") {
        notificationPage.style.display = "block";
    } else {
        notificationPage.style.display = "none";
    }
}

// Sahifada bo'sh joyga bosilganda bildirishnomani yopish
document.addEventListener("click", function(event) {
    var notification = document.querySelector(".header-menu__notification");
    var notificationPage = document.getElementById("notificationPage");

    if (!notification.contains(event.target) && !notificationPage.contains(event.target) && notificationPage.style.display === "block") {
        notificationPage.style.display = "none";
    }
});

// *** Kiritish maydonlarini boshqarish ***
// Foydalanuvchi javob variantlarini qo'shishi va boshqarishi uchun ishlatiladi
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
            <button type="button" class="delete-btn"><img src=".app/static/app/assets/icon/delete.svg"></button>
            <div class="answer-error">
                <p>error answer</p>
            </div>
        `;

        inputContainer.appendChild(newInputDiv);
        inputCount++;

        // Kiritilgan javobni o'chirish tugmachasini bog'lash
        const deleteButton = newInputDiv.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function () {
            newInputDiv.remove();
            inputCount--;
            updateInputNames();
        });

        // Bitta to'g'ri javob tanlashni boshqarish
        newInputDiv.querySelector('.single-select').addEventListener('change', handleSingleSelect);
    }
});

// Faqat bitta javobni tanlash uchun ishlatiladi
function handleSingleSelect() {
    const checkboxes = document.querySelectorAll('.single-select');
    checkboxes.forEach((checkbox) => {
        if (checkbox !== this) {
            checkbox.checked = false;
        }
    });
}

// Javob variantlari nomlarini yangilash
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

// *** Matnli skroll animatsiyasi ***
// Matnli bloklarni ekranda harakatlantirish uchun ishlatiladi
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

// *** Dropdown menyu o'zgarishlari ***
// Ochiladigan menyularni boshqarish uchun ishlatiladi
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

// *** O'zgartiriladigan maydonlar ***
// Matnni tahrirlash va saqlash imkonini beradi
function editField(event, field) {
    event.stopPropagation();
    const textElement = document.getElementById(field);
    const inputElement = document.getElementById(`edit-${field}`);

    inputElement.value = textElement.innerText;
    textElement.style.display = 'none';
    inputElement.style.display = 'block';
    inputElement.focus();
}

function saveField(field) {
    const textElement = document.getElementById(field);
    const inputElement = document.getElementById(`edit-${field}`);

    if (inputElement.value.trim() !== '') {
        textElement.innerText = inputElement.value;
    }

    inputElement.style.display = 'none';
    textElement.style.display = 'block';
}

// Tashqi bosishlarda tahrirni yopish
function closeAllInputs(event) {
    if (!event.target.closest('.editable') && event.target.tagName !== 'INPUT') {
        const inputs = document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            if (input.style.display === 'block') {
                const field = input.id.replace('edit-', '');
                saveField(field);
            }
        });
    }
}

document.addEventListener('click', closeAllInputs);

// *** Profil rasmi tahriri ***
// Foydalanuvchi profil rasmini almashtirishi uchun ishlatiladi
document.getElementById('edit-pic').addEventListener('change', function(event) {
    const newPic = event.target.files[0];

    if (newPic) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-pic').src = e.target.result;
        };
        reader.readAsDataURL(newPic);
    }
});

// *** Parolni tahrirlash ***
// Parol tahrir qilish formasi ko'rsatish va yashirish uchun ishlatiladi
function togglePasswordEdit(event) {
    event.stopPropagation();
    const editForm = document.getElementById('password-edit-form');
    const passwordDisplay = document.getElementById('password');

    if (editForm.style.display === 'none') {
        editForm.style.display = 'block';
        passwordDisplay.style.display = 'none';
    } else {
        editForm.style.display = 'none';
        passwordDisplay.style.display = 'block';
    }
}

// Tashqi bosishlarda parol formasini yopish
function closeInputs(event) {
    const editForm = document.getElementById('password-edit-form');
    const passwordDisplay = document.getElementById('password');

    if (event.target.closest('#password-edit-form')) {
        return;
    }

    if (editForm.style.display === 'block') {
        editForm.style.display = 'none';
        passwordDisplay.style.display = 'block';
    }
}

document.addEventListener('click', closeInputs);































// document.addEventListener('DOMContentLoaded', function () {
//     const emailInput = document.getElementById('email');
//     const passwordInput = document.getElementById('password');
    
//     // Autofillni o'chirish
//     emailInput.setAttribute('autocomplete', 'off');
//     passwordInput.setAttribute('autocomplete', 'new-password');
    
//     // Ko'zcha tugmasini bosganda parol ko'rinishini o'zgartirish
//     const eyeIcon = document.getElementById("eye-icon");
//     if (eyeIcon) {
//         eyeIcon.addEventListener('click', togglePassword);
//     }

//     // Bildirishnoma sahifasini ochish/yopish uchun tugma
//     const notificationBtn = document.getElementById("notificationBtn");
//     if (notificationBtn) {
//         notificationBtn.addEventListener('click', toggleNotificationPage);
//     }
    
//     // Sahifa bo'sh joyiga bosilganda bildirishnomani yopish
//     document.addEventListener("click", function (event) {
//         const notification = document.querySelector(".notification");
//         const notificationPage = document.getElementById("notificationPage");

//         if (notificationPage && notification && !notification.contains(event.target) && 
//             !notificationPage.contains(event.target) && 
//             notificationPage.style.display === "block") {
//             notificationPage.style.display = "none";
//         }
//     });
// });

// // Parol ko'rinishini o'zgartirish funksiyasi
// function togglePassword() {
//     const passwordInput = document.getElementById("password");
//     const eyeIcon = document.getElementById("eye-icon");

//     if (passwordInput.type === "password") {
//         passwordInput.type = "text"; // Parolni ko'rinadigan qilish
//         eyeIcon.src = "assets/icon/eye closed.svg"; // Ko'zcha tasvirini o'zgartirish
//         eyeIcon.alt = "Hide Password";
//     } else {
//         passwordInput.type = "password"; // Parolni yashirish
//         eyeIcon.src = "assets/icon/eye opened.svg"; // Dastlabki ko'zcha tasviri
//         eyeIcon.alt = "Show Password";
//     }
// }

// // Bildirishnoma sahifasini ochish/yopish funksiyasi
// function toggleNotificationPage(event) {
//     event.stopPropagation(); // Tashqi bosishlarni bloklash
//     const notificationPage = document.getElementById("notificationPage");

//     if (notificationPage) {
//         if (notificationPage.style.display === "none" || notificationPage.style.display === "") {
//             notificationPage.style.display = "block";
//         } else {
//             notificationPage.style.display = "none";
//         }
//     }
// }
