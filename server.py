import socket
import threading
import json

HOST = '0.0.0.0' #asculta pe toate conexiunile, adica inafara containerului docker
PORT = 8719
AUCTION_TIME = 30.0

clients = {}
products = {}
lock = threading.RLock()

def broadcast(msg):
    data = msg + "\n"
    with lock:
        for c in clients.values():
            try:
                c.sendall(data.encode('utf-8'))
            except:
                pass

def expire_product(name):
    with lock:
        if name in products and products[name]['active']:
            products[name]['active'] = False
            p = products[name]
            broadcast(f"Licitatia pt '{name}' a expirat! Castigator: {p['highest_bidder']} (Pret: {p['current_price']})")

def handle_client(conn):
    name = None
    try:
        data = conn.recv(1024).decode('utf-8')
        if not data: return
        
        name = data.strip()
        with lock:
            if name in clients:
                conn.sendall(b"Eroare: Numele exista deja!\n")
                return
            clients[name] = conn
        
        conn.sendall(b"Te-ai conectat cu succes!\n")
        
        with lock:
            for p_name, p_data in products.items():
                if p_data['active']:
                    msg = f"Produs activ: {p_name}, Pret curent: {p_data['current_price']}\n"
                    conn.sendall(msg.encode('utf-8'))
        
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data: break
            
            req = json.loads(data)
            cmd = req.get("cmd")
            
            if cmd == "publish":
                p_name = req["item"]
                price = float(req["price"])
                
                with lock:
                    if p_name in products:
                        conn.sendall(b"Eroare: Produsul exista deja!\n")
                        continue
                    products[p_name] = {
                        'owner': name, 
                        'current_price': price, 
                        'highest_bidder': "Nimeni", 
                        'active': True
                    }
                    
                broadcast(f"NOU! {name} vinde '{p_name}' cu {price} lei.")
                threading.Timer(AUCTION_TIME, expire_product, args=(p_name,)).start()
                
            elif cmd == "bid":
                p_name = req["item"]
                price = float(req["price"])
                
                with lock:
                    if p_name not in products:
                        conn.sendall(b"Eroare: Produs inexistent!\n")
                        continue
                        
                    p = products[p_name]
                    if not p['active']:
                        conn.sendall(b"Eroare: Licitatia a expirat!\n")
                        continue
                        
                    if price <= p['current_price']:
                        conn.sendall(f"Eroare: Pretul minim este {p['current_price'] + 1}\n".encode('utf-8'))
                        continue
                        
                    p['current_price'] = price
                    p['highest_bidder'] = name
                    
                broadcast(f"OFERTA! {name} da {price} lei pt '{p_name}'.")

    except Exception as e:
        pass
    finally:
        if name and name in clients:
            with lock:
                del clients[name]
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server pornit pe portul {PORT}...")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()
