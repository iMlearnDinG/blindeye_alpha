from flask import Flask, render_template, session, request, redirect, flash
from flask_socketio import SocketIO, emit
import csv

# Read CSV file and store username-password combinations
users = {}
with open('users.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        users[row['username']] = row['password']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

game_sessions = {1: 0, 2: 0}


def count_sessions_in_game(game_number):
    count = 0
    room_name = '/game' + str(game_number)
    if room_name in socketio.server.manager.rooms:
        count = len(socketio.server.manager.rooms[room_name]) - 1  # Subtract 1 for the current session
    return count


@app.route('/')
def home():
    if 'username' in session:
        return redirect('/lobby')  # Redirect to the lobby page if the user is logged in
    else:
        return redirect('/login')  # Redirect to the login page if the user is not logged in


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username  # Store the username in the session
            return redirect('/lobby')  # Redirect to the lobby page if login is successful
        else:
            return 'Invalid username or password'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect('/')


@app.route('/lobby')
def lobby():
    if 'username' in session:
        username = session['username']
        game1_disabled = False
        game2_disabled = False

        # Logic to determine the state of the game buttons
        if count_sessions_in_game(1) >= 2:
            game1_disabled = True
        if count_sessions_in_game(2) >= 2:
            game2_disabled = True

        return render_template('lobby.html', username=username, game1_disabled=game1_disabled, game2_disabled=game2_disabled)
    else:
        return redirect('/login')  # Redirect to the login page if the user is not logged in


@app.route('/game', methods=['POST'])
def game():
    game_number = int(request.form['game'])

    if game_sessions[game_number] >= 2:
        flash(f'Game {game_number} is full. Please select another game.')
        return redirect('/lobby')

    game_sessions[game_number] += 1  # increment the player count
    return redirect(f'/game/{game_number}')


@app.route('/game/<int:game_number>')
def display_game(game_number):
    return render_template('game.html', game_number=game_number)


@socketio.on('lobby')
def handle_lobby():
    if 'username' in session:
        emit('lobby_response', {'username': session['username']})
    else:
        emit('redirect', {'location': '/login'})


@socketio.on('move_card')
def handle_move_card(data):
    card_id = data['card_id']
    new_position = data['new_position']
    # Handle the card movement logic here
    # Update the card position in the server-side data structure or perform other relevant actions
    # ...
    # Emit an event to notify other clients about the card movement
    emit('card_moved', {'card_id': card_id, 'new_position': new_position}, broadcast=True)

@socketio.on('leave_game')
def on_leave(data):
    game_number = data['game']
    game_sessions[game_number] -= 1  # decrement the player count


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
