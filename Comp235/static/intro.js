console.log(`--> 'Hello world' from Flask server`)


window.onload = onWindowHasLoaded
async function onWindowHasLoaded() {
    console.log(`--> 'intro.html' has finished loading`)
 
    let response
 
    try {
        response = await fetch('http://localhost:5000/info')

        if (response.status != 200)
            throw 'Invalid HTTP Response: ' + response.status

        console.log(`--> Response: ${response}, status: ${response.status}`)

        const data = await response.text()
        console.log(`--> Data: ${data}`)
 
    } catch (error) {
        console.error(`--> *** onWindowHasLoaded error: ${error} ***`)
        console.error(`--> Response: ${response}, status: ${response.status}`)
    }
}
