const companyInput = document.getElementById("item-company");
const submitButton = document.getElementById("submit-company-button"); 


const messageContainer = document.createElement("div");
messageContainer.style.display = "none";
document.body.appendChild(messageContainer);

function fetchCompanyName() {

    fetchApi('GET', 'user')
        .then(response => response.json())
        .then(data => {
            if (data && data.name) {
                companyInput.value = data.name; 
                console.log("Nom de l'entreprise récupéré :", data.name);
            } else {
                console.log("Aucune information d'entreprise trouvée.");
            }
        })
        .catch(error => {
            console.error("Erreur lors de la récupération du nom de l'entreprise :", error);
        });
}

submitButton.addEventListener("click", function(event) {
    event.preventDefault();

    
    const companyName = companyInput.value;

    if (companyName) {
        console.log("Nom de l'entreprise:", companyName);
        messageContainer.textContent = `Nom de l'entreprise: ${companyName}`;
        messageContainer.style.display = "block";
    } else {
        alert("Veuillez entrer le nom de l'entreprise.");
    }
});

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM chargé et prêt.");
    fetchCompanyName(); 
});




document.getElementById('advert-logo-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('advert-logo').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

