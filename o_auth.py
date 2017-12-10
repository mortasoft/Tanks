from flask import Flask, request, jsonify, render_template, request, redirect, url_for
from random import randint
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.github import make_github_blueprint, github
# Instalar el paquete:
# flask_httpauth

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['tanks'] = []
app.config['number'] = 0
app.config['SECRET_KEY'] = 'ulacit'
width = 1366  # Ancho del tablero
height = 768  # Largo del tablero
pixHeight = 28;
pixWidth = 28;

#github_blueprint = make_github_blueprint(client_id='df32b1b8d9c4dd730a0c', client_secret='5f90f651009036ccc49a2b93a2e445e7f4b67ee9')
github_blueprint = make_github_blueprint(client_id='d4056701894d81060774', client_secret='bb3955555590d78e26988a09aac4ab31fac26dd0')

app.register_blueprint(github_blueprint, url_prefix='/github_login')

@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        return redirect('/Battle-Tanks')

    return '<h1>Request failed!</h1>'

# Tank Class
class Tank:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.direction = 'right'
        self.hp = 100
        self.alive = True

    # Prints the tank information
    def print(self):
        return {'x': self.x, 'y': self.y, 'name': self.name, 'direction': self.direction, 'hp': self.hp,
                'alive': self.alive}


@app.route("/createTank")
def createNewTank():
    randomX = randint(0, (width-pixWidth))
    randomY = randint(0, (height-pixHeight))
    number = app.config['number'] = app.config['number'] + 1
    tank = Tank(randomX, randomY, 'Tank_' + str(number))
    app.config['tanks'].append(tank)
    return jsonify(tank.print())


@app.route('/shot', methods=['GET'])
def shot():
    tank = request.args.get('tank')
    hp = request.args.get('hp')
    for i in app.config['tanks']:
        if i.name == tank:
            i.hp -= int(hp)
            if i.hp <= 0:
                i.alive = False
        return jsonify(hp=i.hp, alive=i.alive, name=i.name)
    return jsonify({'Error': 'Not Found or dead'})


@app.route("/tanks")
def tanks():
    out = []
    for i in app.config['tanks']:
        out.append(i.print())
    return jsonify(out)


@app.route("/tank", methods=['GET'])
def atank():
    out = []
    req = request.args.get('id')
    found = False
    for i in app.config['tanks']:
        if i.name == req:
            out.append(i.print())
            found = True

    if found:
        return jsonify(out)
    else:
        return jsonify({'Error': 'Not Found'})


# Direccion principal donde se juega
@app.route('/Battle-Tanks')
def game():
    return render_template('CanvasRec.html')


# Direccion principal donde se juega
@app.route('/')
def root():
    #return render_template('Index.html')
    return redirect('/github')


# Metodo para realizar una jugada aleatoria
@app.route('/play', methods=['GET'])
def jugar_solo():
    for tank in app.config['tanks']:
        random = randint(0,15)

        if random == 0 or random == 2:
            mover(tank.name, "left")
        elif random == 1 or random == 3:
            mover(tank.name, "right")
        elif random == 4 or random == 6:
            mover(tank.name, "up")
        elif random == 5 or random == 7:
            mover(tank.name, "down")
        elif random == 8 or random == 9:
            mover(tank.name, "right")
            mover(tank.name, "right")
        elif random == 10 or random == 12:
            mover(tank.name, "left")
            mover(tank.name, "left")
        elif random == 11 or random == 13:
            mover(tank.name, "up")
            mover(tank.name, "up")
        elif random == 14 or random == 15:
            mover(tank.name, "down")
            mover(tank.name, "down")

    out = []
    for i in app.config['tanks']:
        out.append(i.print())
    return jsonify(out)

# Metodo que mueve un tanque en una direccion dada
def mover(name, direction):
    for tank in app.config['tanks']:
        if tank.name == name:
            if direction == 'right':
                if(tank.x<=(width-pixWidth)):
                    tank.x += 5
                    tank.direction= 'right'
                return
            if direction == 'left':
                if(tank.x>0):
                    tank.x -= 5
                    tank.direction= 'left'
                return
            if direction == 'up':
                if(tank.y>0):
                    tank.y -= 5
                    tank.direction= 'up'
                return
            if direction == 'down':
                if(tank.y<=(height-pixHeight)):
                    tank.y += 5
                    tank.direction= 'down'
                return

if __name__ == '__main__':
    print("----Iniciando servidor de Battle Tanks----")
    app.run('0.0.0.0', 8888)
