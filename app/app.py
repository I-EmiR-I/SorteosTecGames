from flask import Flask, request, jsonify, render_template, session, url_for,redirect
import csv
from datetime import datetime
import random
from flask_cors import CORS
from database import *

app = Flask(__name__,static_folder='/')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'tu_clave_secreta'  # Clave secreta para cifrar la sesión


#Documentacion
@app.route('/Documentation')
def Documentation():
  html_documentation = 'documentation.html'
  return render_template(html_documentation)

# Verifica si el usuario existe en la base de datos, si existe lo manda a la pagina principal
@app.route("/TryLogin",methods=["GET","POST"])
def try_login():
  #email = request.args.get('email')
  #contraseña = request.args.get('password')
  email = request.form['email']
  contraseña = request.form['password']
  verificar = login(email, contraseña)
  
  if verificar != 'Contraseña incorrecta.' and verificar != 'El usuario no existe.':
    session['username'] = email
    session['password'] = contraseña
    session['nombre'] = str(verificar[1])
    session['vidas'] = str(devolver_vidas(int(verificar[0])))
    session['cupones'] = str(devolver_cupones(int(verificar[0])))
    session['saldo'] = str(devolver_saldo(int(verificar[0]))) #int(verificar[0]) = id
    session['admin'] = str(usuario_admin(int(verificar[0]))) #False = no admin
    if session['admin'] == "False":
      return redirect(url_for('Principal'))
    else:
      return redirect(url_for('Administrador'))
    #return render_template('pagina_principal.html')
  else:
    return render_template('index.html')

  # Registro utilizado para hacer pruebas
@app.route('/Registro')
def Registro():
  html = 'registro.html'
  return render_template(html)

# Pagina de login
@app.route('/Test')
def Test():
  session['admin'] = False
  return render_template('index.html')

# Funcion para verificar si el usuario gana o pierde en el juego de la garra
@app.route('/win_or_loose')
def win_or_loose():
  #Logica para definir la probabilidad de victoria
  bolitas = 10 # Probabilidad de ganar
  win = random.randint(1,bolitas) 
  bolita = random.randint(1,bolitas)
  if bolita == win:
    return 'win'
  
  bolitas+=1
  print('bolitas:',bolitas)
  return 'loose'

# Funcion para verificar si el usuario existe en la base de datos
@app.route('/Login', methods=['GET'])
def Login():
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')

    mensaje = login(email, contraseña)
    #session['email'] = email
    #session['contraseña'] = contraseña
    #session['nombre'] = str(mensaje[1])
    return str(mensaje)

# Crea la base de datos
@app.route('/create_database')
def create():
  # Start program
  conn,cursor = conectar_base_datos()

  # Create database
  create_database(cursor)
  return 'Base de datos creada exitosamente'

# Muestra los usuarios
@app.route('/display_users')
def mostrar_usuarios():
  usuarios_json = display_users()  # Obtener la cadena JSON de los usuarios
  return jsonify(usuarios_json)
  #return 'Usuarios desplegados exitosamente'

@app.route('/display_user')
def mostrar_usuario():
  user_id = request.args.get('id')  # Obtener el ID del usuario de los parámetros de consulta
  user_id = int(user_id)
  if user_id is not None:
      usuario_info = display_users()  # Obtener la información del usuario por su ID
      for usuario in usuario_info:
        if usuario[0] == user_id:
          return jsonify(usuario)
      if usuario_info:
          return jsonify(usuario_info)
      else:
          return jsonify({"error": "Usuario no encontrado"}), 404
  else:
      return jsonify({"error": "Se requiere el parámetro 'id' en la consulta"}), 400

# Crea un usuario
@app.route('/create_user',methods=["GET","POST"])
def crear_usuario():
  if request.method == "POST":
    nombre = request.form['nombre']
    email = request.form['email']
    contraseña = request.form['contraseña']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    ciudad = request.form['ciudad']
    estado = request.form['estado']
    telefono = request.form['telefono']
    try:
      if (session['admin'] == "True"):
        admin = True
      admin = False  
    except:
      admin = False
    usuario = {
          "nombre": nombre,
          "email": email,
          "contraseña": contraseña,
          "apellido_paterno": apellido_paterno,
          "apellido_materno": apellido_materno,
          "ciudad": ciudad,
          "estado": estado,
          "telefono": telefono
    }
    #return usuario
    if create_user(usuario,admin) == "Usuario registrado exitosamente.":
      return render_template('registro-exitoso.html')
    return 'test'
