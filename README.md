[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8b4b2bf11a0c47aab33278e207254932)](https://app.codacy.com/app/MarloneA/Bright_Events?utm_source=github.com&utm_medium=referral&utm_content=MarloneA/Bright_Events&utm_campaign=badger)
[![Build Status](https://travis-ci.org/MarloneA/Bright_Events.svg?branch=master)](https://travis-ci.org/MarloneA/Bright_Events)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)

# Bright_Events

 Bright Events is a platform where event organizers can create and manage different types of events.
 The platform also allows Users to to create accounts so that they can view, reserve edit and delete events
 they intend to attend


# Framework used

Built with

  - Flask

# Installation

Clone the repository locally:

`$ git clone [URL]`

Create a virtual environment and activate it:
 ```
 $ cd Bright_Events
 $ virtualenv env
 $ source env/bin/activate
 ```

Install the application dependencies:

`$ pip install -r requirements.txt`

Export Flask variables:

 ```
 $ export FLASK_CONFIG=development`
 $ export FLASK_APP=run.py
 ```

Run the application:

`$ flask run`


# API reference

The api documentation is hosted as the homepage
of the application. Reference material for the API can be found at [API](https://brightevents.docs.apiary.io)

## Live Application
The Live API is hosted [here](https://andela-brightevents.herokuapp.com/) on [heroku](https://heroku.com)

# Contribute

To contribute to the project, create a Pull Request on a feature branch from develop. 

# License

MIT © 2017 Marlone Akidiva
