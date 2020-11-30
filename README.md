<p align="center">

  <h3 align="center">Website for Lunchtime Yoga for Professionals</h3>

  <p align="center">
    A mobile responsive website to allow users/instructors to create, schedule, and signup for yoga classes in Boise, Idaho.
    <br />
    <a href="https://github.com/Bolmstead/Yoga"><strong>Explore the docs »</strong><a>
    <br>
    <a href="https://yoga-website.herokuapp.com/">View Heroku Demo</a>
  </p>
</p>

![Website_pic](static/images/website.png?raw=true "website")

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project serves as the Capstone 1 project for the Springboard Software Engineering Course. This code will hopefully operate as a website for the Lunchtime Yoga for Business Professionals group in the near future. On this website, a user will be able to do the following:
* View information about the group including pricing, instructor bios, how to contact, and social media links.
* Create and log into an account with an encrypted password using bcrypt.
* Signup for available yoga classes using the website's calendar.
* View enrolled yoga classes and cancel their class enrollment.
* Edit their account information.
* (eventually) Receive automatic emails to confirm their yoga class signup, signup cancellation, or account creation.


Instructors will be able to do all of the above while having the authority to:
* Create/delete a yoga class.
* View who has enrolled for each class.


## Built With

The coding languages, frameworks, source code, and an API that I used to build this project:
* Python
* Javascript
* HTML
* CSS
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Axios](https://www.npmjs.com/package/axios)
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Postgres](https://www.postgresql.org/)
* [SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [Font Awesome](https://fontawesome.com/)
* [Simple Calendar](https://github.com/brospars/simple-calendar)
* [Send Grid Email API](https://sendgrid.com/docs/api-reference/)


<!-- GETTING STARTED -->
## How to Run the Project

To get a local copy up and running follow these steps:

### Clone Repo

1. Clone the repo by clicking on the green "Code" button at the top of the screen or by entering the following in your terminal:
   ```sh
   git clone https://github.com/Bolmstead/Yoga.git
   ```
2. (optional but recommended) Create a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) in the same directory of the cloned unzipped code.

### Library Installations

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.txt.

  ```sh
  pip install -r requirements.txt
  ```

### Postgres Installation

4. Install [Postgres](https://www.postgresql.org/).
5. Create a database named "yoga" in your terminal.
  ```sh
  createdb yoga
  ```

<!-- USAGE EXAMPLES -->
###  Sendgrid API Setup (DO NOT FOLLOW. INCOMPLETE STEP)

6. Create a free account with [SendGrid](https://signup.sendgrid.com/)
7. Follow their instructions to obtain a free API key for the Email API
8. ############# INCOMPLETE! (Get steps from mentor about how to approach this)


<!-- ROADMAP -->
## Roadmap

Possible features that I would like to integrate into the website are:
* Instructor can add any user to a class.
* User having a class credits column that would deplete after they attend a class and can be refilled by an instructor.
* Payment system to allow a user to pay/prepay for classes on the website.
* Google calendar API that would allow a user to save their class signup to their google calendar. Also to allow the instructors to save their created classes to their google calendar.

############# INCOMPLETE! Working to completely set up API. Account is currently under review. Once receive full access to my account again, I will uncomment the appropriate code in my app.py to get it working.

<!-- LICENSE -->
## Notes

The source code for the calendar used on the website was pulled and maniputlated from [Simple Calendar](https://github.com/brospars/simple-calendar). Author of the Simple Calendar grants permission to any person to use, copy, modify, or publish the code. All documents regarding the Simple Calendar code are located in /static/calendar.



<!-- CONTACT -->
## Contact

Berkley Olmstead - olms2074@gmail.com - [Linkedin](https://www.linkedin.com/in/berkleyolmstead/)

Project Link: [https://github.com/Bolmstead/Yoga](https://github.com/Bolmstead/Yoga)
