Hello, and welcome to our project!
We have built Mr. Brønshøj - a betting website for football games
in the spanish La Liga. customers can register an account, and state
how much they want to deposit - The only time they can deposit - Because why would you 
need to deposit more than once? And if you ever even end up at 0, does that not make you a bad player? 
We dont associate with losers here at Mr. Brønshøj. 

Customers can see which games are created by the betmakers, what the odds are, and then bet accordingly.
They can see their balance go up and down depending on how they play.

Admin can create games and set odds. Admin can also validate results for finished football matches, and
money will be deposited to accounts or not depending on bets.

We hope you like the project.


1 . ##############################################################################################################################################

Firstly, we need to create a virtual environment

use a terminal, and head to the directory where your project is.

for a reference, our terminal looked like this with folder named <flask_project> using Visual Studio Code (ON MAC BTW):

bertanturan@BTs-MacBook-Pro flask_project % 


########################################

Then you want to install virtualenv
you can type in the terminal the following:

COMMAND: pip install virtualenv

########################################

Then we can create the virtual environment.
with virtual environment with name "env", command looks like this:

FOR MAC:
COMMAND: virtualenv env 

########################################

You should now see a folder called <environmentname> pop up in current directory
We now need to activate the environment
To activate environment, please type following:

FOR MAC (ENVIRONMENT NAME = "env"):
COMMAND: source env/bin/activate

########################################
You should now see <environmentname> pop up to the left of your terminal line.
This means it is activated.

########################################

We now need to install dependencies.
Please put requirements.txt file into current directory
When requirements.txt file is in directory, then type following command to download
all useful libraries:

COMMAND: pip install -r requirements.txt

########################################

Now environment is set up!

2 . ##########################################################################################################

We need to some things first before you
are able to run the project.

First, we need to build the database

We do this the following way.

Assuming every file is put into the directory now:

go into python interactive mode (MAKE SURE VENV IS ACTIVATED):

COMMAND: python3

Now we need to type the following:

COMMAND: 
from app import app, db
with app.app_context():
    db.create_all()

IF THIS DOES NOT WORK, TRY: 

COMMAND: 
from app import app, db
db.create_all()

########################################
To exit python interactive mode, type:
COMMAND: exit()

########################################

Now database has been built.

We then need to put in an admin user.

to do this, go into the directory of the database
(Sometimes, it creates in currect directory, sometimes it makes a folder called "instance")

When inside directory where mrbronshoj.db is, do the following:

COMMAND : sqlite3 mrbronshoj.db
########################################
then copy in the insert stamement:
COMMAND: 


INSERT
INTO Users (username, password, usertype, balance)
VALUES ('admin', 'admin', 'admin', 10000);


########################################
We also need to load in the teams. copy in the insert statement:
COMMAND:


INSERT INTO Teams (teamname) VALUES
('Real Madrid'),
('Barcelona'),
('Atletico Madrid'),
('Sevilla'),
('Valencia'),
('Villarreal'),
('Real Sociedad'),
('Athletic Bilbao'),
('Real Betis'),
('Celta Vigo'),
('Granada'),
('Levante'),
('Osasuna'),
('Getafe'),
('Espanyol'),
('Alaves'),
('Mallorca'),
('Cadiz'),
('Elche'),
('Rayo Vallecano');

########################################

Lastly we now would like to boot up the project, we will type this into our terminal:
COMMAND: python app.py

########################################

The project should then be ready to run! 
There has been some trouble with the ports for us,
so we have sat port=5001 as standard. 5000 works sometimes
as well. 
########################################
To use the homepage, begin by signing in as an admin using the username "admin" and password "admin". Once signed in, you can create a game. After creating the game, sign out and register as a user.
As a user, when you log in, you should be able to see the games you just created as an admin. You can then place bets on these games. To finalize the results, log back in as an admin and select the outcome of the game. You will then see that the user's balance has been updated based on the result.

########################################

FORMALITIES FOR ASSIGNMENT: 
made in flask
uses sqlalchemy and sqlite3 for database management
uses Tailwind for css
queries and alters a database (see routes in app.py)
uses regex (for username and password requirements) (look at /register route in app.py)


