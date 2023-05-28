let serverUrl = 'http://localhost:8000/topTenTracks';


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

        for(let i = 0; i < data.items.length; i++){
            document.getElementById('display').innerHTML += `
             <div style = 'border-radius: 10px'>${data.items[i].name}</div>
             <audio controls src="${data.items[i].preview_url}"></audio>

            `
        }
    });

}

function logout() {
    const url = 'https://accounts.spotify.com/en/logout'                                                                                                                                                                                                                                                                          
    window.location.href = url
}
