from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'unhackable123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mrbronshoj.db'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    usertype = db.Column(db.String(8), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(150), nullable=False, unique=True)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.Integer, nullable=False)
    team2 = db.Column(db.Integer, nullable=False)
    t1wins = db.Column(db.Float, nullable=False)
    draw = db.Column(db.Float, nullable=False)
    t2wins = db.Column(db.Float, nullable=False)


class Bets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)
    pot_cashout = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    if 'username' in session and 'usertype' in session and 'balance' in session:
        username = session['username']
        balance = session['balance']
        # SQL EXECUTIING BELOW IS:
        # SELECT * FROM Games
        # SAID BY TA's TO BE OKAY

        games = Games.query.all()
        if session['usertype'] == "customer":
            return render_template('customer_page.html', username=username, usertype ='customer', games=games)
        
        elif session['usertype'] == "admin":
            return redirect(url_for('admin_page'))
        
    else:
        return render_template('index.html')


@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        outcome = request.form['bet_selection'] 
        gameid = request.args.get('gameid')
        bets = Bets.query.filter_by(game=gameid,prediction=outcome).all()
        for bet in bets:
            winneruser = Users.query.filter_by(username=bet.user).first()
            winneruser.balance = winneruser.balance + bet.pot_cashout

        bets_to_delete = Bets.query.filter_by(game=gameid).all()
        for bet in bets_to_delete:
            db.session.delete(bet)

        game_to_del = Games.query.filter_by(id=gameid).first()
        db.session.delete(game_to_del)
        db.session.commit()

        return redirect(url_for('index'))

    elif request.method == 'GET':
        if 'username' in session and 'usertype' in session:
            username = session['username']
            games = Games.query.all()
            if session['usertype'] == "admin":
                return render_template('admin_page.html', username=username, usertype='admin', games=games)

@app.route('/create_bet', methods=['GET', 'POST'])
def create_bet():
    if request.method == 'POST':
        returnA = request.form['returna']
        returnB = request.form['returnb']
        draw = request.form['draw']
        teamA = request.form['teamA']
        teamB = request.form['teamB']
        
        if returnA == "" or returnB == "" or draw == "":
            return render_template('/create_bet.html', error="Outcomes must have returns.")

        if float(returnA) <= 1.0 or float(returnB) <= 1.0 or float(draw) <= 1.0:
            return render_template('/create_bet.html', error="Return must be over 1")

        if teamA == teamB:
            return render_template('/create_bet.html', error="Teams are the same, choose distinct teams.")
        
        potential_same_game = Games.query.filter_by(team1=teamA, team2=teamB).first()
        if potential_same_game:
            return render_template('/create_bet.html', error="The game is already created. Create another game")
        else:
            # SQL EXECUTIING BELOW IS:
            # INSERT INTO Games (team1, team2, t1wins, draw, t2wins)
            # VALUES (<teamA>, <teamB>, <returnA>, <draw>, <returnB>)

            #SAID BY TA's TO BE OKAY
            
            new_game = Games(team1=teamA, team2=teamB, t1wins=returnA, draw=draw, t2wins=returnB)
            db.session.add(new_game)
            db.session.commit()
            return redirect(url_for('index'))
           
    elif request.method == 'GET':
        return render_template('/create_bet.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
    

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    username = session['username']
    userbalance = session['balance']
    return render_template('profile.html',username=username,Balance=userbalance)

@app.route('/game')
def game():
    games = Games.query.all()
    return render_template('game.html', games=games)


@app.route('/bet_on_game', methods=['GET', 'POST'])
def bet_on_game():
    if request.method == "POST":
        amount = request.form['amount']
        if int(amount) > int(session['balance']):
            return render_template('bet_on_game.html', error = "You don't have that much money, buddy :(")

        team1 = request.args.get('team1')
        team2 = request.args.get('team2')
        t1wins = request.args.get('t1wins')
        draw = request.args.get('draw')
        t2wins = request.args.get('t2wins')
        gameid = request.args.get('id')
        list = [t1wins, draw, t2wins]
        odds = 0
        prediction = ""
        for elm in list:
            if elm != "0":
                odds = float(elm)
                names = ["t1wins", "draw", "t2wins"]
                prediction = names[list.index(elm)] 

        # SQL EXECUTIING BELOW IS:
        # INSERT INTO Bets (game, user, amount, prediction, pot_cashout) 
        # VALUES (<gameid>, <session['username']>, <amount>, <prediction>, <float(amount)*odds>)

        #SAID BY TA's TO BE OKAY

        new_bet = Bets(game=gameid, user=session['username'], amount=amount, prediction=prediction, pot_cashout=float(amount)*odds)
        db.session.add(new_bet)

        # SQL EXECUTIING BELOW IS:
        # UPDATE Users
        # SET balance = balance - int(amount)
        # WHERE username = session['username'];

        #SAID BY TA's TO BE OKAY

        bettaker = Users.query.filter_by(username=session['username']).first()
        bettaker.balance = bettaker.balance - int(amount)
        db.session.commit()
        session["balance"] = bettaker.balance
        return redirect(url_for('index'))

    elif request.method == "GET":
        return render_template('bet_on_game.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        # SQL EXECUTIING BELOW IS:
        # SELECT * FROM Users WHERE username= username AND password = password
        # SAID BY TA's TO BE OKAY.
        # techically not same query, but because username is unique, all is also
        # always the first and vice versa. 
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            session['usertype'] = user.usertype
            session['balance'] = user.balance
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
   
    elif request.method == 'GET':
        return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usertype = 'customer'
        balance = request.form['balance']
        
        password_pattern = re.compile(r'^[A-z0-9!?]{8,}$')
        if not password_pattern.match(password):
            return render_template('register.html', error="Password must be minimum 8 chars long. Password can only contain alphanumeric, '!' and '?'")
        
        elif not password_pattern.match(username):
            return render_template('register.html', error="Username must be minimum 8 chars long. Username can only contain alphanumeric, '!' and '?'")

        elif int(balance) <= 0:
            return render_template('register.html', error="We don't associate with broke people")

        # SQL EXECUTIING BELOW IS:
        # SELECT * FROM User WHERE username = <username>
        # SAID BY TA's TO BE OKAY

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="Username already exists. Please try again.")
        else:
            new_user = Users(username=username, password=password, usertype=usertype, balance=balance)
            # SQL EXECUTIING BELOW IS:
            # INSERT INTO User (username, password, usertype, balance)
            # VALUES (<username>, <password>, <usertype>, <balance>)
            #SAID BY TA's TO BE OKAY

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
           
    elif request.method == 'GET':
        return render_template('register.html')
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
