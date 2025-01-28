function moveFocus(index) {
    const input = document.getElementById("code" + index);
    if (input.value.length === 1) {
        if (index < 6) {
            document.getElementById("code" + (index + 1)).focus();
        }
    }
}

function handleBackspace(event, index) {
    const input = document.getElementById("code" + index);
    if (event.key === "Backspace" && input.value === "") {
        if (index > 1) {
            document.getElementById("code" + (index - 1)).focus();
        }
    }
}

function combineCode(event) {
    // Get the values from each input field
    const code = [];
    for (let i = 1; i <= 6; i++) {
        code.push(document.getElementById("code" + i).value);
    }

    // Combine the code into a single string
    const fullCode = code.join("");

    // Add the combined code to the hidden input
    document.getElementById("fullCode").value = fullCode;

    // Validate: only submit if the code is exactly 6 digits long
    if (fullCode.length !== 6) {
        event.preventDefault(); // Prevent the form from submitting
        alert("Please enter a valid 6-digit code.");
    }
}
