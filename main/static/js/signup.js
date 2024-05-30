
function verification_mdp(pass,checkpass){
    if(pass!==checkpass){
        // afficher un message au dessous de champs mot de pass
        console.log('pass !== checkpass ')
    }

}

function log()
{   console.log('retreiving data ......!')
    clientname = document.getElementById('Name').value
    country = document.getElementById('Country').value
    address_1 = document.getElementById('Address_1').value
    city = document.getElementById('City').value
    state = document.getElementById('State').value
    postcode = document.getElementById('Postcode').value
    phone = document.getElementById('Phone').value
    email = document.getElementById('Email').value
    check_password = document.getElementById('Check-Password').value
    password = document.getElementById('Password').value
    data = {
        'name':clientname,
        'country': country,
        'address': address_1,
        'city': city,
        'state': state,
        'code_postal': postcode,
        'telephone': phone,
        'email': email,
        'password': password}
    console.log('data :',data)

    var csrftoken = document.cookie.slice(d.indexOf('csrftoken')).split('=')[1]
    if (csrftoken.indexOf(';')) {
           csrftoken = csrftoken.split(';')[0]
       }
       console.log(csrftoken)
    url = 'http://127.0.0.1:8000/accounts/signup/create-account/'
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
        }).then(console.log('data sent!'))



}