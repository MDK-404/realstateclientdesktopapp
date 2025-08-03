import qrcode
import os
import json

def generate_qr(client_id):
    # Load database
    with open("database.json", "r") as f:
        db = json.load(f)

    # Find client by ID
    client = next((c for c in db["clients"] if c["id"] == client_id), None)
    
    if not client:
        print(f"[QR] ❌ Client ID '{client_id}' not found in database.")
        return

    pin = client.get("pin", "0000")  # fallback if pin missing
    url = f"client_login://{client_id}?pin={pin}"

    img = qrcode.make(url)
    path = f"assets/qrcodes/{client_id}.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

    print(f"[QR] ✅ QR with PIN saved to: {path}")