# Pruebas
@app.route('/Menu_compras')
def prueba():
  return """<form action="/vidas_usuario" method="GET">
    Email: <input type="text" name="email"><br>
    Contraseña: <input type="password" name="contraseña"><br>
    
    <input type="submit" value="Comprar">
</form>"""

@app.route('/datos', methods=["GET","POST"])
def datos():
  email = request.form['email']
  contraseña = request.form['contraseña']
  id = str(login(email,contraseña)[0])
  id = int(id)
  vidas = str(devolver_vidas(id))
  cupones = str(devolver_cupones(id))
  saldo = str(devolver_saldo(id))

# Devolver vidas
@app.route('/vidas_usuario',methods=["GET","POST"])
def vidas():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  
  else:
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  id = str(login(email,contraseña)[0])
  id = int(id)
  vidas = str(int(devolver_vidas(id)))
  return vidas

# Devolver cupones
@app.route('/cupones_usuario',methods=["GET","POST"])
def cupones():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  id = str(login(email,contraseña)[0])
  id = int(id)
  cupones = str(devolver_cupones(id))
  return cupones

# Devolver saldo
@app.route('/saldo_usuario',methods=["GET","POST"])
def saldo():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  id = str(login(email,contraseña)[0])
  id = int(id)
  saldo = str(devolver_saldo(id))
  return saldo

# Comprar cupon
@app.route('/Comprar_cupon',methods=["GET","POST"])
def comprar_cupon():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
    cantidad = request.form['cantidad']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
    cantidad = request.args.get('cantidad')
    
  id = str(login(email,contraseña)[0])
  id = int(id)
  if str(sumar_cupones(id,cantidad)) == "Saldo insuficiente":
    return "Saldo insuficiente"
  return str (devolver_cupones(id))
  
# Comprar vidas
@app.route('/Comprar_vidas',methods=["GET","POST"])
def comprar_vidas():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
    cantidad = request.form['cantidad']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
    cantidad = request.args.get('cantidad')
    
  id = str(login(email,contraseña)[0])
  id = int(id)
  if str(sumar_vidas(id,cantidad)) == "Saldo insuficiente":
    return "Saldo insuficiente"
  return str (devolver_vidas(id))

# Agregar saldo
@app.route('/Comprar_saldo',methods=["GET","POST"])
def comprar_saldo():
  if request.method == "POST":
    try:
      # Aquí puedes realizar las operaciones necesarias con los datos recibidos
      email = session['username']
      contraseña = session['password']
    except:
      email = request.form['email']
      contraseña = request.form['contraseña']
    cantidad = request.form['cantidad']
      
  elif request.method == "GET":
    try:
      # Aquí puedes realizar las operaciones necesarias con los datos recibidos
      email = session['username']
      contraseña = session['password']
    except:
      email = request.args.get('email')
      contraseña = request.args.get('contraseña')
    cantidad = request.args.get('cantidad')
    
  id = str(login(email,contraseña)[0])
  id = int(id)
  sumar_saldo(id,cantidad)
  if request.method == "POST":
    session['saldo'] = str(devolver_saldo(id))
    return redirect(url_for('Wallet'))
  return str (devolver_saldo(id))

# Agregar skin
@app.route('/add_skin',methods=["GET","POST"])
def add_skin():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
    skin = request.form['skin']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
    skin = request.args.get('skin')
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  return str(create_skin(id,int(skin)))

# Agregar song
@app.route('/add_song',methods=["GET","POST"])
def add_song():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
    skin = request.form['song']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
    skin = request.args.get('song')
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  return str(create_song(id,int(skin)))

# Agregar song ritmico
@app.route('/add_song_ritmico',methods=["GET","POST"])
def add_song_ritmico():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
    skin = request.form['song']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
    skin = request.args.get('song')
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  return str(create_song_ritmico(id,int(skin)))

