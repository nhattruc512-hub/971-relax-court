(()=>{
  function addPrintButtons(){
    document.querySelectorAll('#orders .order').forEach(card=>{
      if(card.querySelector('.ipad-print-btn')) return;
      const cancelled = card.textContent.includes('ĐÃ HỦY');
      const btn=document.createElement('button');
      btn.className='primary ipad-print-btn';
      btn.style.cssText='margin-top:10px;width:100%;font-size:15px';
      btn.textContent=cancelled?'🖨️ IN BILL ĐƠN ĐÃ HỦY':'🖨️ IN BILL';
      btn.onclick=()=>printCard(card);
      card.appendChild(btn);
    });
  }

  function cleanClone(card){
    const c=card.cloneNode(true);
    c.querySelectorAll('button,a').forEach(x=>x.remove());
    c.querySelectorAll('.card').forEach(x=>{x.style.boxShadow='none';x.style.border='0';x.style.padding='0';x.style.margin='5px 0'});
    return c;
  }

  function printCard(card){
    const content=cleanClone(card).innerHTML;
    const w=window.open('','_blank');
    if(!w){alert('Safari đang chặn cửa sổ in. Hãy cho phép pop-up cho trang này.');return;}
    w.document.write(`<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bill 971 Relax Court</title><style>
      @page{size:80mm auto;margin:3mm}
      html,body{margin:0;padding:0;background:#fff;color:#000;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
      body{width:74mm;margin:0 auto;font-size:13px;line-height:1.35}
      .head{text-align:center;border-bottom:1px dashed #000;padding:4mm 0 2mm;margin-bottom:2mm}
      .head b{font-size:19px}.sub{font-size:11px;margin-top:2px}
      .bill{border-bottom:1px dashed #000;padding-bottom:3mm;margin-bottom:2mm}
      .top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}.muted{font-size:11px;color:#000!important}
      .pill{font-size:10px;border:1px solid #000;border-radius:3px;padding:1px 3px}.cash,.transfer{background:#fff!important;color:#000!important}
      .card{border:0!important;background:#fff!important;box-shadow:none!important;padding:0!important;margin:5px 0!important;opacity:1!important}
      .foot{text-align:center;padding:3mm 0 2mm;font-size:12px}.amount{font-size:16px;font-weight:800}
      @media screen{body{padding:10px}.printbar{position:sticky;top:0;background:#fff;padding:8px 0 12px;text-align:center}.printbar button{font-size:16px;padding:11px 18px;border:0;border-radius:10px;background:#0a7f47;color:#fff;font-weight:700}}
      @media print{.printbar{display:none}}
    </style></head><body><div class="printbar"><button onclick="window.print()">🖨️ IN BILL</button><div style="font-size:11px;margin-top:5px">Trên iPad chọn máy in KPOS/AirPrint nếu máy xuất hiện</div></div><div class="head"><b>971 RELAX COURT</b><div class="sub">PHIẾU GỌI MÓN</div></div><div class="bill">${content}</div><div class="foot">CẢM ƠN QUÝ KHÁCH!</div><script>setTimeout(()=>window.print(),350)<\/script></body></html>`);
    w.document.close();
  }

  window.addEventListener('load',()=>{
    addPrintButtons();
    const target=document.getElementById('orders');
    if(target)new MutationObserver(addPrintButtons).observe(target,{childList:true,subtree:true});
  });
})();
