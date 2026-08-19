import json, socket, time, urllib.request, urllib.error, unicodedata

API_URL = "https://dinqlgaveujdeyisgpty.supabase.co/functions/v1/r971-api"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpbnFsZ2F2ZXVqZGV5aXNncHR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcxMjQxNzAsImV4cCI6MjEwMjcwMDE3MH0.L5aitJLmaGC4yopIzjwkQomwQ0H9dSOfNWqvAgwrzQI"
BRIDGE_KEY = "R971-BRIDGE-2026-8c9a4f5d7e31"
PRINTER_IP = "192.168.1.199"
PRINTER_PORT = 9100
POLL_SECONDS = 2


def api(payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "apikey": ANON_KEY,
        "Authorization": "Bearer " + ANON_KEY,
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def ascii_text(s):
    s = str(s or "")
    s = s.replace("đ", "d").replace("Đ", "D")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def money(n):
    try: return f"{int(n):,}".replace(",", ".") + "d"
    except: return "0d"


def line_lr(left, right, width=48):
    left, right = ascii_text(left), ascii_text(right)
    if len(left) + len(right) + 1 > width:
        left = left[:max(1, width-len(right)-1)]
    return left + " " * max(1, width-len(left)-len(right)) + right + "\n"


def bill_bytes(job):
    p = job.get("payload") or {}
    ESC=b"\x1b"; GS=b"\x1d"
    out = bytearray()
    out += ESC+b"@"
    out += ESC+b"a\x01" + ESC+b"!\x20"
    out += b"971 RELAX COURT\n"
    out += ESC+b"!\x00" + b"Order & Drink Service\n"
    out += b"-----------------------------------------------\n"
    if job.get("job_type") == "test":
        out += ESC+b"!\x10" + b"TEST PRINT OK\n" + ESC+b"!\x00"
        out += f"Printer: {PRINTER_IP}:{PRINTER_PORT}\n".encode()
        out += b"KPOS Zy307 - ESC/POS\n"
    else:
        out += ESC+b"a\x00"
        out += ascii_text(f"Ma don: {p.get('order_code','')}\n").encode()
        out += ascii_text(f"San: {p.get('court','')}\n").encode()
        created = str(p.get('created_at','')).replace('T',' ')[:19]
        out += ascii_text(f"Thoi gian: {created}\n").encode()
        if p.get('customer_name'): out += ascii_text(f"Khach: {p['customer_name']}\n").encode()
        out += b"-----------------------------------------------\n"
        for it in (p.get("items") or []):
            qty = int(it.get("qty",1)); name = it.get("name",""); sub = it.get("subtotal", int(it.get("price",0))*qty)
            out += line_lr(f"{qty} x {name}", money(sub)).encode()
        out += b"-----------------------------------------------\n"
        out += ESC+b"!\x10" + line_lr("TONG CONG", money(p.get("total",0))).encode() + ESC+b"!\x00"
        pm = "TIEN MAT" if p.get("payment_method") == "cash" else "CHUYEN KHOAN/QR"
        out += ascii_text(f"Thanh toan: {pm}\n").encode()
        if p.get('customer_note'):
            out += b"-----------------------------------------------\n"
            out += ascii_text(f"Ghi chu: {p['customer_note']}\n").encode()
    out += ESC+b"a\x01" + b"\nCAM ON QUY KHACH!\n\n\n"
    out += GS+b"V\x00"
    return bytes(out)


def send_to_printer(data):
    with socket.create_connection((PRINTER_IP, PRINTER_PORT), timeout=5) as s:
        s.sendall(data)


def ping(last_error=None):
    try:
        api({"action":"bridge_ping","bridge_key":BRIDGE_KEY,"printer_ip":PRINTER_IP,"printer_port":PRINTER_PORT,"last_error":last_error})
    except Exception as e:
        print("Heartbeat error:", e)


def main():
    print("971 RELAX COURT - PRINT BRIDGE")
    print(f"Printer: {PRINTER_IP}:{PRINTER_PORT}")
    print("Keep this window open while staff are working.\n")
    last_ping = 0
    while True:
        try:
            if time.time()-last_ping > 5:
                ping(); last_ping=time.time()
            d = api({"action":"bridge_next","bridge_key":BRIDGE_KEY})
            job = d.get("job")
            if not job:
                time.sleep(POLL_SECONDS); continue
            print("Printing job", job.get("id"), job.get("job_type"))
            try:
                send_to_printer(bill_bytes(job))
                api({"action":"bridge_done","bridge_key":BRIDGE_KEY,"job_id":job["id"],"ok":True})
                print("Printed OK")
            except Exception as e:
                msg=str(e)
                api({"action":"bridge_done","bridge_key":BRIDGE_KEY,"job_id":job["id"],"ok":False,"error":msg})
                ping(msg)
                print("Print failed:", msg)
        except KeyboardInterrupt:
            print("Stopped"); break
        except Exception as e:
            print("Bridge error:", e); time.sleep(3)

if __name__ == "__main__": main()
