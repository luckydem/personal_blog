# TODO
- [X] Ensure that blank posts and titles cannot be submitted (client & server)
- [X] move datastore functions to googleDatastore.py
- [X] implement firebase authentication
  - [ ] bundle using a javascript bundler? Not sure if I'll do this
- [ ] login decorator (not sure if I need to implement it this way but I will try - it works differently with firebase but I like the idea of setting up a decorator)
  - [X] only show the "POST" link if logged in
  - [X] only allow to navigate to /post if logged in
  - [X] only show edit and delete buttons if logged in
- [X] Remove firebaseui css as this is causing issues with the app (modals in wrong place etc) and implement the buttons myself
  - [X] Sign in with Google
  - [X] Sign in with Email
    - [ ] ChatGPT suggested a server side (python) check of the token. Not sure if this is necessary but I will look into this
- [X] ensure that only users that are registered in the datastore database can be authenticated and not "any" google account
- [ ] Create script to empty datastore
- [X] Create a script to populate database
- [ ] sql
  - [ ] implement an sql database version
    - [ ] store posts 
    - [ ] store user details
  - [ ] use sql and python library (session) for authentication
    - [ ] store hashed password
  - [ ] Add a boolean to switch between data-store and sql
- [ ] Truncate long blog posts and add the ability for a user to click on the post to view the entire post
- [ ] Add ability to upload pictures for a post
- [X] Toggle Public / Private Posts
- [ ] Add Tagging feature
- [ ] Add token and session storage on server side and not on client side
  - [ ] implement flasks session and store token in flasks session instead of a cookie on the client.
  - [ ] wrap every call with a session verification function
  - [ ] add more security using google secret manager and .env files (python-dotenv)
- [X] Implement Edit and Delete Post for logged in users

# DEV NOTES

### gcloud CLI commands

