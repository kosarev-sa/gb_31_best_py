let $custom_form_modal = $('.cd-user-modal');
let $error_message = $("#error_message");
// $custom_form_modal.removeClass('is-visible');
let $last_list_section = $('#detail_last_list_section')
let $relation_detail_section = $('#relation_detail_section')
dropErrorMessage();

/**
 * Open modal.
 */
function openModalForm(relation_id) {

    // set magic
    $("#magic_field").val(relation_id);

    //show modal layer
    $custom_form_modal.addClass('is-visible');
}

/**
 * Send to create relation.
 */
function sendData(way_id) {
    dropErrorMessage();
    let csrf_token = $('meta[name="csrf-token"]').attr('content');
    let magic_field = $("#magic_field").val();
    let select_picker = $("#relation_select_picker").val();
    let letter = $("#transmittal_letter").val();

    let rel_row_str = '#rel_row_' + magic_field;
    let rel_row = $(rel_row_str);


    if (!checkValues(select_picker, letter)) {
        return;
    }

    if (magic_field && select_picker && letter) {

        let part_url;

        if (way_id === 0) {
            part_url = '/relations/create_from_rel/';
        } else {
            part_url = '/relations/create_from_detail/';
        }

        $.ajaxSetup({
            headers: {
                "X-CSRFToken": csrf_token
            }
        });

        $.ajax({
            type: 'POST',
            url: part_url + magic_field + '/' + select_picker + '/' + letter + '/',
            data: {},
            success: (data) => {
                if (data) {
                    if (data.result) {
                        if (way_id === 0) {
                            rel_row.replaceWith(data.result)
                        } else {
                            $relation_detail_section.replaceWith(data.result);
                        }
                    }
                    // Hide modal form.
                    $custom_form_modal.removeClass('is-visible');
                    // Clear modal form.
                    $("#magic_field").val('');
                    $('#relation_select_picker').val(0);
                    $("#relation_select_picker").selectpicker('refresh')
                    $("#transmittal_letter").val('');
                }
            },
            error: function (data) {
                createErrorMessage('Ошибка 500!');
            }
        });
    }
}

/**
 * Checking enter user fields.
 * @param select_picker
 * @param letter
 * @returns {boolean}
 */
function checkValues(select_picker, letter) {

    if (select_picker === '0') {
        createErrorMessage('Ошибка. Выберите значение из выпадающего списка!')
        return false;
    }

    if (!letter) {
        createErrorMessage('Ошибка. Заполните сопроводительный текст!');
        return false;
    }

    return true;
}

/**
 * Create error message.
 * @param text
 */
function createErrorMessage(text) {
    $error_message.addClass('alert');
    $error_message.addClass('alert-danger');
    $error_message.text(text);
}

/**
 * Drop error message.
 */
function dropErrorMessage() {
    $error_message.removeClass('alert');
    $error_message.removeClass('alert-danger');
    $error_message.text('');
}

/**
 * Close modal.
 */
$custom_form_modal.on('click', function (event) {
    if ($(event.target).is($custom_form_modal) || $(event.target).is('.cd-close-form')) {
        $custom_form_modal.removeClass('is-visible');
        $('#relation_select_picker').val(0);
        $("#relation_select_picker").selectpicker('refresh')
        $("#transmittal_letter").val('');
        dropErrorMessage();
    }
});

/**
 * Close modal when clicking the esc keyboard button.
 */
$(document).on('keyup', function (event) {
    if (event.which == '27') {
        $custom_form_modal.removeClass('is-visible');
        $('#relation_select_picker').val(0);
        $("#relation_select_picker").selectpicker('refresh')
        $("#transmittal_letter").val('');
        dropErrorMessage();
    }
});