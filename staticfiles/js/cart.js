$(document).ready(function() {

    $('.product-count').on('click', '.btn', function() {
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            var input = $(this).siblings('input');
            var value = parseInt(input.val());
            if ($(this).text() == '+') {
                value++;
            } else if (value > 1) {
                value--;
            }
            input.val(value);
            
            var productId = $(this).data('product-id')
            // Отправка POST-запроса через AJAX
            $.ajax({
                type: 'POST',
                url: '/shop/cart/add/',
                data: {
                    'csrfmiddlewaretoken': csrfToken,
                    'product_id': productId,
                    'quantity': value,
                    'update_quantity': true
                },
                success: function(response) {
                    // Обработка успешного ответа
                    totalPrice = response.total_price
                    $('#subtotal-cart').html("Subtotal: $" + totalPrice);
                    
                    console.log('Success:', response);
                },
                error: function(xhr, textStatus, errorThrown) {
                    // Обработка ошибки
                    console.error('Error:', errorThrown);
                }
            });
        });



   $(document).on('click', '.cart-remove, .remove_from_cart_button', function() {
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
        var cartItemsProcessed = false;
        $('.subtotal-cart').html("$" + totalPrice);
        $('#cart-item-' + productId).remove();
        var cartItems = $('.woocommerce-mini-cart-item');
        $(".mini-cart-count").html(cartItems.length)
        if(cartItems.length == 0){
             if (cartItemsProcessed) {
                 return;
             }
            $('.woocommerce-mini-cart').prepend("<h4>Cart is empty</h4>")
            $('.woocommerce-mini-cart__total').hide()
            $('.checkout').hide()
            cartItemsProcessed = true;

        }
        console.log('success:', response);
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
        const toastLive = document.getElementById('liveToast')
 
        // AJAX-запит для відправлення даних на сервер
        $.ajax({
            type: 'POST',           // Тип запиту (POST, GET і т.д.)
            url: '/shop/cart/add/',  // URL-адреса сервера
            data: {
                'csrfmiddlewaretoken': csrfToken,  // CSRF-токен
                'product_id': productId,
                'quantity': 0,
                
            },
            success: function(response) {
                // Обробка успішної відповіді від сервера
                const toast = new bootstrap.Toast(toastLive)

                 toast.show()
                var products = $('.woocommerce-mini-cart.cart_list.product_list_widget.list-wrap');

                product = response.product
                product_detail = response.product.product
if (!$(`#cart-item-${product_detail.id}`).length) {
    // Создаем новый элемент только если его еще нет в корзине
    var newCartItem = `
        <li id="cart-item-${product_detail.id}" class="woocommerce-mini-cart-item d-flex align-items-center">
            <a data-product-id="${product_detail.id}" class="remove remove_from_cart_button">×</a>
            <div class="mini-cart-img">
                <img src="${product_detail.image_url}" alt="Product">
            </div>
            <div class="mini-cart-content">
                <h4 class="product-title"><a href="${product_detail.url}">${product_detail.title}</a></h4>
                <div class="mini-cart-price">${product.quantity} ×
                    <span class="woocommerce-Price-amount amount">$${product.price}</span>
                </div>
            </div>
        </li>
    `;
    console.log(product.price)
    // Добавляем новый элемент в ваш элемент products
    products.append(newCartItem);
   
}
                    $('.woocommerce-mini-cart h4:contains("Cart is empty")').remove();
    $('.woocommerce-mini-cart__total').show()
    $('.checkout').show()
    $.ajax({
        type: 'GET',
        url: '/shop/cart/',
        data: {
             'csrfmiddlewaretoken': csrfToken
        },
        success: function(response) {
            $('.subtotal-cart').html("$" + response.total_price)
            var cartItems = $('.woocommerce-mini-cart-item');
            $(".mini-cart-count").html(cartItems.length)

        }



    });




                
                


            console.log('Success:', response);
            },
            error: function(xhr, textStatus, errorThrown) {
                // Обробка помилки під час відправлення запиту
                console.error('Error:', errorThrown);
            }
        });
    });
});
