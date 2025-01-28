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
