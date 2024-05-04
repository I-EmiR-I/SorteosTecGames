
from datetime import datetime
import json

import mysql.connector
# Aiven connection details
dbname = 'defaultdb'
user = 'avnadmin'
password = 'secret password :)'
host =  'mysql-156e6015-tec-2f91.a.aivencloud.com'
port = '27826'

def conectar_base_datos():
    # Establishing the connection
    conn = mysql.connector.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    return conn, cursor

def create_database(cursor):
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
    ID_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255),
    Email VARCHAR(255),
    Contraseña VARCHAR(255),
    Apellido_Paterno VARCHAR(255),
    Apellido_Materno VARCHAR(255),
    Ciudad VARCHAR(255),
    Estado VARCHAR(255),
    telefono VARCHAR(20),
    Fecha_Registro DATETIME,
    Ultima_conexion DATETIME
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Wallet (
    ID_Cliente INT PRIMARY KEY,
    Saldo INT,
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario (ID_Cliente)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Compra (
    ID_Compra INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Elemento_comprado TEXT,
    Fecha_compra DATETIME,
    Ingreso INT,
    Cantidad INT,
    FOREIGN KEY (ID_Cliente) REFERENCES Wallet (ID_Cliente)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Elementos (
    ID_Cliente INT PRIMARY KEY,
    Num_Vidas INT,
    Num_cupones INT,
    TEUS_Design TEXT,
    Unlocked_SONGS TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario (ID_Cliente)
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Skins (
    ID_Skin INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Skin1 INT,
    Skin2 INT,
    Skin3 INT,
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario (ID_Cliente)
    );''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Canciones (
    ID_Cancion INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Cancion1 INT,
    Cancion2 INT,
    Cancion3 INT,
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario (ID_Cliente)
    );''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Canciones_ritmico (
    ID_Cancion INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Cancion1 INT,
    Cancion2 INT,
    Cancion3 INT,
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario (ID_Cliente)
    );''')
    

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Garra (
    ID_garra INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    intento INT,
    gano_perdio ENUM('Gano', 'Perdio'),
    premio_actual DECIMAL(10, 2),
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario(ID_Cliente)
);''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tarjetas (
    ID_Tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    Numero_Tarjeta VARCHAR(16),
    Fecha_Expiracion VARCHAR(16),
    CVV INT,
    Nombre VARCHAR(16),
    FOREIGN KEY (ID_Cliente) REFERENCES Usuario (ID_Cliente)
);''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scores (
    ID_Cliente INT PRIMARY KEY,
    Ganados INT,
    Perdidos INT,
    Winrate DECIMAL(5, 2)
);
''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ganancias (
    ID_ganancia INT AUTO_INCREMENT PRIMARY KEY,
    ID_cliente INT,
    tipo_ganancia ENUM('Vidas', 'Cupones', 'Canciones', 'Skins', 'Dinero', 'Retiro'),
    cantidad DECIMAL(10, 2),
    FOREIGN KEY (ID_cliente) REFERENCES Usuario(ID_cliente)
);''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS UsuariosAdmin (
    ID_Admin INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Cliente)
    ON DELETE CASCADE
);
''')
    print("Database tables created successfully.")
  
def obtener_ultimo_intento():
    conn, cursor = conectar_base_datos()
    try:
        query = "SELECT * FROM Garra ORDER BY ID_garra DESC LIMIT 1"
        cursor.execute(query)
        ultimo_intento = cursor.fetchone()
        if ultimo_intento:
            print("Último intento obtenido:", ultimo_intento)
            return ultimo_intento
        else:
            print("No se encontraron registros en la tabla Garra.")
            return None
    except mysql.connector.Error as error:
        print("Error al obtener el último intento:", error)
        return None
    finally:
        cursor.close()
        conn.close()

def agregar_registro_garra(id_cliente, intento, resultado, premio_actual):
    conn, cursor = conectar_base_datos()
    try:
        query = "INSERT INTO Garra (ID_Cliente, intento, gano_perdio, premio_actual) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_cliente, intento, resultado, premio_actual))
        conn.commit()
        print("Registro agregado correctamente a Garra")
    except mysql.connector.Error as error:
        print("Error al agregar el registro:", error)
    finally:
        cursor.close()
        conn.close()
  
def obtener_tarjetas_usuario(id_usuario):
    try:
        conn, cursor = conectar_base_datos()  # Suponiendo que tienes una función conectar_base_datos() que establece la conexión a la base de datos
        query = f"SELECT * FROM Tarjetas WHERE ID_Cliente = {id_usuario}"
        cursor.execute(query)
        tarjetas = cursor.fetchall()  # Obtener todas las filas resultantes de la consulta
        return tarjetas
    except mysql.connector.Error as error:
        print("Error al obtener las tarjetas:", error)
        return None
    finally:
        cursor.close()
        conn.close()
        
def agregar_tarjeta(id_usuario, fecha, cvv, nombre, tarjeta):
    conn, cursor = conectar_base_datos()
    tarjeta = tarjeta.replace(" ", "")
    try:
        query = f"INSERT INTO Tarjetas (ID_Cliente, Numero_Tarjeta, Fecha_Expiracion, CVV, Nombre) VALUES ('{id_usuario}', '{tarjeta}', '{fecha}', '{cvv}', '{nombre}')"
        cursor.execute(query)
        conn.commit()
        print("Tarjeta agregada correctamente a Tarjetas")
        return 'Tarjeta agregada exitosamente'  
    except mysql.connector.Error as error:
        print("Error al agregar la tarjeta:", error)
        return 'error al agregar tarjeta'
    finally:
        cursor.close()
        conn.close()
      
def agregar_intento_garra(id_usuario, intento, gano_perdio, premio_actual):
    conn, cursor = conectar_base_datos()
    try:
        # Insertar un nuevo registro en la tabla Garra
        query = f"INSERT INTO Garra (ID_usuario, intento, gano_perdio, premio_actual) VALUES ({id_usuario}, {intento}, '{gano_perdio}', {premio_actual})"
        cursor.execute(query)
        conn.commit()
        print("Intento agregado correctamente a Garra.")
    except mysql.connector.Error as error:
        print("Error al agregar el intento a Garra:", error)
        return 'error al agregar intento'
    finally:
        cursor.close()
        conn.close()
    return 'intento agregado exitosamente'
    
def login(email, contraseña):
    conn, cursor = conectar_base_datos()
    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT * FROM Usuario WHERE Email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            # Verificar la contraseña
            if usuario[3] == contraseña: #3 es el index de la contraseña
                # Actualizar la fecha de última conexión
                ultima_conexion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE Usuario SET Ultima_conexion = %s WHERE ID_Cliente = %s", (ultima_conexion, usuario[0])) #0 es el index del id_usuario
                conn.commit()
                print("Inicio de sesión exitoso.")
                conn.close()
                return usuario
            else:
                print("Contraseña incorrecta.")
                conn.close()
                return 'Contraseña incorrecta.'
        else:
            print("El usuario no existe.")
            conn.close()
            return 'El usuario no existe.'
    except mysql.connector.Error as e:
        print("Error al iniciar sesión:", e) 
    
def create_user(usuario,es_admin=False):
    conn, cursor = conectar_base_datos()
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Create user
        cursor.execute('''INSERT INTO Usuario (Nombre, Email, Contraseña, Apellido_Paterno, Apellido_Materno, Ciudad, Estado, telefono, Fecha_Registro, Ultima_conexion) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                   (usuario["nombre"], usuario["email"], usuario["contraseña"], usuario["apellido_paterno"], usuario["apellido_materno"], usuario["ciudad"],
                    usuario["estado"], usuario["telefono"], fecha_registro, fecha_registro))
        # Obtener el ID del usuario recién insertado
        id_usuario = cursor.lastrowid

        # Insertar una nueva entrada en la tabla "Elementos" para el nuevo usuario
        cursor.execute('''INSERT INTO Elementos (ID_Cliente, Num_Vidas, Num_cupones) 
                          VALUES (%s, 0, 0)''', (id_usuario,))
        
        # Crear una entrada en la tabla "Wallet" para el nuevo usuario
        cursor.execute('''INSERT INTO Wallet (ID_Cliente, Saldo) 
                          VALUES (%s, 0)''', (id_usuario,))
        
        # Crear tabla skins y songs
        cursor.execute('''INSERT INTO Skins (ID_Cliente, Skin1, Skin2, Skin3) VALUES (%s, 0, 0, 0)''', (id_usuario,))
        cursor.execute('''INSERT INTO Canciones (ID_Cliente, Cancion1, Cancion2, Cancion3) VALUES (%s, 0, 0, 0)''', (id_usuario,))
        
        # Crear tabla songs para el ritmico
        cursor.execute('''INSERT INTO Canciones (ID_Cliente, Cancion1, Cancion2, Cancion3) VALUES (%s, 0, 0, 0)''', (id_usuario,))
        # Verificar si el usuario debe ser administrador
        if es_admin:
            cursor.execute('''INSERT INTO UsuariosAdmin (ID_Usuario) VALUES (%s)''', (id_usuario,))
            
        conn.commit()
        print("Usuario registrado exitosamente.")
        conn.close()
        return 'Usuario registrado exitosamente.'
    except mysql.connector.Error as e:
        print("Error al registrar usuario:", e)

def create_skin(usuario_id, skin):
    conn, cursor = conectar_base_datos()
    # Actualizar la tabla de Skins para el usuario dado
    try:
        query = f"UPDATE Skins SET Skin{skin} = 1 WHERE ID_Cliente = {usuario_id}"
        cursor.execute(query)
        conn.commit()
        print("Skin agregada correctamente.")
    except mysql.connector.Error as error:
        print("Error al agregar la skin:", error)
        return 'error al agregar skin'
    finally:
        cursor.close()
        conn.close()
    return 'skin agregada existosamente'

def create_song(usuario_id, song):
    conn, cursor = conectar_base_datos()
    
    # Actualizar la tabla de Canciones para el usuario dado
    try:
        query = f"UPDATE Canciones SET Cancion{song} = 1 WHERE ID_Cliente = {usuario_id}"
        cursor.execute(query)
        conn.commit()
        print("Canción agregada correctamente.")
    except mysql.connector.Error as error:
        print("Error al agregar la canción:", error)
        return 'error al agregar cancion'  
    finally:
        cursor.close()
        conn.close()
    return 'cancion agregada exitosamente'

def create_song_ritmico(usuario_id, song):
    conn, cursor = conectar_base_datos()
    
    # Actualizar la tabla de Canciones para el usuario dado
    try:
        query = f"UPDATE Canciones_ritmico SET Cancion{song} = 1 WHERE ID_Cliente = {usuario_id}"
        cursor.execute(query)
        conn.commit()
        print("Canción agregada correctamente.")
    except mysql.connector.Error as error:
        print("Error al agregar la canción:", error)
        return 'error al agregar cancion'  
    finally:
        cursor.close()
        conn.close()
    return 'cancion agregada exitosamente'
  
def get_skins(id_cliente):
    conn, cursor = conectar_base_datos()

    try:
        # Obtener las skins activadas para el usuario dado
        query = f"SELECT Skin1, Skin2, Skin3 FROM Skins WHERE ID_Cliente = {id_cliente}"
        cursor.execute(query)
        skins_activadas = cursor.fetchone()
        
        # Convertir los resultados a una lista con 0 o 1
        skins_activadas_lista = [1 if skin == 1 else 0 for skin in skins_activadas]
        
        print("Skins activadas:", skins_activadas_lista)
        return skins_activadas_lista
    except mysql.connector.Error as error:
        print("Error al obtener las skins activadas:", error)
    finally:
        cursor.close()
        conn.close()

def get_songs(id_cliente):
    conn, cursor = conectar_base_datos()

    try:
        # Obtener las canciones activadas para el usuario dado
        query = f"SELECT Cancion1, Cancion2, Cancion3 FROM Canciones WHERE ID_Cliente = {id_cliente}"
        cursor.execute(query)
        songs_activadas = cursor.fetchone()
        
        # Convertir los resultados a una lista con 0 o 1
        songs_activadas_lista = [1 if song == 1 else 0 for song in songs_activadas]
        
        print("Canciones activadas:", songs_activadas_lista)
        return songs_activadas_lista
    except mysql.connector.Error as error:
        print("Error al obtener las canciones activadas:", error)
    finally:
        # cursor.close()
        conn.close()

def get_songs_ritmico(id_cliente):
    conn, cursor = conectar_base_datos()

    try:
        # Obtener las canciones activadas para el usuario dado
        query = f"SELECT Cancion1, Cancion2, Cancion3 FROM Canciones_ritmico WHERE ID_Cliente = {id_cliente}"
        cursor.execute(query)
        songs_activadas = cursor.fetchone()
        
        # Convertir los resultados a una lista con 0 o 1
        songs_activadas_lista = [1 if song == 1 else 0 for song in songs_activadas]
        
        print("Canciones activadas:", songs_activadas_lista)
        return songs_activadas_lista
    except mysql.connector.Error as error:
        print("Error al obtener las canciones activadas:", error)
    finally:
        cursor.close()
        conn.close()
def usuario_admin(id_usuario):
    conn, cursor = conectar_base_datos()
    try:
        # Consultar la tabla UsuariosAdmin para verificar si el ID del usuario está presente
        cursor.execute('''SELECT 1 FROM UsuariosAdmin WHERE ID_Usuario = %s''', (id_usuario,))
        resultado = cursor.fetchone()  # Obtener el primer resultado de la consulta
        return resultado is not None  # Retornar True si se encontró un resultado, de lo contrario False
    except mysql.connector.Error as e:
        print("Error al verificar el estado de administrador:", e)
        return False  # En caso de error, retornar False
    finally:
        conn.close()  # Asegurarse de cerrar la conexión a la base de datos
        
def devolver_vidas(usuario_id=0):
    connection, cursor = conectar_base_datos()
    if connection:
        try:
            cursor.execute("""SELECT Num_Vidas FROM Elementos WHERE ID_Cliente = %s""", (usuario_id,))
            vidas = cursor.fetchone()
            if vidas:
                vidas =  vidas[0]
                if vidas == None:
                  return "0"
                return vidas
        except mysql.connector.Error as e:
            print("Error al obtener vidas:", e)
            return None
        finally:
            # Cerrar la conexión con la base de datos
            if connection:
                cursor.close()
                connection.close()
    return vidas

def devolver_cupones(usuario_id=0):
    connection, cursor = conectar_base_datos()
    if connection:
        try:
            cursor.execute("""SELECT Num_cupones FROM Elementos WHERE ID_Cliente = %s""", (usuario_id,))
            cupones = cursor.fetchone()
            print("debug")
            if cupones:
                cupones = cupones[0]
                if cupones == None:
                  return "0"
                else:
                  return str(cupones)
        except mysql.connector.Error as e:
            print("Error al obtener cupones:", e)
            return None
        finally:
            # Cerrar la conexión con la base de datos
            if connection:
                cursor.close()
                connection.close()
    return None


def devolver_saldo(usuario_id):
    connection, cursor = conectar_base_datos()
    saldo = 0
    if connection:
        try:
            cursor.execute("""SELECT Saldo FROM Wallet WHERE ID_Cliente = %s""", (usuario_id,))
            row = cursor.fetchone()
            if row:
                saldo = row[0]
                if saldo == None:
                  return "0"
                return saldo
        except mysql.connector.Error as e:
            print("Error al obtener saldo:", e)
        finally:
            # Cerrar la conexión con la base de datos
            if connection:
                cursor.close()
                connection.close()
    return saldo

def sumar_vidas(usuario_id, cantidad):
    saldo = int(devolver_saldo(usuario_id))
    precio_vidas = 30
    if not(saldo > precio_vidas * int(cantidad)):
      return "Saldo insuficiente"
    connection, cursor = conectar_base_datos()
    if connection:
        try:
            vidas_actuales = devolver_vidas(usuario_id)
            if vidas_actuales is not None:
                nuevas_vidas = int(vidas_actuales) + int(cantidad)
                cursor.execute("""UPDATE Elementos SET Num_Vidas = %s WHERE ID_Cliente = %s""", (nuevas_vidas, usuario_id))
                connection.commit()
        except mysql.connector.Error as e:
            print("Error al sumar vidas:", e)
        finally:
            # Cerrar la conexión con la base de datos
            if connection:
                cursor.close()
                connection.close()


def sumar_saldo(usuario_id, cantidad):
    connection, cursor = conectar_base_datos()
    if connection:
        try:
            saldo_actual = devolver_saldo(usuario_id)
            if saldo_actual is not None:
                nuevo_saldo = int(saldo_actual) + int(cantidad)
                cursor.execute("""UPDATE Wallet SET Saldo = %s WHERE ID_Cliente = %s""", (nuevo_saldo, usuario_id))
                connection.commit()
        except mysql.connector.Error as e:
            print("Error al sumar saldo:", e)
        finally:
            # Cerrar la conexión con la base de datos
            if connection:
                cursor.close()
                connection.close()

def sumar_cupones(usuario_id, cantidad):
    saldo = int(devolver_saldo(usuario_id))
    precio_cupones = 25
    if not(saldo > precio_cupones * int(cantidad)):
      return "Saldo insuficiente"
    connection, cursor = conectar_base_datos()
    if connection:
        try:
            cupones_actuales = devolver_cupones(usuario_id)
            if cupones_actuales is not None:
                nuevos_cupones = int(cupones_actuales) + int(cantidad)
                cursor.execute("""UPDATE Elementos SET Num_cupones = %s WHERE ID_Cliente = %s""", (nuevos_cupones, usuario_id))
                connection.commit()
        except mysql.connector.Error as e:
            print("Error al sumar cupones:", e)
        finally:
            # Cerrar la conexión con la base de datos
            if connection:
                cursor.close()
                connection.close()


def display_users(id=0):
    try:
        # Establecer conexión con la base de datos
        connection, cursor = conectar_base_datos()
        
        if id != 0:
          cursor.execute("SELECT Usuario.*, Wallet.Saldo, Elementos.Num_Vidas, Elementos.Num_cupones FROM Usuario LEFT JOIN Wallet ON Usuario.ID_Cliente = Wallet.ID_Cliente LEFT JOIN Elementos ON Usuario.ID_Cliente = Elementos.ID_Cliente WHERE Usuario.ID_Cliente = ?",(id))
        else:
          # Ejecutar una consulta para obtener la información de los usuarios con sus wallets y elementos asociados
          cursor.execute("SELECT Usuario.*, Wallet.Saldo, Elementos.Num_Vidas, Elementos.Num_cupones FROM Usuario LEFT JOIN Wallet ON Usuario.ID_Cliente = Wallet.ID_Cliente LEFT JOIN Elementos ON Usuario.ID_Cliente = Elementos.ID_Cliente")
        
        # Recuperar todos los registros de la consulta
        usuarios = cursor.fetchall()

        # Mostrar la información de los usuarios
        for usuario in usuarios:
            print("ID Cliente:", usuario[0])
            print("Nombre:", usuario[1])
            print("Email:", usuario[2])
            print("Contraseña:", usuario[3])
            print("Apellido Paterno:", usuario[4])
            print("Apellido Materno:", usuario[5])
            print("Ciudad:", usuario[6])
            print("Estado:", usuario[7])
            print("Teléfono:", usuario[8])
            print("Fecha de Registro:", usuario[9])
            print("Saldo en Wallet:", usuario[10])
            print("Número de Vidas:", usuario[11])
            print("Número de Cupones:", usuario[12])
            print("-----------------------------------")
  
    finally:
        # Cerrar la conexión con la base de datos
        if connection:
            cursor.close()
            connection.close()
            return usuarios

#def elmininar_tarjetas(usuario_id):
  #connection, cursor = conectar_base_datos()
   # if connection:
    #    try:
     #       cursor.execute("""DELETE * FROM Tarjetas WHERE ID_Cliente = %s""", (usuario_id,))
      #      except mysql.connector.Error as e:
      #      print("Error al obtener tarjetas:", e)
      #      return None
      #  finally:
            # Cerrar la conexión con la base de datos
      #      if connection:
       #         cursor.close()
        #        connection.close()
   # return None
  
          
          