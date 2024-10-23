
const applyForm = document.getElementsByClassName("apf")[0];

const firstNameInput = document.getElementById("firstname");
const lastNameInput = document.getElementById("lastname");
const emailInput = document.getElementById("email");
const phoneInput = document.getElementById("phone_number");
const degreeInput = document.getElementById("degree");
const birthdayInput = document.getElementById("birthdate");

const urlParams = new URLSearchParams(window.location.search);
const advertId = urlParams.get('advert');

document.addEventListener("DOMContentLoaded", getAdvertData)

document.getElementById("disconnect-button").addEventListener("click", onDisconnect)
document.getElementById("back-button").addEventListener("click", window.history.back)
document.getElementById("submit-button").addEventListener("click", onSubmit)

initMessageContainer()

function initMessageContainer() {

    const messageContainer = document.createElement("div");
    messageContainer.className = 'success-message';
    messageContainer.style.display = 'none';
    messageContainer.textContent = "Successfully applied !";

    applyForm.appendChild(messageContainer);
    applyForm.parentNode.insertBefore(messageContainer, applyForm.nextSibling);
}

function getAdvertData() {

    if (advertId) {
        fetchApi('GET', `advert/${advertId}`)
            .then(response => response.json())
            .then(data => {displayAdvertData(data); getUserData()})
            .catch(error => console.error(`Error while fetching advert: ${error}`))
    }
}

function displayAdvertData(advert) {

    const itemTitle = document.getElementById("item-title");
    const itemCompany = document.getElementById("item-entreprise");
    const infoText = document.getElementById("info-text");
    const lineItems = document.querySelectorAll(".line-item");

    itemTitle.textContent = advert['title'];
    itemCompany.textContent = advert['company'];
    infoText.innerHTML =
        `
        <p>Contract: ${getContractType(advert['contract'])}</p>
        <p>Salary: ${advert['salary']}€/an</p>
        <p>Duration: ${advert['duration']} mois</p>
        <p>Competences: ${advert['competences']}</p>
        `

    const lines = advert['long_desc'].split("\n");

    lineItems.forEach((line, index) => {
        if (lines[index]) {line.textContent = lines[index]}
        else {line.textContent = ''}
    })
}

function getContractType(contractCode) {
    switch (contractCode) {
        case 'FX': return "Fixed-Term Contract";
        case 'PX': return "Permanent Contract";
        case 'AS': return "Apprenticeship";
        case 'TJ': return "Temp Job";
        case 'IS': return "Internship";
        default: return "Unknown";
    }
}

function getUserData() {

    fetchApi('GET', `user`)
        .then(response => response.json())
        .then(displayUserData)
        .catch(error => console.error(`Error while retrieving user data: ${error}`))
}

function displayUserData(data) {

    if (data) {

        firstNameInput.value = data.firstname || "";
        lastNameInput.value = data.lastname || "";
        emailInput.value = data.email || "";
        phoneInput.value = data.phone_number || "";
        degreeInput.value = data.degree || "";
        birthdayInput.value = data.birthdate || "";
    }
}

function onSubmit(event) {

    event.preventDefault();

    fetchApi('POST', `advert/${advertId}/apply`, getApplicationData())
        .then(onSubmitSuccess)
        .catch(onSubmitError)
}

function onSubmitSuccess() {
    applyForm.style.display = "none";
    messageContainer.style.display = "block";
}

function onSubmitError(error) {
    console.error("Could not send application :",error.message || error);
    alert(`Error : ${error.message || error}`);
}

function getApplicationData() {

    return {
        firstname: firstNameInput.value,
        lastname: lastNameInput.value,
        email: emailInput.value,
        phone_number: phoneInput.value,
        degree: degreeInput.value,
        birthdate: birthdayInput.value,
    }
}

function onDisconnect() {}