function login() {
  let username = document.getElementById('username').value
  let password = document.getElementById('password').value
  let errorText = document.getElementById('error-text');

  let auth = "Basic " + btoa(username + ':' + password);
  console.log(auth);

  const headers = new Headers({
    "Authorization": auth
  });

  const request = new Request('/api/auth', {
    headers: headers,
  });
  
  fetch(request).then((response)=> {
    if (response.ok) {
      localStorage.setItem('auth', auth);
      window.location.href = '/';
    } else {
      errorText.innerText = 'Invalid username/password'
      errorText.style.display = 'block';
    }
  }).catch(()=> {
    errorText.innerText = 'Request failed, try again later'
    errorText.style.display = 'block';
  })
  return false;
}
