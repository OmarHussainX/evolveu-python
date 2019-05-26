console.log(`--> 'Hello world' from Flask server 'front-end'`)


window.onload = onWindowHasLoaded
async function onWindowHasLoaded() {
    console.log(`--> 'intro.html' has finished loading`)
 
    let response
 
    try {
        response = await fetch('/info')

        if (response.status != 200)
            throw 'Invalid HTTP Response: ' + response.status

        console.log(`--> Response: ${response}, status: ${response.status}, class of response Object: ${response.constructor.name}`)

        // const data = await response.text()
        // console.log(`--> Data rec'd:\n${data}\ndata type: ${typeof data}`)
 
        const data = await response.json()
        console.log(`--> data rec'd from response.json():\n${data}\ndata type: ${typeof data}`)

        const dataString = JSON.stringify(data)
        console.log(`--> data after processing via JSON.stringify():\n[${dataString}]\ndata type: ${typeof dataString}, class: ${dataString.constructor.name}`)

        // display data recieved from server on the front-end
        document.getElementById('response_data').innerText = dataString

    } catch (error) {
        console.error(`--> *** onWindowHasLoaded error: ${error} ***`)
        console.error(`--> Response: ${response}, status: ${response.status}`)
    }
}
