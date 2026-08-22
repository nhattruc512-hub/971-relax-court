const CFG=window.R971;
const $=id=>document.getElementById(id);
const money=n=>new Intl.NumberFormat('vi-VN').format(Number(n||0))+'đ';
const PUSH_URL='https://dinqlgaveujdeyisgpty.supabase.co/functions/v1/r971-push';
function toast(s){const e=document.createElement('div');e.className='toast';e.textContent=s;document.body.appendChild(e);setTimeout(()=>e.remove(),2500)}
async function pushApi(method,body=null,query=''){
  const r=await fetch(PUSH_URL+query,{method,headers:{'Content-Type':'application/json','Authorization':'Bearer '+CFG.ANON_KEY,'apikey':CFG.ANON_KEY},body:body?JSON.stringify(body):undefined});
  const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error(d.error||'Không kết nối được thông báo');return d;
}
function b64ToBytes(s){const p='='.repeat((4-s.length%4)%4),b=(s+p).replace(/-/g,'+').replace(/_/g,'/'),raw=atob(b);return Uint8Array.from([...raw].map(c=>c.charCodeAt(0)))}
async function enableOrderPushNotifications(showToast=true){
  if(!('serviceWorker'in navigator)||!('PushManager'in window)||!('Notification'in window)){if(showToast)toast('Thiết bị này chưa hỗ trợ thông báo nền');return false}
  const ios=/iphone|ipad|ipod/i.test(navigator.userAgent),standalone=window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  if(ios&&!standalone){if(showToast)toast('iPhone: hãy cài app vào Màn hình chính rồi bật thông báo trong app');return false}
  let perm=Notification.permission;if(perm!=='granted')perm=await Notification.requestPermission();if(perm!=='granted'){if(showToast)toast('Bạn chưa cho phép thông báo');return false}
  const reg=await navigator.serviceWorker.ready;const k=await pushApi('GET',null,'?action=key');let sub=await reg.pushManager.getSubscription();if(!sub)sub=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:b64ToBytes(k.publicKey)});
  await pushApi('POST',{action:'subscribe',subscription:sub.toJSON(),user_agent:navigator.userAgent});if(showToast)toast('✅ Đã bật thông báo nhận đơn trên điện thoại');return true;
}
async function api(method,body=null,query=''){
  const r=await fetch(CFG.API_URL+query,{method,headers:{'Content-Type':'application/json','Authorization':'Bearer '+CFG.ANON_KEY,'apikey':CFG.ANON_KEY},body:body?JSON.stringify(body):undefined});
  const d=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(d.error||'Không kết nối được máy chủ');
  if(method==='POST'&&body&&body.action==='order'&&d.order_code){pushApi('POST',{action:'notify_order',order_code:d.order_code}).catch(()=>{})}
  return d;
}
if('serviceWorker'in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('./sw.js').then(()=>{if(Notification.permission==='granted')enableOrderPushNotifications(false).catch(()=>{})}).catch(()=>{})});document.addEventListener('click',e=>{const el=e.target.closest('button');if(el&&String(el.getAttribute('onclick')||'').includes('enableNoti'))enableOrderPushNotifications(true).catch(err=>toast(err.message))},true)}
