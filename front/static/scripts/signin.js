

const loginForm = document.getElementById("login-form");

const messageContainer = document.createElement("div");

messageContainer.style.display = "none";
loginForm.parentNode.insertBefore(messageContainer, loginForm.nextSibling);


document.getElementById("login-button").addEventListener("click", onSubmit)

function onSubmit(event) {

    event.preventDefault();

    fetchApi('POST', `user/authenticate`, getRegistrationData())
        .then(onSubmitResponse)
        .catch(onSubmitError)
}

function getRegistrationData() {

    return {
        email:  document.getElementById("email").value,
        password: document.getElementById("password").value
    }
}

function onSubmitResponse() {
    loginForm.style.display = "none";
    messageContainer.textContent = "Successfully connected !";
    messageContainer.style.display = "block";
}

function onSubmitError(error) {
    console.error(`Connection error: ${error.message || error}`);
    alert(`Error : ${error.message || error}`);
}


// RAIN

function randomText() {
    var text = "abc,defgh;,ijk/l/mn;op'qrst'uvw'xy,z.ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
    let letters = text[Math.floor(Math.random() * text.length)];
    return letters;
}

function rain() {
    const rainContainer = document.querySelector('.main-content'); 
    let e = document.createElement('div');
    e.classList.add('drop');
    rainContainer.appendChild(e);

    let i = Math.floor(Math.random() * rainContainer.clientWidth); // Largeur du conteneur
    let size = Math.random() * 1.5;

    e.innerText = randomText();
    e.style.left = i + 'px';
    e.style.fontSize = 0.5 + size + 'em';
    e.style.animationDuration = 4 + size + 's';

    setTimeout(function() {
        e.remove();
    }, 3000);
}

setInterval(function() {
    rain();
}, 100); 
