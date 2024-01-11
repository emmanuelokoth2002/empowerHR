$(document).ready(function() {
    // Initialize DataTable with AJAX
    $('#userstable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getusers",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "userid"},
        {data: "roleid"},
        {data: "username"},
        {data: "passwordhash"},
        {data: "email"},
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
    $('#userstable tbody').on('click', 'button.edit-btn', function () {
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
    $('#employeestable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getemployees",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "employeeid"},
        {data: "firstname"},
        {data: "lastname"},
        {data: "email"},
        {data: "dateofbirth"},
        {data: "phonenumber"},
        {data: "address"},
        {data: "phonenumber"},
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

    $('#departmenttable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getdepartments",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "departmentid"},
        {data: "departmentname"},
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

    $('#roletable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getroles",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "roleid"},
        {data: "rolename"},
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

    $('#suggestionstable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getsuggestions",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "suggestionid"},
        {data: "employeeid"},
        {data: "description"},
        {data: "status"},
        {data: "rolename"},
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

    $('#leaverequesttable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getleaverequest",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "leaverequestid"},
        {data: "employeeid"},
        {data: "leavetype"},
        {data: "startdate"},
        {data: "enddate"},
        {data: "status"},
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

    $('#complaintstable').DataTable({
      "ajax": {
        "url": "http://127.0.0.1:5000/getcomplaints",
        "type": "GET",
        "datatype": "json",
        "dataSrc": function (json) {
          return json || [];
        }
      },
      "columns": [
        {data: "complaintid"},
        {data: "employeeid"},
        {data: "type"},
        {data: "description"},
        {data: "status"},
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

});

  
  