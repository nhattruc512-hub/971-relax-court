import json, socket, time, urllib.request, urllib.error, os, sys

API_URL = "https://dinqlgaveujdeyisgpty.supabase.co/functions/v1/r971-api"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpbnFsZ2F2ZXVqZGV5aXNncHR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcxMjQxNzAsImV4cCI6MjEwMjcwMDE3MH0.L5aitJLmaGC4yopIzjwkQomwQ0H9dSOfNWqvAgwrzQI"
BRIDGE_KEY = "R971-BRIDGE-2026-8c9a4f5d7e31"
PRINTER_IP = "192.168.1.199"
PRINTER_PORT = 9100
POLL_SECONDS = 2

def api(payload):
    body=json.dumps(payload).encode('utf-8')
    req=urllib.request.Request(API_URL,data=body,headers={'Content-Type':'application/json','Authorization':'Bearer '+ANON_KEY,'apikey':ANON_KEY},method='POST')
    with urllib.request.urlopen(req,timeout=15) as r:
        return json.loads(r.read().decode('utf-8'))

def vn_ascii(s):
    table=str.maketrans('àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ','aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiioooooooooooooooooouuuuuuuuuuuyyyyydAAAAAAAAAAAAAAAAAEEEEEEEEEEEIIIIIOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYD')
    return str(s or '').translate(table)

def line(left='',right='',width=42):
    left=vn_ascii(left);right=vn_ascii(right)
    if len(left)+len(right)+1>width: return left[:width]+'\n'+right.rjust(width)+'\n'
    return left+(' '*(width-len(left)-len(right)))+right+'\n'

def receipt(payload):
    ESC=b'\x1b'; GS=b'\x1d'; out=bytearray()
    out += ESC+b'@' + ESC+b'a'+b'\x01' + ESC+b'E'+b'\x01'
    out += b'971 RELAX COURT\n'; out += ESC+b'E'+b'\x00'
    if payload.get('job_type')=='test' or payload.get('title'):
        out += b'\nIN THU KPOS Zy307\n192.168.1.199:9100\n\n'
    else:
        out += (vn_ascii('DON HANG '+str(payload.get('order_code','')))+'\n').encode()
        out += ESC+b'a'+b'\x00'
        out += ('-'*42+'\n').encode()
        out += line('San:',payload.get('court','')).encode()
        out += line('Khach:',payload.get('customer_name','')).encode()
        created=str(payload.get('created_at',''))
        if created: out += line('Thoi gian:',created[:19].replace('T',' ')).encode()
        out += ('-'*42+'\n').encode()
        for x in payload.get('items',[]):
            name=vn_ascii(x.get('name','')); qty=int(x.get('qty',0)); subtotal=int(x.get('subtotal',int(x.get('price',0))*qty))
            out += line(f'{qty}x {name}',f'{subtotal:,}d'.replace(',','.')).encode()
        out += ('-'*42+'\n').encode()
        out += ESC+b'E'+b'\x01' + line('TONG:',f"{int(payload.get('total',0)):,}d".replace(',','.')).encode() + ESC+b'E'+b'\x00'
        pay='TIEN MAT' if payload.get('payment_method')=='cash' else 'CHUYEN KHOAN/QR'
        out += line('Thanh toan:',pay).encode()
        note=payload.get('customer_note')
        if note: out += ('\nGhi chu: '+vn_ascii(note)+'\n').encode()
        out += b'\nCam on quy khach!\n'
    out += b'\n\n\n' + GS+b'V'+b'\x00'
    return bytes(out)

def print_raw(data):
    with socket.create_connection((PRINTER_IP,PRINTER_PORT),timeout=5) as s:
        s.sendall(data)

def ping(err=None):
    try: api({'action':'bridge_ping','bridge_key':BRIDGE_KEY,'printer_ip':PRINTER_IP,'printer_port':PRINTER_PORT,'last_error':err})
    except: pass

def main():
    print('971 RELAX COURT - AUTO PRINT')
    print('May in: %s:%s' % (PRINTER_IP,PRINTER_PORT))
    print('Dang cho don moi... KHONG DONG CUA SO NAY.')
    last_ping=0
    while True:
        try:
            if time.time()-last_ping>8: ping(); last_ping=time.time()
            d=api({'action':'bridge_next','bridge_key':BRIDGE_KEY})
            job=d.get('job')
            if not job: time.sleep(POLL_SECONDS); continue
            jid=job['id']; p=job.get('payload') or {}; p['job_type']=job.get('job_type')
            try:
                print_raw(receipt(p)); api({'action':'bridge_done','bridge_key':BRIDGE_KEY,'job_id':jid,'ok':True}); print('Da in:',p.get('order_code',jid))
            except Exception as e:
                api({'action':'bridge_done','bridge_key':BRIDGE_KEY,'job_id':jid,'ok':False,'error':str(e)}); ping(str(e)); print('LOI MAY IN:',e)
        except Exception as e:
            print('LOI KET NOI:',e); ping(str(e)); time.sleep(5)

if __name__=='__main__': main()
