

# ParkEasy

Welcome to the **ParkEasy** repository! Follow the steps below to set up and run this project on your local machine.



# Features

[Authentication, Authorization, Pagination, Input Validation]


---
# Prerequisites

1. **Python**: Ensure that you have Python3.8+ installed on your system. You can download it from [python.org](https://www.python.org).

2. **Virtual Environment**: Isolate your project in a virtual environment where no mismatch of versions and libraries from your local machine occurs.
3. **MySQL**: Ensure you have a MySQL server installed on your system for the database.



## Installation Steps

### 1. Clone the repository
```bash
    git clone git@github.com:codegeek004/ParkEasy.git
    cd ParkEasy
```

### 2. Setup the virtual environment
```bash
    python -m venv venv
    source venv/bin/activate    # On macOS/Linux
    venv\Scripts\activate       # On Windows
```

### 3. Install the requirements
Install all the python packages from requirements.txt
```bash
    pip install -r requirements.txt
```

### 4. Configure the database
1. To configure the database in the ParkEasy directory.
2. Go to the MySql server and create database named parking.
```bash
    mysql -u <your_username> -p


```
3. Update your username and password in the db.py file.
```python
    import mysql.connector
    db_config1 = {
        'host' : 'localhost',
        'user' : 'root', #replace this with your username
        'password' : 'root', #replace this with your password
        'database' : 'parking'
        }
    db = mysql.connector.connect(**db_config1)
    cursor = db.cursor(buffered=True)
```

### 5. Populate the database
Populate your database by running the scripts inside the faker folder. 
###### You need to necessarily populate the database to enable functionalities in the application.
```python
    python faker/generate_bookingslots.py
    python faker/generate_payments.py
    python faker/generate_slots.py
    python faker/generate_users.py
```


### 6. Run the server
```bash
    python app.py
```
Access the project at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes and create a pull request. If you want to make any changes to the project. Please make all those changes in the dev branch


---

## License
[License](LICENSE)

---
