import socket
import threading
import time
import json

HOST = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
players = {}

blocks = {}   # ID -> block
block_id = 0

chat = []
pid = 0

TICK = 0.1


def broadcast():
    while True:
        time.sleep(TICK)

        data = {
            "players": players,
            "blocks": list(blocks.values()),
            "chat": chat[-5:]
        }

        msg = json.dumps(data).encode()

        for c in list(clients.keys()):
            try:
                c.send(msg)
            except:
                pass


def handle(client, id):
    global block_id

    name = client.recv(1024).decode()
    players[id] = {"x":100,"y":100,"name":name}

    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)

            # MOVE
            if "x" in msg:
                players[id]["x"] = msg["x"]
            if "y" in msg:
                players[id]["y"] = msg["y"]

            # CHAT
            if "chat" in msg:
                chat.append({"name":name,"msg":msg["chat"]})

            # PLACE BLOCK (GRID SNAP)
            if msg.get("action") == "block":
                p = players[id]

                bx = round(p["x"]/40)*40
                by = round(p["y"]/40)*40 - 40

                # NIE DUPLIKUJ
                exists = False
                for b in blocks.values():
                    if b["x"] == bx and b["y"] == by:
                        exists = True
                        break

                if not exists:
                    blocks[block_id] = {
                        "id": block_id,
                        "x": bx,
                        "y": by
                    }
                    block_id += 1

            # BREAK BLOCK
            if msg.get("action") == "break":
                px = players[id]["x"]
                py = players[id]["y"]

                for bid in list(blocks.keys()):
                    b = blocks[bid]
                    if abs(b["x"]-px)<40 and abs(b["y"]-py)<40:
                        del blocks[bid]
                        break

        except:
            break

    clients.pop(client, None)
    players.pop(id, None)
    client.close()


threading.Thread(target=broadcast, daemon=True).start()

print("SERVER OK")

while True:
    client, addr = server.accept()
    clients[client] = pid

    threading.Thread(target=handle, args=(client,pid), daemon=True).start()
    pid += 1
