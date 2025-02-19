
const modal = document.getElementById('deleteModal');

function openModal() {
  modal.style.display = 'flex';
  localStorage.setItem('modalState', 'open');
}

function closeModal() {
  modal.style.display = 'none';
  localStorage.setItem('modalState', 'closed');
}

function confirmDelete() {
  closeModal();
}

window.onload = function() {
  const modalState = localStorage.getItem('modalState');
  if (modalState === 'open') {
    openModal();
  }
};






// const modal = document.getElementById('deleteModal');
//
//         // Modalni ochish funksiyasi
//         function openModal() {
//           modal.style.display = 'flex';
//         }
//
//         // Modalni yopish funksiyasi
//         function closeModal() {
//           modal.style.display = 'none';
//         }
//
//         // Tasdiqlash funksiyasi
//         function confirmDelete() {
//           // Bu yerda o'chirish amali bajariladi (hozircha faqat modalni yopamiz)
//           closeModal();
//         }