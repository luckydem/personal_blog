window.addEventListener('load', function () {

    document.addEventListener("click", (e) => {
        if (e.target.id === "sign-out") {
          e.preventDefault();
          firebase.auth().signOut();
          location.reload();
        }        
    })    
  
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

    // Add event listeners to each delete button
    const deletePostBtns = document.querySelectorAll(".delete_post");
    deletePostBtns.forEach((delBtn) => {
      delBtn.addEventListener("click", (e) => {
        e.preventDefault();
        id = del.id.split("del_")[1];
        showYesNoModal(text="Are you sure you want to delete this post?", action=`deletePost('${id}')`);
      })
    })

    // Add event listeners to each "view post" button and fetch the posts data
    const viewPostBtn = document.querySelectorAll(".view_post");
    viewPostBtn.forEach((viewBtn) => {
      viewBtn.addEventListener("click", (e) => {
        e.preventDefault();
        id = viewBtn.id.split("view_")[1];
        fetchPost(id);
      })
    })

    // Add event listeners for post edit and cancel
    const editBtn = document.getElementById("editPost");
    if (editBtn !== null) {
      editBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log("edit Clicked");            
        toggleEditPost();
      });
    }
    

    const cancelBtn = document.getElementById("cancelEditPost")
    if (cancelBtn !== null) {
      cancelBtn.addEventListener("click", (e) => {
        e.preventDefault()
        toggleEditPost()
      })
    }
    
});

function validateForm(showAlert = true) {

  const form = document.forms["postForm"];
  const title = form["title"].value;
  const post = form["post"].value;                    

  if ( (title === "" || post === "") && showAlert) {      
    displayToast("Title and Post cannot be blank", "info")
    return false;
  } 
    
  displayToast("form validated", "success")
  return true;

}

function showPost(post) {
  const postViewModal = document.getElementById("postViewModal");
  const form = document.forms["postForm"];
  postViewModal.querySelector(".spinner").classList.add("hidden");  
  form.action = `/post/${post.post_id}`;
  form.classList.remove("hidden");
  // console.log(form.elements);
  document.getElementById("titleHeader").innerHTML = post.title;

  if (form.private) {
    form.private.checked = post.private;
  }
  
  form.title.value = post.title;
  form.post_id.value = post.post_id;
  form.post.value = post.post;

}

function submitForm(event) {
  event.preventDefault()

  if(!validateForm()) {
    return false;
  }

  const postViewModal = document.getElementById("postViewModal");
  postViewModal.querySelector(".spinner").classList.remove("hidden");

  const form = event.target
  form.classList.add("hidden"); 
  const formData = new FormData(form)
  
  toggleEditPost();

  const url = form.action
  const options = {
    method: "POST",
    headers: new Headers({
      "Accept": "application/json"
    }),
    body: formData
  }
  
  fetch(url, options)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    return response.json()
  })
  .then((data) => {
    console.log("Return data from submit:")
    console.log(data)
    
    if (data.edit) {
      toggleEditPost()
    }
    if (data.show_alert){
      validateForm()
    }
    showPost(data.post)
    form.classList.remove("hidden")
  })
  .catch(error => console.error("Error:", error))
  
}

function fetchPost(id) {
  const postViewModal = document.getElementById("postViewModal");
  const form = document.forms["postForm"];
  form.classList.add("hidden");
  postViewModal.querySelector(".spinner").classList.remove("hidden"); 
  postViewModal.showModal();

  const url = `/post/${id}`
  const options = {
    method: "GET",
    headers: new Headers({
      "Content-Type": "application/json",
      "Accept": "application/json"
    })
  }
  fetch(url, options)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      showPost(data.post);
      
    })
    .catch(error => console.error("Error:", error));
}

function toggleEditPost() {            

  const editBtn = document.getElementById("editPost");
  editBtn.classList.toggle("hidden");

  const titleInput = document.getElementById("titleInput");
  titleInput.removeAttribute("disabled");
  titleInput.classList.toggle("hidden");

  const titleHeader = document.getElementById("titleHeader");
  titleHeader.classList.toggle("hidden");

  const privateChk = document.getElementById("privatePost");
  privateChk.toggleAttribute("disabled");

  const post = document.getElementById("post");
  post.toggleAttribute("readonly");
  post.classList.toggle("textarea-bordered");
  if (!post.hasAttribute("readonly")) {
    post.focus();
  }  

  const cancelBtn = document.getElementById("cancelEditPost");
  cancelBtn.classList.toggle("hidden");

  const submitBtn = document.getElementById("submitPost");
  submitBtn.classList.toggle("hidden");
}

function showYesNoModal(text, action) {
  
  const yesNoModal = document.getElementById("yesnoModal");
  const yesNoModalTextEle = document.getElementById("yesnoModalText");
  yesNoModalTextEle.innerHTML = text
  yesNoModalYesBtn = document.getElementById("yesnoModal_yes")
  yesNoModalYesBtn.setAttribute("onClick", action)
  yesNoModal.showModal()

}

function displayToast(toastText, toastType) {
  const toast = document.querySelector(".toast");
  const alert = document.createElement("div");
  alert.classList.add("alert")
  if (toastType == "success") {
    alert.classList.add("alert", "alert-success")
  }
  else if (toastType == "info") {
    alert.classList.add("alert", "alert-info")
  }
  const alertText = document.createElement("span")
  alertText.textContent = toastText;
  alert.append(alertText)

  toast.append(alert)
  setTimeout(() => {
    alert.remove()
  }, 3000)
  
}

function deletePost(id) {
  const postEle = document.getElementById(id);
  if (postEle !== null) {
    postEle.classList.add("hidden"); 
  }  

  url = `/post/${id}/delete`
  console.log(url)
  fetch( url, { 
    method: "DELETE", 
  })
  .then((resp) => {
      if (resp.status == "200") {
        if (postEle !== null) {
          postEle.remove()
        }
        displayToast("Successfully deleted post", "success")

      } else {
        console.log("error deleting post")
        alert.classList.add("alert-info")
        displayToast("error deleting post", "info")
      }
  })
  .catch( e => {
    console.log(e)
  })
}

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