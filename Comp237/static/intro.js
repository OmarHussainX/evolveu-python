console.log(`--> 'Hello world' from Flask server 'front-end'`)

// setup click event listeners for the buttons
document.getElementById('fetchData').addEventListener('click', fetchData)
document.getElementById('sendData').addEventListener('click', updatePerson)

window.onload = onWindowHasLoaded
function onWindowHasLoaded() {
    console.log(`--> 'intro.html' has finished loading`)
}

async function fetchData() {
    console.log(`--> sending fetch request to server's '/info' route`)

    let response

    try {
        response = await fetch('/info')

        if (response.status != 200)
            throw 'Invalid HTTP Response: ' + response.status

        console.log(`--> Response: ${response}, status: ${response.status}, class of response Object: ${response.constructor.name}`)

        // const data = await response.text()
        // console.log(`--> Data rec'd:\n${data}\ndata type: ${typeof data}, class: ${data.constructor.name}`)

        const data = await response.json()
        console.log(`--> data rec'd from response.json():\n${data}\ndata type: ${typeof data}, class: ${data.constructor.name}, \nkeys: ${Object.keys(data)}, values: ${Object.values(data)}`)

        // converts the JavaScript object (or value) to a JSON string
        const dataString = JSON.stringify(data)
        console.log(`--> data after processing via JSON.stringify():\n[${dataString}]\ndata type: ${typeof dataString}, class: ${dataString.constructor.name}`)

        // display data received from server on the front-end
        document.getElementById('response_data').innerText = dataString

    } catch (error) {
        console.error(`--> *** onWindowHasLoaded error: ${error} ***`)
        console.error(`--> Response: ${response}, status: ${response.status}`)
    }
}

async function updatePerson() {
    console.log(`--> sending post request to server's '/update' route`)
    let firstName = document.getElementById('firstName').value
    let lastName = document.getElementById('lastName').value
    let age = document.getElementById('age').value
    let userId = document.getElementById('userId').value

    console.log(`--> Data to send:
id: ${userId}
name: ${firstName} ${lastName}
age: ${age}`)

    document.getElementById('firstName').value = ''
    document.getElementById('lastName').value = ''
    document.getElementById('age').value = ''
    document.getElementById('userId').value = ''

    let response

    try {
        response = await fetch('/update', {
            method: "post",
            headers: {
                Accept: "application/json, text/plain, */*",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(
                { [userId]: { 'fname': firstName, 'lname': lastName, 'age': age } }
            )
        })
        if (response.status != 200)
            throw 'Invalid HTTP Response:' + response.status
        const res = await response.json()
        console.log('Response from update:', res)

    } catch (error) {
        console.trace()
        console.error(`--> *** updatePerson error: ${error} ***`)
        console.error(`--> Response: ${response}, status: ${response.status}`)
    }

}