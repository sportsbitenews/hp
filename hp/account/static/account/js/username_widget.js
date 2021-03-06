/**
 * This variable tracks the last change of the username input fields so that
 * return functions from asynchronous functions (-> check username) can detect
 * if the field has been modified since.
 *
 * Without this counter, the return value from the check-user api call might
 * mark the username field as valid/invalid even if the field has been modified
 * since.
 */
var username_counter = 0;

var check_username = function(form_group, timer, counter) {
    var local_counter = counter;
    var input = form_group.find('input#id_username_0');
    var domain_select = form_group.find('select#id_username_1');

    clearTimeout(timer);

    if (input[0].checkValidity()) { // only check if the username is syntactically valid
        timer = setTimeout(function() {
            var exists_url = $('meta[name="account:api-check-user"]').attr('content');

            $.post(exists_url, {
                username: input.val(),
                domain: domain_select.val()
            }).done(function(data) { // user does not exist yet
                if (counter != username_counter) {
                    console.log('no action, because field has been changed again.');
                    return;
                }

                input[0].setCustomValidity("");
                domain_select[0].setCustomValidity("");
            }).fail(function(data) {
                if (counter != username_counter) {
                    console.log('no action, because field has been changed again.');
                    return;
                }

                if (data.status == 409) {  // 409 = HTTP conflict -> The user already exists.
                    error = bs4_forms_set_error(input, 'unique');
                    domain_select[0].setCustomValidity(error.message);
                } else {
                    bs4_forms_set_error(input, 'error');

                    domain_select[0].setCustomValidity(error_msg);
                }
            });
        }, 100);
    }
};

$(document).ready(function() {
    var username_timer;

    $('input#id_username_0').on('input propertychange paste', function(e) {
        var input = $(e.target);
        var form_group = input.parents('.form-group');
        var domain_select = form_group.find('select#id_username_1');
        var check_existance = input.data('check-existance');
        username_counter += 1;

        if (e.target.checkValidity()) {  // only check existance if input is valid
            if (check_existance) {
                check_username(form_group, username_timer, username_counter);
            } else {
                // valid input again, so domain is valid too
                domain_select.each(function(i, elem) {
                    elem.setCustomValidity('');
                })
            }
        } else {
            var msg = form_group.find('.invalid-feedback:visible').text().trim();
            msg = msg ? msg : 'invalid username';  // just to be sure
            domain_select.each(function(i, elem) {
                elem.setCustomValidity(msg);
            })
        }
    });

    $('#id_username_1').change(function(e) {
        var form_group = $(e.target).parents('.form-group');
        var input = form_group.find('input#id_username_0');
        var check_existance = input.data('check-existance');
        username_counter += 1;

        input[0].setCustomValidity('');  // clear any custom error message

        /**
         * If the username is currently invalid because of a unique constraing (-> the username already
         * exists), we clear the constraint because the username might be valid in a different domain.
         */
        if (input[0].checkValidity()) {  // check if the username is currently valid
            if (form_group.hasClass('invalid-unique')) {
                form_group.removeClass('invalid-unique');
                form_group.find('input#id_username_0')[0].setCustomValidity('');
            }
            if (check_existance) {
                check_username(form_group, username_timer, username_counter);
            }
        } else {
            bs4_forms_calculate_error(input);

            var msg = form_group.find('.invalid-feedback:visible').text().trim();
            msg = msg ? msg : 'invalid username';  // just to be sure
            e.target.setCustomValidity(msg);
        }
    });
});
