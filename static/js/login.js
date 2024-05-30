

function save(){
    name = document.getElementById('name').value;
    email = document.getElementById('email').value;
    password = document.getElementById('password').value;
    console.log(name)
    console.log(email)
    console.log(password)
       var csrftoken = document.cookie.slice(d.indexOf('csrftoken')).split('=')[1]
       if (csrftoken.indexOf(';')) {
           csrftoken = csrftoken.split(';')[0]
       }
    
    fetch('http://127.0.0.1:8000/accounts/login/auth/', {
        method : 'POST',
        headers:{
            'Content-Type' : 'application/json',
            'X-CSRFToken':csrftoken,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": true

        },
        body:JSON.stringify({'name':name,'email':email,'password':password})

    })
    window.Location.href = 'http://127.0.0.1:8000/shop-grid/'

}
