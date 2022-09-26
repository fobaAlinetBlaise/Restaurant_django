$(document).ready(function() {
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