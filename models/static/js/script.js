$(document).ready(function() {
    // Initialize DataTable with AJAX
    $('#contactsTable').DataTable({
      "ajax": {
        "url": "http://localhost/contact/Controllers/contactoperation.php?getcontacts=true",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "contactid"},
        {data: "firstname"},
        {data: "lastname"},
        {data: "phonenumber"},
        {data: "email"},
        {data: "location"},
        {
            "data": null,
            "render": function (data, type, row) {
              return '<button class="btn btn-info btn-sm edit-btn">Edit</button>';
            }
        },
        {
            "data": null,
            "render": function (data, type, row) {
              return '<button class="btn btn-danger btn-sm delete-btn">Delete</button>';
            }
        }
      ]
    });

    

    // Handle edit button click event
    $('#contactsTable tbody').on('click', 'button.edit-btn', function () {
        var rowData = table.row($(this).parents('tr')).data();
    
        // Populate the modal with the contact details for editing
        $('#editFirstName').val(rowData.firstname);
        $('#editLastName').val(rowData.lastname);
        $('#editPhoneNumber').val(rowData.phonenumber);
        $('#editEmail').val(rowData.email);
        $('#editLocation').val(rowData.location);
    
        // Handle save changes button click
        $('#saveChangesBtn').off('click').on('click', function () {
        // Retrieve the edited values from the modal
        var editedFirstName = $('#editFirstName').val();
        var editedLastName = $('#editLastName').val();
        var editedPhoneNumber = $('#editPhoneNumber').val();
        var editedEmail = $('#editEmail').val();
        var editedLocation = $('#editLocation').val();
    
        // Perform validation or additional logic if needed
    
        // Prepare data for the update request
        var updateData = {
            contactid: rowData.contactid,
            firstname: editedFirstName,
            lastname: editedLastName,
            phonenumber: editedPhoneNumber,
            email: editedEmail,
            location: editedLocation
        };
    
        // Send an AJAX request to update the contact details
        $.ajax({
            url: 'your_update_endpoint.php', // Replace with your server-side endpoint
            type: 'POST', // or 'PUT', depending on your server-side implementation
            dataType: 'json',
            data: updateData,
            success: function (response) {
            // Handle the success response, if needed
            console.log('Contact updated successfully:', response);
    
            // Close the modal
            $('#editContactModal').modal('hide');
    
            // Refresh the DataTable to reflect the changes
            table.ajax.reload();
            },
            error: function (error) {
            // Handle the error, if needed
            console.error('Error updating contact:', error);
            }
        });
        });
    });

    // Handle delete button click event
    $('#contactsTable tbody').on('click', 'button.delete-btn', function () {
        var data = table.row($(this).parents('tr')).data();
    
        // Show a confirmation modal or dialog
        if (confirm('Are you sure you want to delete this contact?')) {
        // User confirmed deletion
    
        // Send an AJAX request to delete the contact
        $.ajax({
            url: 'your_delete_endpoint.php', // Replace with your server-side endpoint
            type: 'POST', // or 'DELETE', depending on your server-side implementation
            dataType: 'json',
            data: { contactid: data.contactid }, // Send the contact ID for deletion
            success: function (response) {
            // Handle the success response, if needed
            console.log('Contact deleted successfully:', response);
    
            // Refresh the DataTable to reflect the changes
            table.ajax.reload();
            },
            error: function (error) {
            // Handle the error, if needed
            console.error('Error deleting contact:', error);
            }
        });
        } else {
        // User canceled deletion
        console.log('Deletion canceled for contact with ID: ' + data.contactid);
        }
    });    
});

  
  