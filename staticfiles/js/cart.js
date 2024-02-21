$(document).ready(function() {
   $('.cart-remove').click(function() {
        // Отримання значення атрибута data-product-id
        var productId = $(this).data('product-id');
        
        // Отримання CSRF-токена з мета-тегу
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        
        // AJAX-запит для відправлення даних на сервер
        $.ajax({
            type: 'POST',           // Тип запиту (POST, GET і т.д.)
            url: '/shop/cart/remove/',  // URL-адреса сервера
            data: {
                'csrfmiddlewaretoken': csrfToken,  // CSRF-токен
                'product_id': productId
            },
            success: function(response) {
                // Обробка успішної відповіді від сервера
               $.ajax({
    type: 'GET',
    url: '/shop/cart/',
    data: {
        'csrfmiddlewaretoken': csrfToken,
    },
    success: function(response) {
        // Обробка успішної відповіді від сервера
        var totalPrice = response.total_price;
        document.getElementById("totalPrice").innerHTML = "Загальна сума: $" + totalPrice;
        $('#cart-item-' + productId).remove();
        console.log('Success:', response);
    },
    error: function(xhr, textStatus, errorThrown) {
        // Обробка помилки під час відправлення запиту
        console.error('Error:', errorThrown);
    }
});
            },
            error: function(xhr, textStatus, errorThrown) {
                // Обробка помилки під час відправлення запиту
                console.error('Error:', errorThrown);
            }
        });
                });
    


    // Обробник події кліку на кнопці або іншому події
    $('.cart').click(function() {
        // Отримання значення атрибута data-product-id
        var productId = $(this).data('product-id');
        
        // Отримання CSRF-токена з мета-тегу
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        
        // AJAX-запит для відправлення даних на сервер
        $.ajax({
            type: 'POST',           // Тип запиту (POST, GET і т.д.)
            url: '/shop/cart/add/',  // URL-адреса сервера
            data: {
                'csrfmiddlewaretoken': csrfToken,  // CSRF-токен
                'product_id': productId,
                'quantity': 1
            },
            success: function(response) {
                // Обробка успішної відповіді від сервера
                console.log('Success:', response);
            },
            error: function(xhr, textStatus, errorThrown) {
                // Обробка помилки під час відправлення запиту
                console.error('Error:', errorThrown);
            }
        });
    });
});
