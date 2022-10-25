$(document).ready(function() {
    $('.increment-btn').click(function(e) {
        console.log('=========1=========');
        e.preventDefault();
        var inc_value = $(this).closest('.menu_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        console.log(value);
        value = isNaN(value) ? 0 : value;
        if (value < 10) {
            value++;
            $(this).closest('.menu_data').find('.qty-input').val(value);
        }
    })
    $('.decrement-btn').click(function(e) {
        e.preventDefault();
        console.log('=========2=========');
        var dec_value = $(this).closest('.menu_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.menu_data').find('.qty-input').val(value);
        }
    })
    $('.addToCartBtn').click(function(e) {
        e.preventDefault();

        var menus_id = $(this).closest('.menu_data').find('.menu_id').val();
        var menu_qtite = $(this).closest('.menu_data').find('.qtite-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        console.log("==============");
        console.log(menus_id);
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'menus_id': menus_id,
                'menu_qtite': menu_qtite,
                'csrfmiddlewaretoken': token
            },

            success: function(response) {
                console.log(response)
                alertify.success(response.status)
            }
        })
    })
});