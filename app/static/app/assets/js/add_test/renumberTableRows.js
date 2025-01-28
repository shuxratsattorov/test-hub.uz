function renumberTableRows() {
          const rows = document.querySelectorAll('.add-test__table-row');

          rows.forEach((row, index) => {
            const firstCell = row.querySelector('td:first-child');
            if (firstCell) {
              firstCell.textContent = index + 1;
            }
          });
        }

        renumberTableRows();