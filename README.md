# Django-htmx-celery Todo Appw

The simple Todo app to track progress of daily tasks.

Done as part of a technical challenge of Mykyta Mishchenko interview process 
for PlatformE.

## Features

- Sign up as a new user profile
- Login into the app with user credentials
- Login / Signup forms error handling 
- Create and prioritize a new task
- List tasks and filter them by priority
- Notification control for the 'HIGH' priority tasks
- Edit and view the created tasks
- Mark tasks as completed
- Remove tasks from the user's tasks list 

## Requirements
```
Docker
Docker-compose
```

## Run

1. Clone the repository:

    ```bash
    git clone https://github.com/CHESTERFIELD/django-app-name.git
    ```

2. Run application with docker-compose:

    ```bash
    docker-compose up
    ```

3. Copy and paste the following link in browser to start using the todo app:

   ```browser
   http://localhost:8000/
   ```

4. To create test data for 'userone' and 'usertwo' with default password 'password': 

    ```bash
    docker exec -it django-web-server python manage.py add_test_data
    ```
   NOTE: test data script creates some of todo tasks with upcoming notification period. 
Please check celery-worker container logs to ensure that scheduled tasks works as expected. 


5. To create a superuser: 

    ```bash
    docker exec -it django-web-server python manage.py createsuperuser
    ```

## Additional

This application shall not be considered as a production ready, because 
requires much more detailed configuration from the developer such as disabling 
of django debug mode, setup of reliable and performant http server like 
gunicorn, hiding of exposing ports that are being opened for developing, 
proper keeping of services logs, etc.

The application is launched in docker-compose so does not require any major 
actions from the user to start working with it.

The .env file contains set of extra env variables that are being used by 
services for their configuration, and can be adjusted according to the user 
needs.

The application has got celery-beat service to watch out for scheduled tasks.
Those tasks just only mimic a work of sending of emails by logging the message 
to the output for visibility.


## Build

The build directory contains scripts, Dockerfiles, etc., for building 
application.

## Tests

TBD, not done yet.

## Known issues

1. Application doesn't save history while working in browser.
2. Pagination for user's tasks is not implemented.