# Devolver skins
@app.route('/get_skins',methods=["GET","POST"])
def skins():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  return str(get_skins(id))

# Devolver canciones
@app.route('/get_songs',methods=["GET","POST"])
def songs():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  return str(get_songs(id))

# Devolver canciones
@app.route('/get_songs_ritmico',methods=["GET","POST"])
def songs_ritmico():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  return str(get_songs_ritmico(id))

@app.route('/agregar_registro_garra', methods=['GET'])
def registro_garra():
    if request.method == "GET":
      email = request.args.get('email')
      contraseña = request.args.get('contraseña')
      intento = request.args.get('intento')
      resultado = request.args.get('resultado')
      premio_actual = request.args.get('premio_actual')

    id = str(login(email,contraseña)[0])
    id = int(id)
  
    agregar_registro_garra(id, intento, resultado, premio_actual)
    return 'registro agregado exitosamente'
  
@app.route('/ultimo_intento')
def premio_actual():
    saldo = obtener_ultimo_intento()[-1]
    gano_perdio = obtener_ultimo = obtener_ultimo_intento()[-2]
    intento = obtener_ultimo_intento()[-3]
    return str([str(saldo),str(gano_perdio),intento])

@app.route('/devolver_tarjeta',methods=["GET","POST"])
def devolver_tarjeta():
  if request.method == "POST":
    email = request.form['email']
    contraseña = request.form['contraseña']
  elif request.method == "GET":
    email = request.args.get('email')
    contraseña = request.args.get('contraseña')
  
  email = session['username']
  contraseña = session['password']
  
  id = str(login(email,contraseña)[0])
  id = int(id)
  
  return obtener_tarjetas_usuario(id)

@app.route('/agregar_tarjeta', methods=["GET", "POST"])
def tarjeta():
    if request.method == "POST":
        numerotarjeta = request.form['numerotarjeta']
        nombreTitular = request.form['nombreTitular']
        fechaVencimiento = request.form['fechaVencimiento']
        cvv = request.form['cvv']
    
    #metodo pendiente de implementar
    elif request.method == "GET":
        tarjeta = request.args.get('NumTarjeta')
        cvv = request.args.get('cvv')
        fecha = request.args.get('fechaVencimiento')
        nombre = request.args.get('nombreTitular')
    
    # Aquí puedes realizar las operaciones necesarias con los datos recibidos
    email = session['username']
    password = session['password']
    id = str(login(email,password)[0])
    id = int(id)
    agregar_tarjeta(id,fechaVencimiento,cvv,nombreTitular,numerotarjeta)
    return redirect(url_for('Pago'))

#@app.route('/eliminar_tarjeta', methods=["GET", "POST"])
#def eliminar_tarjeta():
    #if request.method == "POST":
        #email = request.form['email']
        #contraseña = request.form['contraseña']
    
    #metodo pendiente de implementar
    #elif request.method == "GET":
        #email = request.args.get('email')
        #contraseña = request.args.get('contraseña')
    
    # Aquí puedes realizar las operaciones necesarias con los datos recibidos
    #id = str(login(email,contraseña)[0])
    #id = int(id)
    #elmininar_tarjetas(id)  
    #return 'eliminación exitosa'

    
# Entradas a la pagina
@app.route('/Perfil')
def Perfil():
  return render_template('perfil.html',Nombre=session['nombre'],Email=session['username'],Saldo=session['saldo'],Vidas=session['vidas'],Cupones=session['cupones'])

@app.route('/pagina_principal')
def Principal():
  if session['admin'] == "False":
      pass
  else:
      return redirect(url_for('Administrador'))
  return render_template('pagina_principal.html')

@app.route('/pagina_admin')
def Administrador():
  return render_template('pagina_admin.html')

@app.route('/wallet')
def Wallet():
  return render_template('wallet.html',Saldo=session['saldo'])

@app.route('/Pago')
def Pago():
  return render_template('Forma_pago.html')

if __name__ == '__main__':
    
    app.run(port=5000)