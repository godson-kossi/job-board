const firstNameInput = document.getElementById("first-name");
const lastNameInput = document.getElementById("last-name");
const emailInput = document.getElementById("email");
const phoneInput = document.getElementById("phone");
const degreeInput = document.getElementById("degree");
const birthdayInput = document.getElementById("birthday");
const passwordInput = document.getElementById("password");
const nameInput = document.getElementById("name");
const addressInput = document.getElementById("adress");

const registerForm = document.getElementById("register-form");
const submitButton = document.getElementById("register-button");
const applicantButton = document.getElementById("applicant-button");
const companyButton = document.getElementById("company-button");

const messageContainer = document.createElement("div");
messageContainer.style.display = "none";
registerForm.parentNode.insertBefore(messageContainer, registerForm.nextSibling);

var type = null

document.addEventListener("DOMContentLoaded", function() {
    registerForm.style.display = "none"; 
});


applicantButton.addEventListener("click", function(event) {
    event.preventDefault();
    registerForm.style.display = "block"; 

    hideAllFields();

    
    const applicantFields = document.querySelectorAll('.applicant-fields');
    applicantFields.forEach(field => {
        field.style.display = 'block';
        type = 0
    });
});


companyButton.addEventListener("click", function(event) {
    event.preventDefault();
    registerForm.style.display = "block"; 

    
    hideAllFields();

    
    const companyFields = document.querySelectorAll('.company-fields');
    companyFields.forEach(field => {
        field.style.display = 'block';
        type = 1
    });
});


function hideAllFields() {
    const allFields = document.querySelectorAll('.applicant-fields, .company-fields');
    allFields.forEach(field => {
        field.style.display = 'none';
    });
}

submitButton.addEventListener("click", function(event) {
    event.preventDefault();

    if (type === 0) {
        var registrationData = {
            type: 0,
            firstname: firstNameInput.value,
            lastname: lastNameInput.value,
            email: emailInput.value,
            degree: degreeInput.value,
            birthdate: birthdayInput.value,
            phone_number: phoneInput,
            password: passwordInput.value,
        };
    }
    else {
        var registrationData = {
            type: 1,
            name: nameInput.value,
            email: emailInput.value,
            phone_number: phoneInput,
            password: passwordInput.value,
            address: addressInput,
        };
    }

    const endpoint = `user/register`;

    fetchApi('POST', endpoint, registrationData)
        .then(response => {
            registerForm.style.display = "none";
            messageContainer.textContent = "Inscription réussie ! Vous pouvez maintenant vous connecter.";
            messageContainer.style.display = "block";
        })
        .catch(error => {
            console.error("Erreur lors de l'inscription :", error.message || error);
            alert(`Erreur : ${error.message || error}`);
        });
});

document.addEventListener("DOMContentLoaded", function() {
    
});