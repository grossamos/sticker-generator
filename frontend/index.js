function generate() {
  let goButton = document.getElementById('go-button');
  goButton.style.display = 'none';

  let dualRing = document.getElementById('lds-dual-ring');
  dualRing.style.display = 'block';

  let input = document.getElementById('generate-input')
  let prompt = input.value;

  let errorText = document.getElementById('error-text');

  let auth = localStorage.getItem('auth');
   
  const headers = new Headers({
    "Authorization": auth,
    "Content-Type": "application/json",
  });

  const request = new Request('/api/image', {
    headers: headers,
    method: 'POST',
    body: JSON.stringify({
      prompt: prompt,
    }),
  });
  
  fetch(request).then(async (response)=> {
    if (response.status == 401 || response.status == 403) {
      window.location.href = '/login.html';
    } else if (response.ok) {
      let output = await response.json()
      localStorage.setItem('auth', auth);
      window.location.href = output.link;
    } else {
      errorText.innerText = 'Invalid prompt, please try again.'
      errorText.style.display = 'block';
      dualRing.style.display = 'none';
      goButton.style.display = 'block';
    }
  }).catch(()=> {
    errorText.innerText = 'Request failed, try again later'
    errorText.style.display = 'block';
    dualRing.style.display = 'none';
    goButton.style.display = 'block';
  })

  return false;
}

function init() {
  let imageContainer= document.getElementById('image-container');
  fetch('/api/image').then(async (response)=> {
    let imagePaths = await response.json()
    for (image of imagePaths.images.reverse()) {
      imageContainer.innerHTML += '<image src="/static/' + image + '" class="sticker"/>'
    }
  });
}

init();
