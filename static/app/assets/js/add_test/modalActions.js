const modal = document.getElementById('deleteModal');

        // Modalni ochish funksiyasi
        function openModal() {
          modal.style.display = 'flex';
        }

        // Modalni yopish funksiyasi
        function closeModal() {
          modal.style.display = 'none';
        }

        // Tasdiqlash funksiyasi
        function confirmDelete() {
          // Bu yerda o'chirish amali bajariladi (hozircha faqat modalni yopamiz)
          closeModal();
        }