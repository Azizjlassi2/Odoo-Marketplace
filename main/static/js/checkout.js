if (document.URL === 'http://127.0.0.1:8000/checkout/' || document.URL === 'http://127.0.0.1:8000/checkout/#') {



    // creating order 
    function save() {

        // creating user 
        var first_name = document.getElementById('First Name').value
        var last_name = document.getElementById('Last Name').value
        var country = document.getElementById('Country').value
        var address = document.getElementById('Address_1').value
        var city = document.getElementById('City').value
        var state = document.getElementById('State').value
        var postcode = document.getElementById('Postcode').value
        var phone = document.getElementById('Phone').value
        var email = document.getElementById('Email').value

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'country': country,
            'address_1': address,
            'city': city,
            'state': state,
            'postcode': postcode,
            'phone': phone,
            'email': email,
                }
       


        // complete the fetch and test it ...
        post('http://127.0.0.1:8000/checkout/create_order/', data)

        console.log('data sent !')


    }

    function post(url, data) {
        d = document.cookie
        var csrftoken = document.cookie.slice(d.indexOf('csrftoken')).split('=')[1]
        if (csrftoken.indexOf(';')) {
            csrftoken = csrftoken.split(';')[0]
        }
        console.log('csrftoken :', csrftoken)
        fetch(url, {
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
            body: JSON.stringify(data) // body data type must match "Content-Type" header
        })


    }


}
