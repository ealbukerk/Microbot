"""Render the numeric CAD mesh animation offline; no browser control involved."""
from pathlib import Path
import json,math,subprocess,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent;data=json.loads((p/'assembly.json').read_text());mesh=json.loads((p/'model_mesh.json').read_text());verts=[];faces=[];colors=[]
for m in mesh:
 if m['category'] not in ['cover','dock','structure']:continue
 offset=len(verts);verts.extend(m['v']);faces.extend([[j+offset for j in f] for f in m['f']]);colors.extend([m['color']]*len(m['f']))
v=np.array(verts);f=np.array(faces);colors=np.array(colors);W,H=1000,800;scale=4.5;yaw=-.65;pitch=.7
P=np.array([[math.cos(yaw),-math.sin(yaw),0],[math.sin(yaw)*math.sin(pitch),math.cos(yaw)*math.sin(pitch),-math.cos(pitch)],[math.sin(yaw)*math.cos(pitch),math.cos(yaw)*math.cos(pitch),math.sin(pitch)]])
cam=P[2];light=np.array([-.3,-.5,.8]);light/=np.linalg.norm(light)
def ui_font(size):
 for candidate in ['/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
  try:return ImageFont.truetype(candidate,size)
  except OSError:pass
 return ImageFont.load_default()
big=ui_font(26);small=ui_font(17);label=ui_font(13)
def project(a):
 q=(np.array(a)-[0,-5,25])@P.T;q[...,0]=q[...,0]*scale+W/2;q[...,1]=q[...,1]*scale+H*.57;return q
ff=subprocess.Popen([shutil.which('ffmpeg'),'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','20','-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(p/'SixSecondAssembly.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
gifs=[]
for frameindex in range(120):
 time=frameindex/119*6;fr=max((z for z in data['frames'] if z['time_s']<=time),key=lambda z:z['time_s']);im=Image.new('RGB',(W,H),'#102035');draw=ImageDraw.Draw(im)
 for k in range(-84,85,12):
  for a,b in [([k,-84,0],[k,84,0]),([-84,k,0],[84,k,0])]:
   q=project([a,b]);draw.line([tuple(q[0,:2]),tuple(q[1,:2])],fill='#253d56',width=1)
 triangles=[];cols=[];depths=[]
 for bot,tr in enumerate(fr['transforms'].values()):
  R=np.array(tr['R']).reshape(3,3);world=v@R.T+tr['t'];vv=world[f];norm=np.cross(vv[:,1]-vv[:,0],vv[:,2]-vv[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-20);keep=norm@cam>0
  q=project(vv[keep]);shade=.55+.45*np.maximum(0,norm[keep]@light);c=colors[keep]*shade[:,None];triangles.append(q[:,:,:2]);depths.append(q[:,:,2].mean(axis=1));cols.append(np.clip(c*255,0,255).astype(np.uint8))
 tri=np.concatenate(triangles);color=np.concatenate(cols);depth=np.concatenate(depths)
 for j in np.argsort(depth):draw.polygon([tuple(x) for x in tri[j]],fill=tuple(color[j]))
 mech=fr.get('mechanism')
 def line(a,b,col='#ffc476',width=4):
  q=project([a,b]);draw.line([tuple(q[0,:2]),tuple(q[1,:2])],fill=col,width=width)
 if mech:
  if mech['kind']=='captured hinge':
   for root in mech['roots_mm']:line(root,mech['pivot_mm'])
   z=project(mech['pivot_mm']);draw.ellipse((z[0]-4,z[1]-4,z[0]+4,z[1]+4),fill='#fff0c0',outline='#a0773d')
  else:
   line(mech['fixed_root_mm'],mech['rail_start_mm']);line(mech['rail_start_mm'],mech['rail_end_mm'],'#e9dfb8',3);z=project(mech['carriage_mm']);draw.rectangle((z[0]-4,z[1]-4,z[0]+4,z[1]+4),fill='#ffc476')
 draw.rectangle((0,0,W,95),fill='#15283f');draw.text((25,16),'Spherical bots + pyramid docks',font=big,fill='#eef5fb');draw.text((25,54),'6-second target | 14 bots | CAD geometry + ideal captured joints',font=small,fill='#c2d8eb');draw.text((W-160,22),f'{fr["time_s"]:.2f} / 6.00 s',font=small,fill='#ffdc9e')
 draw.rectangle((0,H-82,W,H),fill='#15283f');draw.text((22,H-71),fr['label'],font=small,fill='#edf4fa');draw.text((22,H-42),'Not hardware proof: latch transfer, actuator routing, circuit and wireless power remain incomplete.',font=small,fill='#ffcd8c')
 ff.stdin.write(im.tobytes())
 if frameindex%2==0 or frameindex==119:
  if frameindex==119 and len(gifs)==60:gifs[-1]=im.quantize(128)
  else:gifs.append(im.quantize(128))
 if frameindex in [0,60,119]:im.save(p/('Ground.png' if frameindex==0 else 'Motion.png' if frameindex==60 else 'Pyramid.png'))
ff.stdin.close();assert ff.wait()==0,'ffmpeg failed';gifs[0].save(p/'SixSecondAssembly.gif',save_all=True,append_images=gifs[1:],duration=100,loop=0,optimize=False)
print('Saved 6.0 s MP4, GIF and snapshots; triangles per bot',len(f),'GIF frames',len(gifs))
