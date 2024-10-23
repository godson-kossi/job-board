
const table = document.getElementById('table')
const apps = document.getElementById('apps')


//fetchApi('GET', 'admin').catch(() => window.location.replace('/'))

fetchApi('GET', `advert`).then(handleAdverts).catch(console.log)

function addCell(row, value) {
    const cell = document.createElement('th')
    cell.textContent = value
    row.appendChild(cell)
}

function insertButton(cell, string, callback) {
    const btn = document.createElement('button')
    btn.textContent = string
    btn.addEventListener('click', callback)
    cell.appendChild(btn)
}

function handleAdverts(response) {response.json().then(displayAdverts)}

function displayAdverts(data) {for (let advert of data['adverts']) addAdvert(advert)}

function addAdvert(advert) {

    const row = document.createElement('tr')

    addCell(row, advert['title'])
    addCell(row, advert['company'])
    addCell(row, advert['short_desc'])

    const actions = document.createElement('th')
    row.appendChild(actions)

    insertButton(actions, '👁️', () => buttonView(advert['key']))
    insertButton(actions, '❌', () => buttonDelete(advert['key']))
    insertButton(actions, '🖋️', () => buttonEdit (advert['key']))
    insertButton(actions, '👤', () => buttonApps(advert['key']))

    table.appendChild(row)
}

function buttonView(advert_id) {window.location.href = `/apply?advert=${advert_id}`}

function buttonDelete(advert_id) {fetchApi('DELETE', `advert/${advert_id}`).catch(console.log)}

function buttonEdit(advert_id) {window.location.href = `/edit?advert=${advert_id}`}

function buttonApps(advert_id) {fetchApi('GET', `advert/${advert_id}/apps`).then(handleApps).catch(console.log)}


function handleApps(response) {response.json().then(displayApps)}

function displayApps(data) {
    apps.innerHTML = ''
    for (let app of data['apps']) addApp(app)
    }

function addApp(app) {

    const row = document.createElement('tr')

    addCell(row, app['firstname'])
    addCell(row, app['lastname'])
    addCell(row, app['email'])
    addCell(row, app['phone_number'])
    addCell(row, app['degree'])
    addCell(row, app['birthdate'])

    apps.appendChild(row)
}