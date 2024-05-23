function signUp() {
    var userName = document.getElementById("user-name").value;
    var userEmail = document.getElementById("user-email").value;
    var userPassword = document.getElementById("user-password").value;
    if(userName.trim() === "") return;
    if(userEmail.trim() === "") return;
    if(userPassword.trim() === "") return;

    fetch('/sign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify([
            { name: userName },
            { email: userEmail },
            { password: userPassword }
        ])
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
}