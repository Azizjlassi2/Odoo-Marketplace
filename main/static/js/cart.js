function postrequest(id, action) {
    var element = document.getElementsByClassName(id)[0]




    if (action === 'delete') {
        element.parentElement.removeChild(element)
    }
    post(id, action)



}

function update_total() {
    q = document.querySelector('#tbody').children
    total =0
    for (var i = 0; i < q.length; i++) {
        id = this.q[i].id
        total += parseFloat(document.querySelector('#item_' + id + '_total').textContent)
    }
    old_total = document.querySelector('#shopping_total').innerHTML
    document.querySelector('#shopping_total').innerHTML = 'DT' + total


}

function update_logo_cart_quantity(action) {
    if (action === 'add') {
        document.querySelector("#logo-cart-quantity").textContent = parseInt(document.querySelector("#logo-cart-quantity").textContent) + 1
    } else {
        document.querySelector("#logo-cart-quantity").textContent = parseInt(document.querySelector("#logo-cart-quantity").textContent) - 1
    }
}

function update_logo_cart_total() {
    total = parseFloat(document.querySelector('#shopping_total').textContent)
    document.querySelector('#logo-cart-total').textContent = total

}

function post(id, action) {

    // to the add action 
    d= document.cookie;
    var csrftoken = document.cookie.slice(d.indexOf('csrftoken')).split('=')[1]
    if (csrftoken.indexOf(';')) {
        csrftoken = csrftoken.split(';')[0]
    }
    fetch('http://127.0.0.1:8000/shop-grid/update_item/', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'same-origin', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            // 'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true
        },
        // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify({
            'productId': id,
            'action': action
        }) // body data type must match "Content-Type" header
    })
}

function total_item(id) {



    rem = document.querySelector('#pro-qty' + id).children[0]
    rem.addEventListener('click', () => {
        run(id, 'remove')
        update_total();
        update_logo_cart_quantity('remove');
        update_logo_cart_total();
        post(id, 'remove')
    })

    add = document.querySelector('#pro-qty' + id).children[2]
    add.addEventListener('click', () => {
        run(id, 'add');
        update_total();
        update_logo_cart_quantity('add');
        update_logo_cart_total();
        post(id, 'add');
    })

    function run(id, action) {
        // getting the quantity
        quantity = parseFloat(document.querySelector('#pro-qty' + id).children[1].value)
        if (action == 'add') {
            quantity += 1
        } else {
            quantity -= 1
        }

        // getting the price
        price = parseFloat(document.querySelector('#item_' + id + '_price').textContent)

        // updating the price

        total = document.querySelector('#item_' + id + '_total').innerHTML = (quantity * price).toFixed(1)


    }

}
if (document.URL === 'http://127.0.0.1:8000/shop-cart/') {
    // modifier cette fonction pour quelle adapte tous les pages !
    q = document.querySelector('#tbody').children
    for (var i = 0; i < q.length; i++) {
        id = this.q[i].id
        total_item(id)
    }
}

if (document.URL === 'http://127.0.0.1:8000/shop-details/\d+/') {

    function add_to_cart_detail() {
        id = document.URL.slice(-3, -1)
        post(id, 'add')
        console.log('item added !')
    }
}

// 