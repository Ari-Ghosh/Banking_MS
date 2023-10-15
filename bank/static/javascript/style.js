$(document).ready(function () {
    // Initialize DataTable
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');
});

// Handle City Dropdown Change on a Particular State
function change_city(element) {
    var state_id = $(element).val();
    $.ajax({
        url: '/ajax/change_state',
        data: { 'state_id': state_id },
        type: 'POST',
        success: function (data) {
            if (data.status) {
                $('#city_id').html(data.data);
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Handle Delete Customer Record via AJAX
function delete_customer(element) {
    var customer_id = $('#customer_delete_id').val();
    performDeleteAction('/ajax/delete_customer', 'customer_id', customer_id);
}

// Handle Delete Account Record via AJAX
function delete_account(element) {
    var account_id = $('#account_delete_id').val();
    performDeleteAction('/ajax/delete_account', 'account_id', account_id);
}

// Common function for performing a delete action
function performDeleteAction(url, key, value) {
    $.ajax({
        url: url,
        data: { [key]: value },
        type: 'POST',
        success: function (data) {
            if (data.status) {
                window.location.href = data.url;
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Validate Cash Transaction Input
function validate_cash_transaction() {
    var operation = $('#cash_action').val();
    var enter_amount = $('#' + operation).val();
    var account_amount = $('#balance').val();
    var error_status = false;
    $('#amount_error').css('display', 'none');
    if (enter_amount === "" || !/^\d+$/.test(enter_amount) || 
        ((operation === 'withdraw_amount' || operation === 'transfer_amount') && 
        (parseInt(enter_amount) <= 0 || parseInt(enter_amount) > parseInt(account_amount)))) {
        error_status = false;
    } else {
        error_status = true;
    }
    $('#amount_error').css('display', error_status ? 'none' : 'inline-block');
    return error_status;
}

// Execute Transaction Operation
function executeOperation(type, amount) {
    var source_account_id = $('#source_account_id').val();
    var transfer_account_id = 0;
    if (parseInt(type) === 3) {
        transfer_account_id = $('#transfer_account_id').val();
    }
    loaderShow();
    $.ajax({
        url: '/ajax/transaction_control',
        data: {
            'source_account_id': source_account_id,
            'transaction_type': type,
            'amount': amount,
            'transfer_account_id': transfer_account_id
        },
        type: 'POST',
        success: function (data) {
            hideLoader();
            if (data.status) {
                window.location.href = data.url;
            }
        },
        error: function (error) {
            hideLoader();
            console.log(error);
        }
    });
}

// Show Loader
function loaderShow() {
    $('.content').css('filter', 'blur(4px)');
    $('#loader').show();
}

// Hide Loader
function hideLoader() {
    $('.content').css('filter', 'blur(0px)');
    $('#loader').hide();
}
