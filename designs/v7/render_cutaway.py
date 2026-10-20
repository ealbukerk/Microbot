from pathlib import Path
import json,math,numpy as np
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent;mesh=json.loads((p/'model_mesh.json').read_text());W,H=1000,850;yaw=-.65;pitch=.7;sc=19
P=np.array([[math.cos(yaw),-math.sin(yaw),0],[math.sin(yaw)*math.sin(pitch),math.cos(yaw)*math.sin(pitch),-math.cos(pitch)],[math.sin(yaw)*math.cos(pitch),math.cos(yaw)*math.cos(pitch),math.sin(pitch)]])
def project(a):
 q=np.array(a)@P.T;q[...,0]=q[...,0]*sc+500;q[...,1]=q[...,1]*sc+430;return q
light=np.array([-.3,-.5,.8]);light/=np.linalg.norm(light);polys=[]
for m in mesh:
 if m['category']=='cover':continue
 v=np.array(m['v']);f=np.array(m['f']);tri=v[f];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-15);keep=norm@P[2]>0;tri=tri[keep];norm=norm[keep];q=project(tri);c=(.13+.87*np.array(m['color']))*(.65+.35*np.maximum(0,norm@light))[:,None];rgb=np.clip(c*255,0,255).astype(np.uint8)
 for t,col,z in zip(q[:,:,:2],rgb,q[:,:,2].mean(axis=1)):polys.append((z,t,col))
im=Image.new('RGB',(W,H),'#102035');d=ImageDraw.Draw(im)
for z,t,c in sorted(polys,key=lambda x:x[0]):d.polygon([tuple(a) for a in t],fill=tuple(c),outline=tuple(c))
def ui_font(size):
 for candidate in ['/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
  try:return ImageFont.truetype(candidate,size)
  except OSError:pass
 return ImageFont.load_default()
big=ui_font(26);small=ui_font(18)
d.text((24,20),'One bot: actual-size component envelopes',font=big,fill='#f0f5fc');d.text((24,59),'Ø23.6 sphere cover hidden | 20 mm board | 235 modeled parts',font=small,fill='#c1d8ec')
for txt,point,xy in [('2 rotary gear drives + direct slide motor',[-3,0,4.9],(25,150)),('20 mm circular board',[0,-5,1.7],(25,690)),('Cylindrical 1 F reserve cell',[0,0,-2],(650,720)),('Separate pyramid docking pods',[12,6,6],(650,150))]:
 a=project(point);b=[xy[0]+60,xy[1]+25];d.line([tuple(a[:2]),tuple(b)],fill='#ffda95',width=2);d.text(xy,txt,font=small,fill='#ffda95')
d.text((24,805),'Package fit only. Complete latches, actuator routing, wiring, sensing and PCB copper remain unfinished.',font=small,fill='#ffc98a');im.save(p/'Cutaway.png')
