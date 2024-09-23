document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-btn');
    const closeModalBtn = document.getElementById('close-modal');
    const editModal = document.getElementById('edit-modal');
    const editForm = document.getElementById('edit-recipe-form');

    // Show the edit modal when the edit button is clicked
    editBtn.addEventListener('click', function () {
        editModal.style.display = 'block';
    });

    // Close the modal when the close button is clicked
    closeModalBtn.addEventListener('click', function () {
        editModal.style.display = 'none';
    });

    // Handle the form submission with AJAX
    editForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent normal form submission

        const formData = new FormData(editForm); // Collect form data
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send the data using Fetch API
        fetch(editForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Success! You can close the modal and maybe refresh part of the page.
                editModal.style.display = 'none';
                alert('Recipe updated successfully!');
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Error updating the recipe.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

const deleteBtn = document.getElementById('delete-btn');

deleteBtn.addEventListener('click', function () {
    const confirmDelete = confirm('Are you sure you want to delete this recipe?');
    if (confirmDelete) {
        const deleteUrl = deleteBtn.getAttribute('data-url'); // Get URL from data attribute
        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json', 
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = "/recipes/";
            } else {
                return response.json().then(data => {
                    alert('Error deleting the recipe: ' + (data.error || 'Unknown error.'));
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the recipe.');
        });
    }
});
