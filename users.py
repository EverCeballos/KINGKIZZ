import random
# Conjunto para llevar un registro de usuarios conectados
connected_users = set()

# Función para registrar un nuevo usuario
def registerUser(name, password):
    name = name.strip().lower()  
    password = password.strip()

    try:
        with open("usuarios.txt", "r") as file:#Se intenta abrir el archivo usuarios.txt en modo lectura r. Si el archivo no existe, se lanzara una excepcion para mas adelante
            for line in file:#Se itera sobre cada linea del archivo abierto.
                if line:  #verifica si la linea esta vacia
                    parts = line.split(",")  #Se divide la línea en partes utilizando la coma paramseparar
                    user = parts[0].strip().lower()  #se pasa el name a minusculas
                    if user == name:  
                        return "ya registrado"
    except FileNotFoundError:
        
        open("usuarios.txt", "w").close()

    with open("usuarios.txt", "a") as file:#abre el archivo txt
        file.write(f"{name},{password},0,no_conectado\n") 
    return "registrado"

def openCloseSession(name, password, flag):
    name = name.strip().lower()
    password = password.strip()
    lines = []#para actualizar las lineas del archivo
    user_found = False# se inicia asi para verificar si el usuario esta en el txt

    with open("usuarios.txt", "r") as file:
        for line in file:
            if line:  
                try:
                    user, passw, user_score, status = line.split(",")#se divide en comas el user,passw,etc
                    if user == name and passw == password:#verifica que si el usuario y la contraseña digitada esta en el txt
                        user_found = True#si se encontro
                       
                        status = "conectado" if flag else "desconetado"#se actualiza el estado a true que es conenctado,si no lo es pasa lo contrario
                    lines.append(f"{user},{passw},{user_score},{status}") #agrega el nuevo estado conectado
                except ValueError:
                    continue  

    if user_found:#procede a actualzair el archivo
        with open("usuarios.txt", "w") as file:#sobreescribe lo que ya existia 
            file.write("\n".join(lines) + "\n")#se escribe en el archivo el contenido de lines 
        return "seccion iniciada" if flag else "Sseccion cerrada"
    
    return "eror de contrasa o usuario"
  
def updateScore(name, password, new_score):
    name = name.strip().lower()
    password = password.strip()
    updated = False
    lines = []#almacena cualquier linea del archivo

    with open("usuarios.txt", "r") as file:
        for line in file:
            if line:  
                try:
                    user, passw, user_score, status = line.split(",")
                    if user.lower() == name and passw == password:
                        user_score = new_score  #se asigna el nuevo dato 
                        updated = True# si fue actualziadao
                    lines.append(f"{user},{passw},{user_score},{status}")#se agrega ala actualizacion a line
                except ValueError:
                    continue 

    if updated:
        with open("usuarios.txt", "w") as file:#sobreescribe el dato"w"
            file.write("\n".join(lines) + "\n")
        return "Actualizado"
    
    return "eror de contra o usuario"

def getScore(name, password):
    name = name.strip().lower()
    password = password.strip()

    with open("usuarios.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:  
                try:
                    user, passw, user_score, status = line.split(",")
                    if user == name and passw == password:
                        return user_score
                except ValueError:
                    continue  
    return "error de contra o usuario"

def usersList(name=None, password=None):
    connected_users = []# guarda el nombre  delos usuarios

    try:
        with open("usuarios.txt", "r") as file:
            for line in file:
                if line:  
                    try:
                        parts = line.split(",") 
                        #Se Comprueba que hay 4 datos de largo(longuitud),se comprueba que el 4 dato es igual conectado
                        if len(parts) >= 4 and parts[3].strip().lower() == "conectado": 
                            connected_users.append(parts[0].strip())  
                    except IndexError:
                        continue  
    except FileNotFoundError:
        return "usuaruio no registrado"

    if connected_users:
        return f"Usuarios conectados: {', '.join(connected_users)}"
    else:
        return "No hay usuarios conectados."
    
  #corregir question  
 #reciba argumentos de nombre, contraseña, categoria
def question(name, password, cat):
    name = name.strip().lower()
    password = password.strip()

    # Mapeo de nombres de categoría a índices
    categories = {
        "Deportes": 0,
        "Música": 1,
        "Cultura General": 2,
        "Cine y Peliculas": 3,
        "Historia": 4,
        "Videojuegos": 5
    }

    # Si `cat` es un texto, mapearlo a su índice correspondiente
    if isinstance(cat, str) and cat in categories:
        cat = categories[cat]
    else:
        try:
            cat = int(cat)
        except ValueError:
            return "Error: Categoría inválida."

    # Validar usuario y estado
    with open("usuarios.txt", "r") as file:
        user_found = False
        user_connected = False
        for line in file:
            if line:
                try:
                    user, passw, _, status = line.split(",")
                    if user == name and passw.strip() == password:
                        user_found = True
                        if status.strip() == "conectado":
                            user_connected = True
                        break
                except ValueError:
                    continue

    if not user_found:
        return "Error: Usuario no registrado o contraseña incorrecta."
    if not user_connected:
        return "Error: Usuario no tiene sesión activa."

    # Determinar el archivo de preguntas basado en la categoría
    match cat:
        case 0: file_name = "preguntas0.txt"  # Deportes
        case 1: file_name = "preguntas1.txt"  # Música
        case 2: file_name = "preguntas2.txt"  # Cultura General
        case 3: file_name = "preguntas3.txt"  # Cine y Películas
        case 4: file_name = "preguntas4.txt"  # Historia
        case 5: file_name = "preguntas5.txt"  # Videojuegos
        case _: return "Error: Categoría inválida."

    # Leer preguntas de la categoría y devolver una aleatoria
    try:
        with open(file_name, "r") as file:
            questions = file.readlines()
            if questions:
                selected_question = random.choice(questions).strip()
                return selected_question
            else:
                return "Error: No hay preguntas disponibles en esta categoría."
    except FileNotFoundError:
        return "Error: Archivo de preguntas no encontrado."
