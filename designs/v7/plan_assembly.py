"""Hub-free 14-unit geometric assembly plan. Not an actuator or wireless validation.
NumPy only. Dimensions mm, time s. OBB tests use 24 mm conservative envelopes.
"""
from pathlib import Path
import json,math,csv
import numpy as np
P=Path(__file__).parent;SIDE=24.;H=12.;I=np.eye(3)
def rx(a):return np.array([[1,0,0],[0,math.cos(a),-math.sin(a)],[0,math.sin(a),math.cos(a)]])
def ry(a):return np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
def pose(R,t):return {'R':np.round(R,9).flatten().tolist(),'t':np.round(t,8).tolist()}
def collision(a,b,tol=1e-6):
 # Separating axis test. Touching is allowed, positive-volume penetration is not.
 A=a[0];B=b[0];v=b[1]-a[1];axes=[A[:,i] for i in range(3)]+[B[:,i] for i in range(3)]
 axes += [np.cross(A[:,i],B[:,j]) for i in range(3) for j in range(3)]
 for axis in axes:
  n=np.linalg.norm(axis)
  if n<1e-9:continue
  axis=axis/n;ra=H*sum(abs(axis@A[:,i]) for i in range(3));rb=H*sum(abs(axis@B[:,i]) for i in range(3));gap=abs(axis@v)-ra-rb
  if gap>=-tol:return False
 return True
def contacts(a,b,tol=1e-5):
 # OBB no-separation contact. Includes zero-area edge hinges, flagged in report.
 v=b[1]-a[1];axes=[a[0][:,i] for i in range(3)]+[b[0][:,i] for i in range(3)]
 axes += [np.cross(a[0][:,i],b[0][:,j]) for i in range(3) for j in range(3)]
 for axis in axes:
  n=np.linalg.norm(axis)
  if n<1e-9:continue
  axis=axis/n;r=H*sum(abs(axis@a[0][:,i])+abs(axis@b[0][:,i]) for i in range(3))
  if abs(axis@v)>r+tol:return False
 return True
def connected(edges):
 seen={0};change=True
 while change:
  old=len(seen)
  for i,j in edges:
   if i in seen or j in seen:seen.update([i,j])
  change=len(seen)>old
 return len(seen)==14
centers=[np.array([x,y,12.]) for y in [-24,0,24] for x in [-24,0,24]]
centers += [np.array([-48.,-12,12]),np.array([48.,-12,12]),np.array([-48.,12,12]),np.array([48.,12,12]),np.array([-24.,-48,12])]
state=[(I.copy(),p.copy()) for p in centers];actions=[]
def roll(bot,pivot,axis,angle,parent,label):actions.append(dict(bot=bot,kind='roll',pivot=pivot,axis=axis,angle=angle,parent=parent,label=label,duration=.68,motion_duration=.63))
def slide(bot,delta,parent,label):actions.append(dict(bot=bot,kind='slide',delta=delta,parent=parent,label=label,duration=.32,motion_duration=.27))
roll(13,[-24,-36,24],'x',-math.pi,0,'Raise future apex bot over the front base edge')
slide(13,[12,-12,0],0,'Park apex bot beside the future second tier')
for bot,x,y,parent in [(9,-48,-12,0),(10,48,-12,2),(11,-48,12,6),(12,48,12,8)]:
 sign=-1 if x<0 else 1;roll(bot,[sign*36,y,24],'y',-sign*math.pi,parent,'Fold middle-tier bot '+str(bot+1)+' over a retained edge')
 slide(bot,[-sign*12,0,0],parent,'Slide middle-tier bot '+str(bot+1)+' into its 2 × 2 position')
roll(13,[-12,-24,48],'x',-math.pi,9,'Raise the apex bot over the completed middle tier')
slide(13,[12,12,0],9,'Center the apex bot over all four middle-tier bots')
frames=[];clock=0;failures=[]
def record(stage,label,moving=None,kind='initial',phase=0):
 pairs=[];bad=[]
 for i in range(14):
  for j in range(i):
   if collision(state[i],state[j]):bad.append([j,i])
   if contacts(state[i],state[j]):pairs.append([j,i])
 corners=np.array([[x,y,z] for x in [-H,H] for y in [-H,H] for z in [-H,H]])
 ground=min(float(np.min(corners@s[0].T+s[1],axis=0)[2]) for s in state)
 f=dict(time_s=round(clock,4),stage=stage,label=label,moving_bot=moving,mode=kind,phase=phase,transforms={f'B{i}':pose(*s) for i,s in enumerate(state)},contacts=pairs,geometric_contact_graph_connected=connected(pairs),colliding_envelopes=bad,minimum_envelope_ground_z_mm=ground)
 if bad or not f['geometric_contact_graph_connected'] or ground<-.0001:failures.append({'frame':len(frames),'collisions':bad,'connected':f['geometric_contact_graph_connected'],'ground_z':ground})
 frames.append(f)
record(0,'Connected 14-bot planar starting unit')
for k,a in enumerate(actions):
 bot=a['bot'];R0,t0=state[bot][0].copy(),state[bot][1].copy();start=clock
 for step in range(1,49):
  elapsed=a['duration']*step/48;u=min(1.,elapsed/a['motion_duration']);u=u*u*u*(10+u*(-15+6*u))
  if a['kind']=='roll':
   r=(rx if a['axis']=='x' else ry)(a['angle']*u);pivot=np.array(a['pivot']);state[bot]=(r@R0,pivot+r@(t0-pivot))
  else:state[bot]=(R0,t0+np.array(a['delta'])*u)
  clock=start+a['duration']*step/48;record(k+1,a['label'],bot,a['kind'],u)
expected=[np.array([x,y,12.]) for y in [-24,0,24] for x in [-24,0,24]]+[np.array([x,y,36.]) for y in [-12,12] for x in [-12,12]]+[np.array([0,0,60.])]
final_error=max(float(np.linalg.norm(state[i][1]-expected[i])) for i in range(14))
summary={'bots':14,'power_hubs':0,'envelope_mm':24,'formation':[9,4,1],'final_pyramid_envelope_mm':[72,72,72],'frames':len(frames),'duration_s':clock,'motion_law':'quintic rest to rest; 50 ms prescribed capture dwell per stage','geometric_collision_free':all(not f['colliding_envelopes'] for f in frames),'geometric_contact_graph_connected_all_frames':all(f['geometric_contact_graph_connected'] for f in frames),'final_center_error_mm':final_error,'ground_penetration_free':all(f['minimum_envelope_ground_z_mm']>=-.0001 for f in frames),'failures':failures,'physical_magnetic_retention_validated':False,'actuator_execution_validated':False,'wireless_power_validated':False,'scope':'Rigid envelope path only. Edge touching is not evidence of a functioning magnetic hinge, and sliding is not an implemented drive. Timing is a six-second target with explicit motion and handoff durations; hardware execution remains unproven.'}
(P/'assembly.json').write_text(json.dumps({'summary':summary,'actions':actions,'frames':frames},separators=(',',':')));(P/'assembly_report.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
