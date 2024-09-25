document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-btn'); // Button that triggers the modal
    const editModalElement = document.getElementById('edit-modal'); // Modal element
    const editForm = document.getElementById('edit-recipe-form'); // Form inside the modal

    // Initialize the Bootstrap 5 Modal
    const editModal = new bootstrap.Modal(editModalElement);

    // Show the edit modal when the edit button is clicked
    editBtn.addEventListener('click', function () {
        editModal.show(); // Use Bootstrap's modal show method
    });

    // Close the modal (Bootstrap automatically handles this with data-bs-dismiss="modal" on the cancel button)

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
                editModal.hide(); // Hide the modal using Bootstrap's hide method
                alert('Recipe updated successfully!');
                location.reload(); // Optionally reload the page to reflect changes
            } else {
                alert('Error updating the recipe.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// delete button
const deleteBtn = document.getElementById('delete-btn');

deleteBtn.addEventListener('click', function () {
    const confirmDelete = confirm('Are you sure you want to delete this recipe?');
    if (confirmDelete) {
        const deleteUrl = deleteBtn.getAttribute('data-url');
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
