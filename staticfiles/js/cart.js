$(document).ready(function() {

    function ajax_request(type, url, data = {}, success) {
    
        data['csrfmiddlewaretoken'] =  $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: type,
            url: url,
            data: data,
            success: success,
            error: function(xhr, textStatus, errorThrown) {
                console.error('Error:', errorThrown);
            }
        });
    }

    function addProductInCart(product, product_detail) {
        var products = $('.woocommerce-mini-cart.cart_list.product_list_widget.list-wrap');
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
    
        products.append(newCartItem);

        $('.woocommerce-mini-cart h4:contains("Cart is empty")').remove();
        $('.woocommerce-mini-cart__total').show()
        $('.checkout').show()

        ajax_request(
            'GET',
            '/shop/cart/',
            {},
            function(response) {
                var cartItems = $('.woocommerce-mini-cart-item');
                $('.subtotal-cart').html("$" + response.total_price)
                $(".mini-cart-count").html(cartItems.length)
            }
        )
    }


    $('.product-count').on('click', '.btn', function() {
       
        var input = $(this).siblings('input');
        var value = parseInt(input.val());

        if ($(this).text() == '+') {
            value++;
        } else if (value > 1) {
            value--;
        }
        input.val(value);
        
        var productId = $(this).data('product-id')
       
        ajax_request(
            'POST',
            '/shop/cart/add/',
            {
                'product_id': productId,
                'quantity': value,
                'update_quantity': true
            },
            function(response){
                
                totalPrice = response.total_price
                $('#subtotal-cart').html("Subtotal: $" + totalPrice);
                
            }
            
        )
    });



   $(document).on('click', '.cart-remove, .remove_from_cart_button', function() {
       
        var productId = $(this).data('product-id');
        
        ajax_request(
            'POST',
            '/shop/cart/remove/',
            {
                'product_id': productId
            },
            function(response) {
                ajax_request(
                    'GET',
                    '/shop/cart/',
                    {},
                    function(response)
                    {
                        var totalPrice = response.total_price;
                        var cartItemsProcessed = false;
                        var cartItems = $('.woocommerce-mini-cart-item');
                        var products = $('.list-group-item');
                        
                        if (products.length == 1) {
                            // Reload the page
                            location.reload();
                            return;
                        }

                        $('.subtotal-cart').html("$" + totalPrice);
                        $('#cart-item-' + productId).remove();
                        $(".mini-cart-count").html(cartItems.length)

                        

                        if(cartItems.length == 1) {
                            if (cartItemsProcessed) {
                                return;
                            }

                            $('.woocommerce-mini-cart').prepend("<h4>Cart is empty</h4>")
                            $(".mini-cart-count").html(0)
                            $('.woocommerce-mini-cart__total').hide()
                            $('.checkout').hide()
                            

                            cartItemsProcessed = true;
               
                        }
                       
                        console.log('success:', response);

                    }

                )
            }

        )
    })
        
    

    $('.cart-btn').click(function() {
        var productId = $(this).data('product-id');
        var countProduct = $('.quickview-cart-plus-minus input').val();
       
        const toastLive = $("#liveToast");

        ajax_request(
            'POST',
            '/shop/cart/add/',
            {
                'product_id': productId,
                'quantity': countProduct, 
            },
            function(response) {
                const toast = new bootstrap.Toast(toastLive);
                toast.show();

                
                product = response.product
                product_detail = response.product.product

                
                
                $('#cart-item-1 .mini-cart-price').html(product.quantity + " × " + `<span class="woocommerce-Price-amount amount">$${product.price}</span>`)

                if (!$(`#cart-item-${product_detail.id}`).length) {
                    
                    if (!$(`#cart-item-${product_detail.id}`).length) {
                        addProductInCart(product, product_detail);
                        return;
                    }

                }
                ajax_request(
                    'GET',
                    '/shop/cart/',
                    {},
                    function(response) {
                        var cartItems = $('.woocommerce-mini-cart-item');
                        $('.subtotal-cart').html("$" + response.total_price)
                        $(".mini-cart-count").html(cartItems.length)

                       
                    }
                )
               
            }
        )
    })
    
    

    $('.cart').click(function() {
        var productId = $(this).data('product-id');
        
        const toastLive = $('#liveToast');

        ajax_request(
            'POST',
            '/shop/cart/add/',
            {
                'product_id': productId,
                'quantity': 0,
            },
            function(response) {
                const toast = new bootstrap.Toast(toastLive)
                toast.show()

                product = response.product
                product_detail = response.product.product
                

                if (!$(`#cart-item-${product_detail.id}`).length) {
                    addProductInCart(product, product_detail);
                   
                }

            }

        )
    });
});
