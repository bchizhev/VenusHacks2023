let serverUrl = 'http://localhost:8000/yourmoodplaylist';


function submit(answer1) {

    const urlParams = new URLSearchParams(window.location.search);
    const authToken = urlParams.get('token');

    console.log('this is the token from the url', authToken)

    fetch(serverUrl, {
      method:'POST',
      body: JSON.stringify({
        mood: answer1,
        authToken: authToken
       
      })
    })
    .then(res => res.json())
    .then(data => {
        // document.getElementById('display').innerHTML = JSON.stringify(data)
        console.log(data)

        for(let i = 0; i < 10; i++){
            document.getElementById('display').innerHTML += `
             <div style = 'border-radius: 10px'>${data.items[i].name}</div>

            `
        }
    });

}

function logout() {
    const url = 'https://accounts.spotify.com/en/logout'                                                                                                                                                                                                                                                                          
    window.location.href = url
}
