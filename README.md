# TODO
- Ensure that blank posts and titles cannot be submitted
- move data-store into own file with a simple switch to switch between data-store and sql
- login decorator
- sql database version 
- sql authentication


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

#### Nice to have's:


## CS50 Final Project (MVP)

For my final project, I decided to create a personal blog - something I have wanted to setup for a long time. I didn't want to pay for wordpress or any other platform so here was a chance to build this blog with authentication, a simple editor and the ability to set posts to private or public.

The stack that I decided to go with was as follows:

For the backend, I decided to use Flask as it was the framework introduced in the CS50 course and therefore I thought it would be the easiest to implement. 

For the database, I decided to use an SQL database for the same reason as the Flask framework (it was introduced in CS50). 

For the front end, I decided to use Tailwindcss with daisyui instead of Bootstrap as I found it more powerful and the development time was reduced quite a lot.

I decided not to use any frontend framework as the application is simple enough but could still be feature rich.

For the MVP, I wanted it to have the following functionality:

- **Home page** 
    - where my "public" blog posts are listed (with concatinated content) in date order (with newest post first)
    - Each "Title" of each post is clickable and a new page is opened to read the whole blog post (I am going to implement dynamic routing a bit like reddit)
- **Login**
    - (as it's a personal blog, I did not need to create functionality to "register" a user).
- **Authenticated Home Page**
    - listing all my blog posts by date, and or title 
    - include an edit and delete button next to each post as well as a check box to make them private or public
    - Include an "Add New Post" button to create a new post
    - Have a simple editor to edit my post

## Implementation

1. **seting up my local environment**
    - I am using vs-code as my IDE
    - I am using both python (Flask) and nodejs (tailwindcss) in the backend
    - Eventually I would like to deploy my website and therefore I have decided to use the google cloud environment as I am somewhat familiar with it and found [this](https://cloud.google.com/appengine/docs/standard/python3/building-app) helpful tutorial
2. **choosing a WYSIWYG editor**

    I wanted a rich text editor for my blog posts and thought about using an external library for this. I explored [quill.js](https://quilljs.com) and [simplemde](https://simplemde.com):

    **[quill.js](https://quilljs.com)**
    Quilljs was easy to setup but storing the data was more complicated and was taking away from building the blog

    **[simplemde](https://simplemde.com)**
    This is a great "drop-in JavaScript textarea replacement and very easy to include
   
    This ended up having it's own set of issues. I could store the markdown easily but once again I had to figure out a way to render the markdown as html again. I found an article by [Matt Layman](https://www.mattlayman.com/blog/2023/python-markdown-tailwind-best-buds/) which addresses this issue exactly



# Resources

- [CS50](https://cs50.harvard.edu/x/2024/) 
    
    I used all my learnings from the CS50 course to create this website and referred to lectures, shorts, sections and problem sets frequently
    
- [tailwindcss.com](https://tailwindcss.com)

    Tailwindcss' documentation was easy to follow and implement. I thought there might be some trouble using tailwind with Flask but I was pleasantly surprised that it worked seamlessly.

- [flowbite.com](https://flowbite.com/docs/getting-started/flask)

- [daisui.com](https://daisyui.com)