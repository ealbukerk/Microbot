"""Package/courtyard placement, not an electrically routed board."""
from pathlib import Path
import json,math,csv
p=Path(__file__).parent;R=10;clear=.25;items=[]
def put(ref,name,w,h,t,x,y,side='front',status='supplier body envelope; land pattern / routing unverified'):
 items.append(dict(ref=ref,name=name,w=w,h=h,t=t,x=x,y=y,side=side,status=status))
put('U1','STM32G431CBU6',7,7,.55,0,0)
put('U2','BQ51013B RHL',4.5,3.5,1,0,6.0)
put('U3','TPS63031 DSK',2.5,2.5,.8,5.3,.5)
put('L1','2.2 uH power inductor reservation',2.5,2.5,1,5.3,3.8,status='value/package target; exact order code and saturation need selection')
put('U4','BQ25173 DSG',2,2,.8,-5,1)
put('U5','LM66100 DCK',2.1,2,1.1,-5,-2)
put('U6','LM66100 DCK',2.1,2,1.1,-5,-5)
put('U7','TPS62840 DLCR',1.5,2,.8,0,-5,status='750 mA motor buck candidate; circuit not routed')
put('L2','2.2 uH motor inductor reservation',2.5,2.5,1,3.3,-5,status='current/inductance target; exact order code unselected')
put('U8','Motor isolation switch reservation',1.5,1.5,.8,6,-3,status='current-limit cutoff implementation not selected')
for i,x in enumerate([-3.5,0,3.5]):put('U'+str(9+i),'DRV8311P RRW',3,3,.8,x,5.5,'back')
for j,x in enumerate([-3,3]):put('U'+str(12+j),'SN74AXC8T245 RJW',4,2,.6,x,-6,'back',status='Ioff / supply isolation candidate; pin routing and OE sequence unverified')
# Place 0402 bypass / divider / tuning / pullup reservations with honest values.
for k in range(56):
 found=False
 for y in [q*.75 for q in range(-12,13)]:
  for x in [q*.75 for q in range(-12,13)]:
   w,h=1,.5
   if max(math.hypot(x+a*w/2,y+b*h/2) for a in [-1,1] for b in [-1,1])>R-.3:continue
   if any(abs(x-i['x'])<(w+i['w'])/2+clear and abs(y-i['y'])<(h+i['h'])/2+clear for i in items if i['side']=='front'):continue
   put('P'+str(k+1),'0402 passive allocation',w,h,.5,x,y,status='role/value/order code not all frozen; NOT a validated netlist');found=True;break
  if found:break
 if not found:raise RuntimeError('board cannot pack required allocations')
errors=[]
for i,a in enumerate(items):
 if max(math.hypot(a['x']+sg*a['w']/2,a['y']+tg*a['h']/2) for sg in [-1,1] for tg in [-1,1])>R-.3:errors.append([a['ref'],'edge'])
 for b in items[i+1:]:
  if a['side']==b['side'] and abs(a['x']-b['x'])<(a['w']+b['w'])/2+clear-1e-8 and abs(a['y']-b['y'])<(a['h']+b['h'])/2+clear-1e-8:errors.append([a['ref'],b['ref']])
(p/'board_placement.json').write_text(json.dumps(items,indent=2));(p/'board_check.json').write_text(json.dumps(dict(diameter_mm=20,thickness_mm=.6,layers=4,package_count=len(items),body_clearance_mm=clear,edge_margin_mm=.3,placement_errors=errors,package_placement_pass=not errors,routed=False,pin_netlist_validated=False,ERC_run=False,DRC_run=False,fabrication_ready=False),indent=2))
with (p/'board_placement.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=items[0]);w.writeheader();w.writerows(items)
print('Placed',len(items),'packages; errors',errors)
