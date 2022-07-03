window.addEventListener("load", function (evt) {
    $('.vac_status').on('click', 'input[type="radio"]', function () {
        let t_href = event.target;

        $.ajax({
            url: '/vacancies/edit_vacancy_list/' + t_href.value + '/',
            success:
                function (data){
                $('.vac_list').html(data.result)
            },
        });
        evt.preventDefault();
    });
    $('.cv_status').on('click', 'input[type="radio"]', function () {
        let t_href = event.target;

        $.ajax({
            url: '/cvs/edit_cv_list/' + t_href.value + '/',
            success:
                function (data){
                $('.cv_list').html(data.result)
            },
        });
        evt.preventDefault();
    });
     $('.comp_status').on('click', 'input[type="radio"]', function () {
        let t_href = event.target;
        // console.log(t_href.name);
        // console.log(t_href.value);
        $.ajax({
            url: '/users/edit_comp_list/' + t_href.value + '/',
            success:
                function (data){
                $('.comp_list').html(data.result)
            },
        });
        evt.preventDefault();
    });
});