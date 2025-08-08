Setup Instructions
1. Install required Python libraries - Django

Run the following command to install Django and the PostgreSQL adapter:
pip install django psycopg2-binary

2. Set up the PostgreSQL database

The database dump file user_reviews.sql is included in the project folder.

3. Configure Django to use the PostgreSQL database

Open settings.py and update the DATABASES section to connect to your new database:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<db_name>',
        'USER': '<your_db_user>',
        'PASSWORD': '<your_db_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4. Run the Django server
   
python manage.py runserver

5. Screenshots :

   <img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/2f390199-bda9-4ccc-8ba0-2474c0863e31" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/c217a7c8-6b07-4681-abaf-429cf89908cb" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/3a2970f3-296f-4456-be4c-8d89028d8b6f" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/f2d610fd-7f63-4d16-a8cb-37127f666d85" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/bb43e88b-d8bd-488f-942d-ac62a48936a4" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/392349bf-09ad-47e7-aa34-b2a8df0d0c68" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/673fa449-84a6-4bf5-b5ae-3cebcdcfc585" />






