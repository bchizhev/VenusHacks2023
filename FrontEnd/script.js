let serverUrl = 'https://localhost:8000/callback';


function submit() {
    let answer1 = document.getElementById('question1').value;




 
    fetch(serverUrl, {
      mathod:'POST',
      body: JSON.stringify({
        mood: answer1,
        erhrtj: 23,
        authToken: 'dfghdghr345tg'
       
      })
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('display').innerHTML = data.message
        })
