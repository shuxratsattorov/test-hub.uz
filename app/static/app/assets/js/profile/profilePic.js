
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
