from pathlib import Path
import json,numpy as np
p=Path(__file__).parent;data=json.loads((p/'assembly.json').read_text());ns=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1.]])
local=[];ln=[]
for n in ns:
 u=np.array([0,1.,0]) if abs(n[0])==1 else np.array([1.,0,0]);v=np.cross(n,u)
 for a in [-6,6]:
  for b in [-6,6]:local.append(12*n+a*u+b*v);ln.append(n)
local=np.array(local);ln=np.array(ln)
def connected(edges):
 seen={0}
 for _ in range(14):
  for i,j in edges:
   if i in seen or j in seen:seen.update([i,j])
 return len(seen)==14
frames=[]
for k,fr in enumerate(data['frames']):
 ps=[];norm=[]
 for tr in fr['transforms'].values():
  R=np.array(tr['R']).reshape(3,3);ps.append(local@R.T+tr['t']);norm.append(ln@R.T)
 edges=[];count=0
 for i in range(14):
  for j in range(i):
   hit=(np.linalg.norm(ps[i][:,None]-ps[j][None,:],axis=2)<1e-5)&(norm[i]@norm[j].T<-.999999);c=int(hit.sum())
   if c:edges.append((j,i));count+=c
 flat=connected(edges)
 if fr['stage']:
  a=data['actions'][fr['stage']-1];edges.append((a['bot'],a['parent']))
 frames.append(dict(frame=k,flat_docks_connected=flat,ideal_captive_joint_graph_connected=connected(edges),flat_land_pairs=count))
report=dict(flat_docks_disconnected_frames=sum(not f['flat_docks_connected'] for f in frames),ideal_captive_joint_graph_connected_all_frames=all(f['ideal_captive_joint_graph_connected'] for f in frames),scope='Added pin/rail edge is an ideal retained constraint. Automatic physical latch transfer is assumed and unvalidated.',frames=frames)
(p/'topology_report.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='frames'})
