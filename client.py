import socket
import json

HOST = '192.168.0.11'
PORTA = 12000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORTA))

def func():
    while True: 
        chute = input("Envie o chute: ")
        while len(chute) != 5:
            chute = input("Input inválido, tente novamente: ")
    
        chute = chute.upper()

        client.send(chute.encode())
        resposta = client.recv(2048)
        resposta = json.loads(resposta.decode())
        printavel = resposta["palavra_print"]

        print(printavel)
        if resposta["ganhou"]:
            #ganhou
            print("Parabéns, você descobriu a palavra")
            return
        
        if resposta["restantes"] > 6:
            print("Chances excedidas")
            return
        
func()