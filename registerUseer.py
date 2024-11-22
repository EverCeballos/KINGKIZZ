from users import registerUser, openCloseSession, updateScore, getScore, usersList,question
import random

def main():
    current_user = None
    current_password = None

    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        option = input("Selecciona una opción: ")

        if option == "1":
            name = input("Introduce el nombre de usuario: ")
            password = input("Introduce la contraseña: ")
            result = registerUser(name, password)
            print(result)

        elif option == "2":
            name = input("Introduce el nombre de usuario: ")
            password = input("Introduce la contraseña: ")
            session_result = openCloseSession(name, password, True)
            if session_result == "seccion iniciada":
                current_user = name
                current_password = password
                print(f"\n¡Bienvenido, {name}! {session_result}")

                while True:
                    print("\nOpciones disponibles:")
                    print("1. Actualizar puntaje")
                    print("2. Ver puntaje actual")
                    print("3. Ver usuarios conectados")
                    print("4. Obtener pregunta aleatoria")
                    print("5. Cerrar sesión")
                    print("6. Volver al menú principal")

                    logged_option = input("Selecciona una opción: ")

                    if logged_option == "1":
                        new_score = int(input("Introduce el nuevo puntaje: "))
                        result = updateScore(current_user, current_password, new_score)
                        print(result)

                    elif logged_option == "2":
                        score = getScore(current_user, current_password)
                        print("Tu puntaje es:", score)

                    elif logged_option == "3":
                        connected_users_info = usersList()  #Ver usuarios conectados
                        print(connected_users_info)

                    elif logged_option == '4':
                           question()
                    elif logged_option == "5":
                        session_result = openCloseSession(current_user, current_password, False)
                        current_user = None
                        current_password = None
                        print("Sesión cerrada.")
                        break  #Salir del menú de sesión

                    elif logged_option == "6":
                        break  #Volver al menú principal

                    else:
                        print("Opción inválida. Inténtalo de nuevo.")

            else:
                print(session_result)

        elif option == "3":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()