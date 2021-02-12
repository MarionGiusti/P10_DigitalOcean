# P10_DigitalOCean _ Deploy appli PurBeurre on a server
* Create a web platform which suggests healthier alternatives to junk food. [OpenClassrooms Project]*
*****************************************************************************************************************
### About The Project:
In the same spirit that the famous 'Ratatouille' restaurant on the Butte Montmartre, 'Pur Beurre' application promotes healthier eating.
The user enters a product and a list of substitutes will be returned with a better NUTRI-SCORE (A-good to E-bad). 

The database of this application based on the Open Food Facts API data, lists several products selected in different
category fields. The available informations of each product like its nutrition-grade, pnns-groups and categories, allow to easily find a healthier substitute in the same category.

#### Built With:
##### Languages and tools used:
- Python 3.8.2 and its framework Django 3.1.4
- HTML5, CSS3, JS
- Responsiv design with Bootstrap
##### API:
- OpenFoodFacts: Import products informations in our database. Documentation here: https://documenter.getpostman.com/view/8470508/SVtN3Wzy.

### Architecture:
	
	config.py
	manage.py
	Procfile
	geckodriver.exe
	requirements.txt
	purbeurre_project/
		.env
		settings.py
		urls.py
		wsgi.py
		asgi.py
	templates/
		404.html
		500.html
		base.html
		home.html
		mentions.html
	static/
		main/
			dist/
			scripts/
			src/
	pages/
		tests/
			test_unit.py
		apps.py
		urls.py
		views.py
	user/
		static/
		templates/
			user/
				account.html
				login.html
				register.html
		tests/
			test_unit.py
		apps.py
		forms.py
		urls.py
		views.py
	catalogue/
		management/
			commands/
				constants.py
				database_import_off.py
		migrations/
		static/
		templates/
			catalogue/
				details_substitute.html
				favorites_substitute.html
				results_substitute.html
		tests/
			dataSet_json_cat_prod_mock.json
			test_database_import_off.py
			test_functionnal.py
		apps.py
		models.py
		urls.py
		views.py

### Getting Started:
##### Prerequisites:
- Python must be installed.
- Virtualenv Module too, otherwise:
	* pip install virtualenv

##### Installation:
###### Local version:
	1- Clone this repository: git clone https://github.com/MarionGiusti/P8_PurBeurreApp

	2- Create a virtualenv in P8_PurBeurreApp: virtualenv -p python3 env

	3- Activate the virtualenv:
		Linux & MacOS user: source pb_env\bin\activate
		Windows user: pb_env\Scripts\activate

	4- Install the required libraries list in the requirements.txt file: pip install -r requirements.txt

	5- Create a PostgreSql database

	6- Create a .env file in the repository purbeurre-project. Write in it your django secret key and database login:
	SECRET_KEY=yourkey
	DATABASE_USER=yourusername
	DATABASE_PWD=yourpassword

	7- Import data from the API OpenFoodFacts:
	python manage.py database_import_off

	8- Run the program on your terminal:
	python manage.py runserver

By default, after running the application will be accessible here: 127.0.0.1:8000/

###### Online version:
The application is deployed on Heroku:
https://healthy-purbeurre.herokuapp.com/
 
