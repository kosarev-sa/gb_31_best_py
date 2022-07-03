let $custom_form_modal = $('.cd-user-modal');
    //$form_relation = $custom_form_modal.find('#cd-relation'),
    //$emp_rel_btn = $('#version4 [id^="employer_relation_btn"]'),
    //$work_rel_btn = $('#version4 [id^="worker_relation_btn"]');

/**
 * Open modal.
 */
function openModalForm(val) {

    // set magic
    $("#magic_field").val(val);

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
    }
});