
document.addEventListener("DOMContentLoaded", checkUserAuthentication);


function checkUserAuthentication() {
    fetchApi('GET', 'user')
        .then(data => toggleButtons(true, data['type'] !== 0))
        .catch(() => toggleButtons(false, false))
}


function toggleButtons(authenticated, manager) {

    document.getElementsByClassName('auth-buttons')[0].style.display = authenticated ? 'none': 'block';
    document.getElementById('disconnect-button').style.display = authenticated ? 'block': 'none';
    document.getElementById('manage-button').style.display = manager ? 'block': 'none';

}

document.getElementById('disconnect-button').addEventListener('click',
    () => {
        fetchApi('DELETE', 'user/')
        toggleButtons(false, false)
    })