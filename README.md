# bomb
a django web app which can do resource(games) search by keywords and release year and display the results

##Features:
1. On fetch page, be able to fetch different types of resources labeled with specific keyword by using the Giant Bomb API. All fetched data will be saved in local database. The default resource type is set to 'game'.
2. On search page, be able to search resources on local database by different resource type and/or release year. The default resource type is 'game' and the default release year is set to before '1999'.
3. On Result page, all filtered resources will be listed in alphabetical order. The pagination number per page is set to 10 by default.
4. On admin/custom_views page, administrator has access to do fetch task which is same to Fetch page.

##Requirements:
Django 1.95, and Python 3.4

##Quick Start: Test on your local:
```
$ git clone git@github.com:zoe-stockholm/bomb.git
$ pip install --upgrade virtualenv
$ virtualenv bomb
$ source bomb/bin/activate
```
go to your project root (bomb)
```
$ pip install -r requirements.txt (bomb)
$ python manage.py migrate (bomb)
$ python manage.py runserver
```

##Another Option, you can test this app on live server:

Navigator to http://ec2-52-51-156-213.eu-west-1.compute.amazonaws.com:8000/

You can login admin panel http://ec2-52-51-156-213.eu-west-1.compute.amazonaws.com:8000/admin

>username: admin,
>password: passpass
