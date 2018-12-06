Name: Corey
Online Demo: http://ccps530flashieprod.herokuapp.com/
Project Title: Flashie
Course:  CCPS530
Instructor: Ghassem Tofighi

# Flashie

Flashie is a tool designed to help provide gameplay insights to League of Legends players. Users can add themselves as well as other players to the tool to better understand their performance. 

See the demo below:

[![Flashie demo](https://img.youtube.com/vi/gjyM-OJ844k/0.jpg)](https://www.youtube.com/watch?v=gjyM-OJ844k)




## Featured Technologies

[Flask](http://flask.pocoo.org/): A Python microframework that utilizes Werkzeug and Jinja 2. 

[FlaskWTF](http://flask.pocoo.org/docs/1.0/patterns/wtforms/): An integration of WTForms for Flask.

[Riot API](https://developer.riotgames.com/): League of Legends API.

[SQLAlchemy](https://www.sqlalchemy.org/): Python SQL toolkit/ORM.

[Chart.js](https://www.chartjs.org/): HTML5 based JavaScript charts.

[jQuery File Upload Plugin](https://github.com/blueimp/jQuery-File-Upload): File upload widget

[jQuery.Flipster](https://github.com/drien/jquery-flipster): CSS3 3D transform 'cover flow'.



## Steps

### Initial Setup

#### 1. Clone the repo

Clone the `ccps530-flashie` repo locally. In a terminal, run:

```
$ git clone https://github.com/cjj272/ccps530-flashie.git
$ cd ccps530-flashie
```



#### 2. Get a Riot API key

You will need to get your own API key from Riot. [Instructions here.](https://developer.riotgames.com/api-keys.html)

#### 3. Set up a virtual environment and install requirements

Next, you will need to create a virtual environment. In a terminal, run:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

If successful, you will now be logged into a virtual environment. 

From there, you can install the requirements:

```
(venv) $ pip install -r requirements.txt
```



#### 4. Create databases

Then, you will need to create the databases that Flashie will use. In order to do so, log into the root directory of the project and perform the following:

```
(venv) $ flask shell
>>> from app import db
>>> db.create_all()
```



#### 5. Run server

If all went well, you should be able to run the server!

```
(venv) $ flask run
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```



## Flashie usage

Now that the server is running, you can begin using the tool!

#### 0. Setup API Key

Using the API Key you've acquired. Please it into the form and click 'submit.'
*Do not share your API key with anyone*

![s8](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s8.PNG)

#### 1. Add/remove a user

Our first step will be to add League of Legends accounts to the tool. You can do so through the "Add User" page:

![s1](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s1.PNG)

Simply add a user and click submit. This will submit an API call to the Riot servers to make sure that the account exists. 

To remove a user, use the bottom form.

#### 2. Get match data 

Next, you will need to get match data for the player you just added. To do so, navigate to the "Match data" page:

![s2](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s2.PNG)

Hit submit for the summoner name you have selected. Another API call will be sent to Riot to get recent match data. 

**NOTE:** Make sure you're grabbing match data for an user who has played recently!

#### 3. Get game data

*After* you have grabbed match data for a player, you can now navigate to the "Game data" page in order to get player specific info for the relevant matches. 

![s3](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s3.png)

Again, simply select the summoner name you are interested in and click submit. 

**WARNING: Make sure to check the API request limits for your Riot API Key! Each submission will make up to 20 requests per player!**

#### 4. (Optional) Upload avatars

If you'd like, you can also upload images to be displayed for each user. After navigating to the "Upload avatars" section, simply drag and drop images and click upload!

![s4](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s4.png)

#### 5. (Optional) Set avatars

If you'd like, you can set avatar images to be displayed for each user. After navigating to the "Choose avatar" section, simply drag and drop images and click upload!![s5](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s5.png)

#### 6. See performance charts

And finally, the payoff for all this setup. Choose the summoner **who has successfully loaded game data** and click submit.

![s6](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s6.png)

![s7](https://github.com/cjj272/ccps530-flashie/blob/master/gitimages/s7.png)
