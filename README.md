# TCP Auction System 🔨

A concurrent client-server distributed application for real-time auctions, built with Python Sockets and containerized using Docker. 

## 📌 How It Works

This system simulates a live auction environment where multiple users can connect simultaneously, list items, and place bids. 

* **Connection:** Clients connect with a unique username. Upon successful connection, the server sends a list of all currently active auctions.
* **Publishing Items:** Any client can publish an item by setting a starting price. Once published, a 30-second countdown begins, and all connected users are notified.
* **Bidding:** Clients can place bids on active items. The server validates the bid (it must be higher than the current maximum price). Valid bids update the current price and trigger a live notification.
* **Expiration:** Auctions have a predefined, automated lifetime (30 seconds). Once the time expires, the server locks the item, prevents further bidding, and broadcasts the winner and the final price to all users.

## 💻 Available Commands
Once connected to the server, use the following commands directly in the terminal prompt (>):

  ```bash
  publish <item_name> <starting_price>
  ```
Puts a new item up for auction. The auction will last for 30 seconds.

Example: `publish Laptop 1500`

```bash
bid <item_name> <bid_amount>
```
Places a bid on an active item. The amount must be strictly greater than the current price.

Example: `bid Laptop 1600`


## ⚙️ Prerequisites
* **Server:** [Docker](https://www.docker.com/) or [Podman](https://podman.io/) installed on your machine.
* **Client:** Python 3.9+ installed locally.

---

## 🚀 Run Instructions

### 1. Start the Server (Docker/Podman)
Open your terminal in the project directory where the `Dockerfile` and `server.py` are located.

**Build the image:**
```bash
docker build -t server-licitatie .
```
*If using Podman, replace `docker` with `podman`*

**Run the container**
```bash
docker run -p 8719:8719 server-licitatie
```
*The server is now listening on port 8719 and ready to accept multiple client connections.*

### 2. Start the clients
Open a new terminal window for each user you want to simulate (minimum 3 recommended for a proper test).

**Run the client script**
```bash
python client.py
```
*You will be prompted to enter a unique username to join the server.*

