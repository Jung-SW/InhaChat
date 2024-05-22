function logIn() {
    var userEmail = document.getElementById("user-email").value;
    var userPassword = document.getElementById("user-password").value;
    if(userEmail.trim() === "") return;
    if(userPassword.trim() === "") return;

    fetch('/check_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify([
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

// 엔터 키 누를 때 전송되도록 설정
document.getElementById("user-password").addEventListener("keypress", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        logIn();
    }
});