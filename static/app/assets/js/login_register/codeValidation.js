function moveFocus(index) {
    if (document.getElementById("code" + index).value.length === 1) {
      if (index < 6) {
        document.getElementById("code" + (index + 1)).focus();
      }
    }
  }

  function handleBackspace(event, index) {
    if (event.key === "Backspace" && document.getElementById("code" + index).value === "") {
      if (index > 1) {
        document.getElementById("code" + (index - 1)).focus();
      }
    }
  }

  function combineCode(event) {
    // Kodlarni birlashtirish
    const code = [];
    for (let i = 1; i <= 6; i++) {
      code.push(document.getElementById("code" + i).value);
    }

    // Yashirin inputga qiymatni qo'shish
    document.getElementById("fullCode").value = code.join("");
  }