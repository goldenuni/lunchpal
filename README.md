# _**_Lunch Service**__ 🌟🐾

Welcome to the Lunchpal API Service: a comprehensive system for managing lunch decisions for employees.

The Lunchpal API Service is a Django-based project designed to help employees choose lunch options by allowing restaurants to upload menus daily and enabling employees to vote on their preferred meals. This system provides a user-friendly platform for restaurant managers, employees, and superusers to manage and participate in lunch selections efficiently.

## Key Features 🗝️

- **Authentication:** Users are authenticated using JWTs, ensuring secure access upon successful login.
- **Admin Panel:** Admins can effortlessly add, edit, and delete restaurant and menu data, maintaining control over the application.
- **Restaurant Management:** Restaurant managers can create, update, and manage their restaurant's menu.
- **Menu Uploading:** Restaurants can upload daily menus for employees to vote on.
- **Voting System:** Employees and superusers can vote for their favorite menu items for the day.
- **Results Tracking:** Users can retrieve the current day's menu and results based on votes.

## Installation 🌟

### Using GitHub

1. Ensure you have Python 3 installed. Install PostgreSQL and create a database.

2. Clone the repository:

   ```bash
   git clone https://github.com/goldenuni/lunchpal.git
   cd lunchpal
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

### Run with Docker

Ensure Docker is installed and running on your machine.

1. **Build the Docker images:**

   Open a terminal and navigate to the root directory of the project, then run the following commands:

   ```bash
   docker-compose build
   ```
2. **Start the Docker**:

After building the images, run the following command to start the application and the PostgreSQL database:
```bash
   docker-compose up
   ```
3. **Access the API**:

Once the containers are up and running, you can access the Lunchpal API Service at http://localhost:8000.

## Note

Ensure you have the .env file configured properly with the necessary environment variables for your database connection and any other settings.

## Database Dump

A database dump is provided for easier setup. The dump file can be found in the root directory as `db_dump.json`. 

### Loading the Database Dump

You can load this dump into your PostgreSQL database using the following command:

```bash
python manage.py loaddata db_dump.json
```
## Getting Access
Here are the default credentials for the application:

### SuperUser:
``````
Email: superuser@dot.com
Password: superpass12345
``````
### Restaurant Manager:
````
Email: restaurant_man@dot.com
Password: superpass12345
````
### Employee:
````
Email: employee@dot.com
Password: superpass12345
````
After completing these steps, you should have access to the Lunchpal API Service. Enjoy exploring the features!