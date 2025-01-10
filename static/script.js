window.addEventListener('load', function () {

    document.addEventListener("click", (e) => {
        if (e.target.id === "sign-out") {
            e.preventDefault()
            firebase.auth().signOut();
            location.reload();
        }
        
    })

    // let sessionCookie = getCookie('token')
    // console.log("cookie:", sessionCookie)
    // if (sessionCookie == "") {
    //   firebase.auth().signOut();
    // }
    
    // document.getElementById('sign-out').onclick = function () {
    //   firebase.auth().signOut();
    // };
  
    // FirebaseUI config.
    // var uiConfig = {
    //   signInSuccessUrl: '/',
    //   signInOptions: [
    //     // Comment out any lines corresponding to providers you did not check in
    //     // the Firebase console.
    //     firebase.auth.GoogleAuthProvider.PROVIDER_ID,
    //     firebase.auth.EmailAuthProvider.PROVIDER_ID,
    //     //firebase.auth.FacebookAuthProvider.PROVIDER_ID,
    //     //firebase.auth.TwitterAuthProvider.PROVIDER_ID,
    //     //firebase.auth.GithubAuthProvider.PROVIDER_ID,
    //     //firebase.auth.PhoneAuthProvider.PROVIDER_ID
  
    //   ],
    //   // Terms of service url.
    //   tosUrl: '<your-tos-url>',
    //   signInFlow: "popup",
    // };
  
    firebase.auth().onAuthStateChanged(function (user) {      

      // console.log("onAuthStateChanged")

      if (user) {
        console.log(`Signed in as ${user.displayName} (${user.email})`);
        user.getIdToken().then(function (token) {
          // Add the token to the browser's cookies. The server will then be
          // able to verify the token against the API.
          // SECURITY NOTE: As cookies can easily be modified, only put the
          // token (which is verified server-side) in a cookie; do not add other
          // user information.

          cookieToken = getCookie("token")
          // console.log(`CookieToken: ${cookieToken}`)
          if(cookieToken == "") {
            console.log(`Creating cookie token: ${token}`)
            document.cookie = "token=" + token;
          }

          
        });
      } else {
        // User is signed out.
        // Clear the token cookie.
        console.log("removing cookie")
        document.cookie = "token=";
        
      }
    }, function (error) {
      console.log(error);
      alert('Unable to log in: ' + error)
    });

    const emailLoginForm = document.querySelector('#login-form')
    emailLoginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const signInModal = document.querySelector("#signInModal")
      signInModal.removeAttribute("open")
      const email = document.querySelector('#login-email').value;
      const password = document.querySelector('#login-password').value;

      firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
          console.log('User logged in:', userCredential.user);
          location.reload();
        })
        .catch((error) => {
          console.error('Error during login:', error);
        })
    })

});

async function googleSignIn() {
  const provider = new firebase.auth.GoogleAuthProvider();
  const signInModal = document.querySelector("#signInModal")
  signInModal.removeAttribute("open")
  try {
      const result = await firebase.auth().signInWithPopup(provider);
      // const idToken = await result.user.getIdToken();
      // Send the ID token to your backend
      // const response = await fetch('/verify-token', {
      //     method: 'POST',
      //     headers: { 'Content-Type': 'application/json' },
      //     body: JSON.stringify({ idToken })
      // });
      // if (response.ok) {
      //     window.location.href = '/dashboard';
      // } else {
      //     console.error('Authentication failed');
      // }
      // document.cookie = "token=" + idToken;
      location.reload();

  } catch (error) {
      console.error('Error during Google Sign-In:', error);
  }
}

function getCookie(cname) {

  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}