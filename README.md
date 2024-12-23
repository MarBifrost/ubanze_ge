# Project Ubanze
 

UBANZE is a Django-based project designed to connect users with service providers in their local area, neighborhood, or even around the corner. This platform allows individuals to showcase their services, including what they can do, what they sell, and what they offer, creating a community-driven hub for local service exchange. The project focuses specifically on services within UBANs—the Georgian word for "Area"—emphasizing hyper-local connections and accessibility.

## Table of Contents
1. [Features](#features)
2. [Installation and setup](#Installation and setup)
3. [Project Structure](#Project Structure)
4. [API Endpoints](#API Endpoints)

## Features
### 1. User Registration and Authentication
    Register users as customers or service providers
    During the registration process, you have the option to select the 'Service
    Provider' checkbox. Upon completing your registration, you will be automatically
    redirected to your profile editing page. Here, you can provide detailed information
    about yourself and save your updates. Once saved, you will be taken to your profile
    page, where you can view your details and use the 'Edit' button to make any future
    changes.
    Additionally, the application supports Basic Authentication for secure access to the
    API endpoints in the Django REST Framework.
    
### 2. Email Notifications
    After Registration Welcome emails are sent to the new users, using Celery for
    handling background tasks like email sending.
    Redis is configured as the message broker. 

### 3. Database Management
    a. User Creation with CustomUser, with form validation and authentication. 
    b. Profile Management: two types of profiles - Service Provider and Customer. 
    c. Service Category management, using MPTT for hierarchical categorization. 
    d. Store Service details, including name, type, description and etc. 
    e. Location management, having City and Area models, using foreign key relations. 


## Installation

#### 1. Check if you have pipenv installed globally and if your Python version is above 3:
        pip install pipenv

####    2. Clone the Repository:
        git clone https://github.com/MarBifrost/ubanze_ge.git
        cd ubanze_ge

####    3. Set Up the Virtual Environment   
        pipenv install

####    4. activate the VIrtual Environment
        pipenv shell
    
####    5. Run Database migrations
        python manage.py makemigrations
        python manage.py migrate

####    6. Start the Development Server
        python manage.py runserver


### requirements (content of Pipfile):
         [[source]]
        url = "https://pypi.org/simple"
        verify_ssl = true
        name = "pypi"

        [packages]
        django-allauth = "*"
        django-mptt = "*"
        pillow = "*"
        redis = "*"
        celery = "*"
        django-celery-results = "*"
        django-celery-email = "*"
        djangorestframework = "*"

        [requires]
        python_version = "3.11"

# Project Structure
    Project structure is defined in another file named the same way




# API Endpoints
## Credentials for APIs:
    "username": "admin",
    "password": "admin123"

1. Providers Listing:

    GET api/providers/

2. Customer Listing:
    
    GET api/customers/

3. Category Listing:

    GET api/categories/

4. Add the Category:

    POST /api/categories/





## Debugging
- Debug Toolbar


## License
This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).



## Author
- **Mariam Gaprindashvili** [GitHub](https://github.com/MarBifrost)

---

Thank you for your interest in this project! 
If you have any suggestions or ideas, feel free to submit an issue or a pull request. 
Happy coding! 😊



