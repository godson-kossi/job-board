
function fetchApi(method, url, body = null, headers = {}) {

    const options = {
        method: method,
        headers: headers
    };

    if (body) {
        options.headers['Content-Type'] = 'application/json'
        options.body = JSON.stringify(body)
    }


    return fetch('api/' + url, options)
        .then(onFetchResponse)
        .catch(onFetchError);
}

function onFetchResponse(response) {
    if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`)
    return response
}

function onFetchError(error) {
    console.log(error); throw error
}