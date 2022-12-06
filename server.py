import socket
import threading
import json

HOST = ''
PORTA = 12000
global PALAVRA_DIA

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', PORTA))

def printPalavra(chute, palavra):
    VERDE = '\033[32m'
    AMARELO = '\033[33m'
    TERMINAR = '\033[0;0m'

    verde = [False]*len(palavra)
    amarelo = [False]*len(palavra)
    
    for i in range(len(palavra)):
        letra = palavra[i]
        if chute[i] == letra:
            verde[i] = True
        else:
            for j in range(len(chute)):
                if chute[j] == letra and verde[j] == False and amarelo[j] == False:
                    amarelo[j] = True
                    break
    
    retorno = ''
    for i in range(len(chute)):
        if verde[i]:
            retorno += VERDE + chute[i] + TERMINAR
        elif amarelo[i]:
            retorno += AMARELO + chute[i] + TERMINAR
        else:
            retorno += chute[i]
    return retorno

def tratarDados(chance, data):
    mensagem_recebida = data.decode()
    palavra_print = printPalavra(mensagem_recebida, PALAVRA_DIA)
    ganhou = (mensagem_recebida == PALAVRA_DIA)
    json_enviado = {
        "ganhou": ganhou,
        "palavra_print": palavra_print,
        "restantes": chance 
    }
    return json.dumps(json_enviado)


def ouvirCliente(client, adress):
    print("Cliente conectado, endereco", adress)
    size = 1024
    chance = 1
    while chance <= 6:
        data = client.recv(size)
        chance += 1
        mensagem_volta = tratarDados(chance, data)
        client.send(mensagem_volta.encode())
        if data.decode() == PALAVRA_DIA:
            break
    client.close()


def ouvir():
    print("Server escutando")
    server.listen()
    while True:
        client, adress = server.accept()
        #client.timeout(60)
        nova_thread = threading.Thread(target=ouvirCliente, args=(client, adress))
        nova_thread.start()

def escolhePalavra():
    while(True):
        palavra_envio = input("Digite a palavra do dia (5 letras): ")
        if (len(palavra_envio) == 5):
            break
        else:
            print('A palavra precisa ter 5 letras.')
    return palavra_envio.upper()

if __name__ ==  "__main__":

    PALAVRA_DIA = escolhePalavra()
    ouvir()
