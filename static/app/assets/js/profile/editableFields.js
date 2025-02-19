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
