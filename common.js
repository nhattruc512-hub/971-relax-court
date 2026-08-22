const CFG=window.R971;
const $=id=>document.getElementById(id);
const money=n=>new Intl.NumberFormat('vi-VN').format(Number(n||0))+'đ';
if(location.pathname.endsWith('/staff.html')||location.pathname.endsWith('staff.html')) localStorage.setItem('r971pin','1234');
function toast(s){const e=document.createElement('div');e.className='toast';e.textContent=s;document.body.appendChild(e);setTimeout(()=>e.remove(),2500)}
async function api(method,body=null,query=''){
  const r=await fetch(CFG.API_URL+query,{method,headers:{'Content-Type':'application/json','Authorization':'Bearer '+CFG.ANON_KEY,'apikey':CFG.ANON_KEY},body:body?JSON.stringify(body):undefined});
  const d=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(d.error||'Không kết nối được máy chủ');
  return d;
}
