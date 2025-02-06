# Almuerzo

## Description

Almuerzo is a Django-based web application that helps a group of people decide where to eat lunch. Users can vote for different places, and a custom management command selects the place with the most votes.

## Features

*   User authentication
*   Voting for lunch places
*   Automatic selection of the winning place based on votes
*   Keeps track of how many times each person has voted for the winning place

## Technologies Used

*   Django 1.5.1
*   Python
*   HTML
*   CSS
*   psycopg2 (PostgreSQL adapter)

## Models

*   `Place`: Represents a place where people can eat lunch.
    *   `name`: The name of the place.
    *   `can_order`: Whether you can order from there.
    *   `can_sit`: Whether you can sit there.
    *   `can_takeaway`: Whether you can take to go.
*   `Person`: Represents a person who can vote.
    *   `name`: The name of the person.
    *   `email`: The email of the person.
    *   `times_won`: How many times the person has voted for the winning place.
*   `Vote`: Represents a vote for a place.
    *   `voter`: The person who voted.
    *   `place`: The place that was voted for.
*   `Selection`: Represents the selected place for a given day.
    *   `place`: The selected place.

## Views

*   `home`: Handles user authentication and displays the homepage.
*   `logged`: Displays the voting page or the selected place, depending on the time of day and whether a place has already been selected.
*   `signout`: Signs the user out.
*   `chooseplace`: Registers a vote for a place.

## Management Commands

*   `select_place`: Selects the place with the most votes for the day and creates a `Selection` object.

## Dependencies

*   Django==1.5.1
*   South==0.8.1
*   dj-database-url==0.2.2
*   gunicorn==17.5
*   wsgiref==0.1.2
*   psycopg2==2.4.5
*   dj-static==0.0.5

## Installation

1.  Install the dependencies using `pip install -r requirements.txt`.
2.  Create a PostgreSQL database.
3.  Configure the database settings in `foodapp/settings.py`.
4.  Run `python manage.py syncdb`.
5.  Run `python manage.py migrate`.
6.  Run `python manage.py collectstatic`.
7.  Run `gunicorn foodapp.wsgi`.

## Business Logic

The application works as follows:

1.  Users log in to the application.
2.  If it is before 11:30 AM, users can vote for a place to eat.
3.  Users can only vote once per day.
4.  At 11:30 AM, the `select_place` management command is run.
5.  The `select_place` command selects the place with the most votes.
6.  The `select_place` command updates the `times_won` field for people who voted for the winning place.
7.  If it is after 2:30 PM, the application displays the selected place.

## Usage

1.  Create users in the Django admin interface.
2.  Create places in the Django admin interface.
3.  Users can log in and vote for places to eat.
4.  The `select_place` management command should be run daily to select the winning place.
