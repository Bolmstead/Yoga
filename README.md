<br />
<p align="center">

  <h3 align="center">Website for Lunchtime Yoga for Professionals</h3>

  <p align="center">
    A website to allow users/instructors to create, schedule, and signup for local yoga classes in Boise, Idaho.
    <br />
    <a href="https://github.com/Bolmstead/Yoga"><strong>Explore the docs »</strong><a>
    <br>
    <a href="https://yoga-website.herokuapp.com/">View Heroku Demo</a>
  </p>
</p>



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

These documents serve as the Capstone 1 project for the Springboard Software Engineering Course. This code will hopefully operate as a website for the Lunchtime Yoga for Business Professionals group in the near future. On this website, a user will be able to do the following:
* View information about the group including pricing, instructor bios, how to contact, and social media links.
* Create and log into an account with an encrypted password using bcrypt.
* Signup for available yoga classes using the website's calendar.
* View enrolled yoga classes and cancel their class enrollment.
* Edit their account information.
* (eventually) Receive automatic emails to confirm their yoga class signup, signup cancellation, or account creation.


Instructors will be able to do all of the above and have the authority to do the following:
* Create/delete a yoga class.
* View who has enrolled for each class.


### Built With

The following are coding languages, frameworks, source code, and an API that I used to build this project:
* Python
* Javascript
* HTML
* CSS
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Axios](https://www.npmjs.com/package/axios)
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [Jinja](https://www.postgresql.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Postgres](https://www.postgresql.org/)
* [SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [Font Awesome](https://fontawesome.com/)
* [Simple Calendar](https://github.com/brospars/simple-calendar)
* [Send Grid / Twilio](https://sendgrid.com/docs/api-reference/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps:
1. (optional but recommended) Create a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
2. Install [Postgres](https://www.postgresql.org/).
3. Create a database named "yoga"
* npm
  ```sh
  createdb yoga
  ```

### Library Installations

Use the package manager <a href="https://pip.pypa.io/en/stable/">pip</a> to install the requirements.txt.
* npm
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```JS
   const API_KEY = 'ENTER YOUR API';
   ```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

The source code for the calendar used on the website was pulled from https://github.com/brospars/simple-calendar and manipulated. All documents regarding the Simple Calendar code are located in /static/calendar. Author of the Simple Calendar grants permission to any person to use, copy, modify, or publish the code.



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
