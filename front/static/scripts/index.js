
const advertContainer = document.getElementsByClassName("advert-container")[0];

document.addEventListener("DOMContentLoaded", getAdvertsData);

function getAdvertsData() {

    fetchApi('GET', 'advert/')
        .then(response => response.json())
        .then(displayAdverts)
        .catch(error => console.error(`Error while retrieving adverts: ${error}`))
}

function displayAdverts(data) {
    for (let advert of data["adverts"]) {displayAdvert(advert)}
}

function displayAdvert(advertData) {

    const advertElement = document.createElement("section");
    advertElement.classList.add("content-block");

    const titleElement = document.createElement("span");
    titleElement.classList.add("title");
    titleElement.textContent = advertData['title'];

    const companyElement = document.createElement("span");
    companyElement.textContent = advertData.company;
    companyElement.textContent = advertData['company'];

    const titleBar = document.createElement("div");
    titleBar.classList.add("title-bar");
    titleBar.appendChild(titleElement);
    titleBar.appendChild(companyElement);
    advertElement.appendChild(titleBar);

    const contentRow = document.createElement("div");
    contentRow.classList.add("content-row");

    const infoElement = document.createElement("div");
    infoElement.classList.add("info", "advert-info");
    infoElement.innerHTML = formatInfos(advertData);
    infoElement.style.display = "none";

    const detailsElement = document.createElement("div");
    detailsElement.classList.add("details");
    detailsElement.innerHTML = formatDetails(advertData['short_desc']);

    const learnMoreButton = document.createElement("button");
    learnMoreButton.textContent = "Learn More";
    learnMoreButton.classList.add("learn-more");

    function onShowMore() {
        detailsElement.innerHTML = formatDetails(advertData['long_desc']);
        infoElement.style.display = "block";

        const applyButton = document.createElement("button");
        applyButton.textContent = "Apply";
        applyButton.classList.add("apply");

        applyButton.addEventListener("click", () => showAdvert(advertData['key']));

        contentRow.replaceChild(applyButton, learnMoreButton);
    }

    learnMoreButton.addEventListener("click", onShowMore)

    contentRow.appendChild(infoElement);
    contentRow.appendChild(detailsElement);
    contentRow.appendChild(learnMoreButton);

    advertElement.appendChild(contentRow);

    advertContainer.appendChild(advertElement);
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

function formatDetails(details) {
    return details.split("\n").map(line => `<p>${line}</p>`).join('')
}

function formatInfos(advertData) {
    return `
    <p>Contract: ${getContractType(advertData['contract'])}</p>
    <p>Salary: ${advertData['salary']}€/year</p>
    <p>Duration: ${advertData['duration']} months</p>
    <p>Skills: ${advertData['competences']}</p>
    `
}

function showAdvert(advertId) {window.location.href = `apply?advert=${advertId}`}