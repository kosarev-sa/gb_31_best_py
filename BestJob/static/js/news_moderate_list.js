let $custom_form_modal = $('.cd-user-modal');
let $error_message = $("#error_message");

/**
 * Delete news.
 */
function newsDelete() {
    dropErrorMessage();
    let csrf_token = $('meta[name="csrf-token"]').attr('content');
    let news_id = $("#magic_field").val();

    if (news_id) {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": csrf_token
            }
        });

        $.ajax({
            type: 'POST',
            url: '/news/delete/' + news_id + '/',
            data: {},
            success: (data) => {
                // Not very good solution... but..
                document.location.reload();
            },
            error: (data) => {
                createErrorMessage('Ошибка 500!');
            }
        });
    }
}

/**
 * Cancel.
 */
function cancelDelete() {
    $custom_form_modal.removeClass('is-visible');
}

/**
 * Open modal.
 */
function openModalForm(news_id) {

    // set magic
    $("#magic_field").val(news_id);

    //show modal layer
    $custom_form_modal.addClass('is-visible');
}

/**
 * Close modal.
 */
$custom_form_modal.on('click', function (event) {
    if ($(event.target).is($custom_form_modal) || $(event.target).is('.cd-close-form')) {
        $custom_form_modal.removeClass('is-visible');
    }
});

/**
 * Close modal when clicking the esc keyboard button.
 */
$(document).on('keyup', function (event) {
    if (event.which == '27') {
        $custom_form_modal.removeClass('is-visible');
        dropErrorMessage();
    }
});

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