* Check config: 

  ```bash
  $ gcloud config list
  [compute]
  region = us-central1
  zone = us-central1-c
  [core]
  account = demianhauptle@gmail.com
  disable_usage_reporting = True
  project = duhworks

  Your active configuration is: [default]

* Check gcloud configurations:

  ```bash
  $ gcloud config configurations list
  ```

* Activate configuration for duhworks: 
  ```bash
  $ gcloud config configurations activate {project-name}
  ```

* Activate ADC (Application Default Credentials): 
  ```bash
  $ gcloud auth application-default set-quota-project {project-name}
  ```

* Check active project: 
  ```bash
  gcloud config get-value project
  ```

# MY PERSONAL BLOG
#### Video Demo: [youtube-link]()
#### Description
A personal blog with the following features:

- **tagging** - The ability to add random tags to my posts and filter posts based on my tags
- **multiple databases** - There are two branches of this blog:
    - `sql` - As the name suggests, this is branch holds the code specific to using an sql database
    - `master` - this branch uses googles firestore (my preferred database for this project as I found it easier to hook up and deploy to a live "mostly free" environment)
- **authentication** 
    - For `master` I have used firebase
    - For `sql` I used 
- **SEO**

#### Roadmap:
- Display number of words in blog as I'm typing 


## CS50 Final Project (MVP)

For my final project, I decided to create a personal blog - something I have wanted to setup for a long time. I didn't want to pay for wordpress or any other platform so here was a chance to build this blog with authentication, a simple editor and the ability to set posts to private or public.

The stack that I decided to go with was as follows:

For the backend, I decided to use Flask as it was the framework introduced in the CS50 course and therefore I thought it would be the easiest to implement. 

For the database, I decided to use an SQL database for the same reason as the Flask framework (it was introduced in CS50). 

For the front end, I decided to use Tailwindcss with daisyui instead of Bootstrap as I found it more powerful and the development time was reduced quite a lot.

I decided not to use any frontend framework as the application is simple enough but could still be feature rich.

For the MVP, I wanted it to have the following functionality:

- **Home page: "/"** 
    - where my "public" blog posts are listed (with concatinated content) in date order (with newest post first)
    - Each "Title" of each post is clickable and a new page is opened to read the whole blog post (I am going to implement dynamic routing a bit like reddit)
- **Blog Post Submission page: "/post"**
    - Where I can write my post and submit it if I'm happy with it
    - includes form validation
- **Login: "/login"**
    - (as it's a personal blog, I did not need to create functionality to "register" a user).
- **Authenticated Home Page: "/"**
    - listing all my blog posts by date, and or title 
    - include an edit and delete button next to each post as well as a check box to make them private or public
    - Include an "Add New Post" button to create a new post
    - Have a simple editor to edit my post

## Implementation

1. **seting up my local environment**
    - I am using vs-code as my IDE
    - I am using both python (Flask) in the backend 
    - I am using nodejs to manage / compile tailwindcss and daisui
    - I am using vanilla JavaScript in the frontend (no framework)

2. **Database implementation**

    I wanted to try out a different database as everything I read seemed quite complicated to get SQL setup when moving to production (hosting it somewhere etc).   
    I followed the tutorial from [cloud.google.com](https://cloud.google.com/appengine/docs/standard/python3/building-app) and found that setting up hosting and the datastore provided by google to be pretty straight forward.  
    Fortunately this was a quick fix and I just needed to specify that I needed to exclude the text from being indexed: `excludeFormIndexes: true`

    I decided to move the datastore functions into their own python file to make my code cleaner. To do this, was easy enough as it's very simple to import other python files

    After clearing out all my test posts, I ran into an error where the datastore complained that I could not "order" the posts in ascending or descending if there was not index applied. This confused me to start off with and then I realised that there is an automatic index created when the database is not empty. Therefore I had to implement a check to see if the database was not empty. 
    To do this, with the help of google and chatGPT, I queried the database with a limit of 1 and only queried the keys to optimise the query. if the query returned more than zero entities, I would then get all entities otherwise I would return empty. This way the ordering of an empty query does not happen.

3. **choosing a WYSIWYG editor for post submission**

    I wanted a rich text editor for my blog posts and thought about using an external library for this. I explored [quill.js](https://quilljs.com) and [simplemde](https://simplemde.com):

    * **[quill.js](https://quilljs.com)**

      Quilljs was easy to setup but storing the data was more complicated and was taking away from building the blog

    * **[simplemde](https://simplemde.com)**
      
      This is a great "drop-in JavaScript textarea replacement and very easy to include    
      This ended up having it's own set of issues. I could store the markdown easily but once again I had to figure out a way to render the markdown as html again. I found an article by [Matt Layman](https://www.mattlayman.com/blog/2023/python-markdown-tailwind-best-buds/) which addresses this issue exactly

      >*NOTE: For now I decided to continue without form validation - I have kept a branch with this option if I wanted to fall back to it*

      - [ ] While I was messing with simplemde, I noticed that it kept track of the number of words I had written and I thought that was a nice feature so I'm going to implement that if time allows it

4. **Form Validation**

      I quickly realised that I would need to implement some sort of form validation. so I googled around and found a simple example on [w3schools.com](https://www.w3schools.com/js/js_validation.asp) and implemented something similar

      >*NOTE: For now I wrote the JavaScript in the HTML page but I recognised the opportunity to re-use this code elsewhere and will put it into a file if needed*
      ?

      The validation checks to see if the post and title exist (well if they are not blank).      
      * If either of them are blank, JavaScript pops up a modal stating that the Post and Title cannot be blank.    
      * If a user tries to manipulate the JavaScript, there is also server side logic that checks if the post or title is blank.
      * If the user submits with a title but no post, the server will return the page with the title and an alert will be displayed
      * If the user submits with a post but no title, the server will return the page with the post and an alert will be displayed  
      * I ran into an issue: When ever I opened the the post page, the alert box would appear every time. To fix this error I passed a `showAlert` variable from the server back to the clients JavaScript - This allowed me to specify when the alert should be shown making my validation work properly was unable to be bypassed

5. **Authentication**   
      I spent a bit of time with the same [google](https://cloud.google.com/appengine/docs/standard/python3/building-app) tutorial trying to get the authentication correct but I found that there were some recommendations in using npm modules etc for production and I didn't really want to start implementing that at this point - I felt it was detracting from getting the mvp working (I know I can implement it later if necessary when I want to add more features).  
      
      I also searched the web for a python module that I could use for firebase authentication using google as well as email and password.
      The only library that I found was called pyrebase and it is like 9 years old and only limited to email and password authentication so I decided to use the firebase-auth-ui javascript library which worked well initially but then I realised that the styling was messing with tailwindcss and daisyui styling so I decided to implement it without the firebase-ui library.
      I achieved this all on the client side with JavaScript but I'm still not 100% sure if it is production safe.
      
      The next step is to only allow "registered" users to post. Currently I can just login with any google account which is not good. There are a few ways that I can think of to implement this. 

      For starters, I'm going to just add a new data "kind" in the google datastore with one "user" entry and if the user_id matches the one in the database, allow the user to be authenticated. 
      
      That means that I have to add a check for this in the `onAuthStateChanged` function - I haven't done this yet but I added some authentication checks in the python functions so even if a user is "logged in" according to firebase auth, the user will still not see "restricted" pages and data.

      I've realised that using python / Flask with firebase plus using googles datastore seems a bit backwards. The intigration doesn't seem as fluid as I thought. I have learnt a lot though and I think my code is relatively secure

      Okay so I'm going to have to change my approach and store the idToken on the server as part of flasks session - that way it cannot be hampered with and there is not "cookie" that can be messed with. Let me see if I can implement that.

# Resources

- [CS50](https://cs50.harvard.edu/x/2024/) 
    
    I used all my learnings from the CS50 course to create this website and referred to lectures, shorts, sections and problem sets frequently
    
- [tailwindcss.com](https://tailwindcss.com)

    Tailwindcss' documentation was easy to follow and implement. I thought there might be some trouble using tailwind with Flask but I was pleasantly surprised that it worked seamlessly.

- [flowbite.com](https://flowbite.com/docs/getting-started/flask)

- [daisui.com](https://daisyui.com)

- 