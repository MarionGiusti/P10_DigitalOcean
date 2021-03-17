# P10_DigitalOcean 
*Deploy the Django app PurBeurre on a server [OpenClassrooms Project]*
*****************************************************************************************************************
# P11_DigitalOcean
*Improve an existing project [OpenClassrooms Project]*
A new functionnality has been added to this project, a user profile
with a picture and the possibility to update it as well as some others user informations.
*****************************************************************************************************************
### About The Project:
See the repository P8_PurBeurreApp for more information about the app.

#### Built With:
##### Languages and tools used:
- Python 3.8.2 and its framework Django 3.1.4
- Django 3.1.4
- PostgreSQL
- Responsiv design with Bootstrap
##### API:
- OpenFoodFacts: Import products informations in our database. [Documentation here](https://documenter.getpostman.com/view/8470508/SVtN3Wzy)
##### Monitoring:
- Travis-CI : continue integration, run app tests before a pull request
- Crontab : update database each week
- Sentry : dashboard to follow the logs
- NewRelic : dashboard to monitor the server activity

#### Deployment
The app has been deployed on Digital Ocean. Choose an Ubuntu droplet.
[Follow this tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04)
###### Online version:
[link here!](http://134.122.106.30/) :beetle:
 
