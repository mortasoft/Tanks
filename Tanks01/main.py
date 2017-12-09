from flask import Flask, request, jsonify, render_template, request, redirect
from random import randint

app = Flask(__name__)

app.config['tanks'] = []
app.config['number'] = 0

# Variables del juego
width = 336 # Ancho del tablero
height = 324 # Largo del tablero
pixWidth = 28 # Ancho del pix
pixHeight = 27 # Largo del Pix

disparos = []

# Tank Class
class Tank:
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.direction = 'left'
        self.hp = 100
        self.alive = True

    # Prints the tank information
    def print(self):
        return {'x':self.x,'y':self.y,'name':self.name,'direction': self.direction,'hp': self.hp,'alive':self.alive}

@app.route("/createTank")
def createNewTank():
    randomX = randint(27, 300)
    randomY = randint(27, 300)
    number = app.config['number'] = app.config['number'] + 1
    tank = Tank(randomX,randomY,'Tank_'+str(number))
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
        return jsonify(hp=i.hp,alive=i.alive,name=i.name)
    return jsonify({'Error':'Not Found or dead'})

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
		return jsonify({'Error':'Not Found'})

# Direccion principal donde se juega
@app.route('/Battle-Tanks')
def game():
    return render_template('CanvasRec.html')

# Direccion principal donde se juega
@app.route('/')
def root():
    return redirect('/Battle-Tanks')


# Metodo para realizar una jugada aleatoria
@app.route('/jugada', methods=['GET'])
def jugar_solo():
    if request.method == 'GET':
        jugador= request.args.get('jugador')
        if jugador in ("1","2"):
            num_aleatorio = randint(0, 3)
            if (num_aleatorio == 0):
                resultado = mover(str(jugador), "izquierda")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="movimiento", direccion="izquierda", x=resultado[0],y=resultado[1])
            if (num_aleatorio == 1):
                resultado = mover(str(jugador), "derecha")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="movimiento", direccion="derecha", x=resultado[0],y=resultado[1])
            if (num_aleatorio == 2):
                resultado = mover(str(jugador), "arriba")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="movimiento", direccion="arriba",x=resultado[0],y=resultado[1])
            if (num_aleatorio == 3):
                resultado = mover(str(jugador), "abajo")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="movimiento", direccion="abajo", x=resultado[0],y=resultado[1])
            if (num_aleatorio == 4):
                #mover(jugador, "abajo")
                print("Disparo bala 1")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="disparar", dato="bala1")
            if (num_aleatorio == 5):
                #mover(jugador, "abajo")
                print("Disparo bala 2")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="disparar", dato="bala2")
            if (num_aleatorio == 6):
                #mover(jugador, "abajo")
                print("Disparo bala 3")
                return jsonify(tanque=jugador, aleatorio=num_aleatorio, accion="disparar", dato="bala3")
        else:
            return jsonify(error="Error, parametros incorrectos")

# Metodo que mueve un tanque en una direccion dada
def mover(tanque,direccion):
    global tank2_x
    global tank2_y
    global tank2_direccion
    global tank1_x
    global tank1_y
    global tank1_direccion

    if(tanque=="1"):
        if direccion=="derecha" :
            if(tank1_x <=308):
                tank1_x+=4
                tank1_direccion="derecha"
                print("Tanque 1 se movio a la derecha")
            else:
                print("Ya no se puede mover en esa direccion")
        if direccion == "izquierda":
            if tank1_x > 0:
                tank1_x -= 4
                tank1_direccion = "izquierda"
                print("Tanque 1 se movio a la izquierda")
            else:
                print("Ya no se puede mover en esa direccion")
        if direccion == "arriba":
            if tank1_y > 0:
                tank1_y -= 4
                tank1_direccion = "arriba"
                print("Tanque 1 se movio arriba")
            else:
                print("Ya no se puede mover en esa direccion")
        if direccion == "abajo":
            if tank1_y <= height - pixHeight:
                tank1_y += 4
                tank1_direccion = "abajo"
                print("Tanque 1 se movio abajo")
            else:
                print("Ya no se puede mover en esa direccion")

        print("Nueva posicion tanque 1: x:" + str(tank1_x) + " y: " + str(tank1_y))
        return [tank1_x,tank1_y]

    if (tanque == "2"):

        if direccion == "derecha":
            if (tank2_x <= 308):
                tank2_x += 4
                tank2_direccion = "derecha"
                print("Tanque 2 se movio a la derecha")
            else:
                print("Ya no se puede mover en esa direccion")
        if direccion == "izquierda":
            if tank2_x > 0:
                tank2_x -= 4
                tank2_direccion = "izquierda"
                print("Tanque 2 se movio a la izquierda")
            else:
                print("Ya no se puede mover en esa direccion")
        if direccion == "arriba":
            if tank2_y > 0:
                tank2_y -= 4
                tank2_direccion = "arriba"
                print("Tanque 2 se movio arriba")
            else:
                print("Ya no se puede mover en esa direccion")
        if direccion == "abajo":
            if tank2_y <= height - pixHeight:
                tank2_y += 4
                tank2_direccion = "abajo"
                print("Tanque 2 se movio abajo")
            else:
                print("Ya no se puede mover en esa direccion")

        print("Nueva posicion tanque 2: x:" + str(tank2_x) + " y: " + str(tank2_y))
        return tank2_x, tank2_y

if __name__ == '__main__':
    print("----Iniciando servidor de Battle Tanks----")
    app.run('0.0.0.0',8888)