import socket
import threading
import json
import sys

HOST = '127.0.0.1' #localhost
PORT = 8719

def asculta_server(sock):
    # Primeste si afiseaza tot ce vine de la server
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data: break
            # Afisam linia fara spatii in plus
            print(f"\n[SERVER] {data.strip()}\n> ", end="")
        except:
            break
    print("\nDeconectat.")
    sys.exit(0)

def main():
    nume = input("Introdu numele tau: ")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except:
        print("Eroare: Serverul nu este pornit!")
        return
        
    # Trimitem numele simplu ca prim mesaj
    sock.sendall(nume.encode('utf-8'))
    
    # Pornim thread-ul care citeste de la server
    threading.Thread(target=asculta_server, args=(sock,), daemon=True).start()
    
    print("Comenzi disponibile:")
    print("  publish <produs> <pret>")
    print("  bid <produs> <pret>")
    
    while True:
        try:
            text = input("> ").strip().split()
            if not text: continue
            
            comanda = text[0].lower()
            if comanda == "publish" and len(text) == 3:
                msg = {"cmd": "publish", "item": text[1], "price": text[2]}
                sock.sendall(json.dumps(msg).encode('utf-8'))
            elif comanda == "bid" and len(text) == 3:
                msg = {"cmd": "bid", "item": text[1], "price": text[2]}
                sock.sendall(json.dumps(msg).encode('utf-8'))
            else:
                print("Comanda gresita. Foloseste publish sau bid.")
        except KeyboardInterrupt:
            break
            
    sock.close()

if __name__ == "__main__":
    main()
