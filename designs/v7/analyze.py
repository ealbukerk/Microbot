"""Inverse-dynamics screening with CAD mass/inertia and ideal pin/rail constraints."""
from pathlib import Path
import json,math,csv,numpy as np
p=Path(__file__).parent;d=json.loads((p/'assembly.json').read_text());parts=json.loads((p/'inertia_parts.json').read_text());m=sum(q['mass_kg'] for q in parts);com=sum((q['mass_kg']*np.array(q['com_m']) for q in parts),np.zeros(3))/m;I=np.zeros((3,3))
for q in parts:
 r=np.array(q['com_m'])-com;I+=np.array(q['I_com_kgm2'])+q['mass_kg']*((r@r)*np.eye(3)-np.outer(r,r))
grav=np.array([0,0,-9.80665]);rows=[];maxclosure=0.;starttimes=[0]
for a in d['actions']:starttimes.append(starttimes[-1]+a['duration'])
for k,fr in enumerate(d['frames']):
 if not fr['stage']:fr['mechanism']=None;continue
 stage=fr['stage']-1;a=d['actions'][stage];initial=d['frames'][stage*48];bot=a['bot'];parent=a['parent'];tr=fr['transforms'][f'B{bot}'];R=np.array(tr['R']).reshape(3,3);t=np.array(tr['t'])/1000;t0=np.array(initial['transforms'][f'B{bot}']['t'])/1000;R0=np.array(initial['transforms'][f'B{bot}']['R']).reshape(3,3);pt=np.array(fr['transforms'][f'B{parent}']['t'])/1000
 T=a['motion_duration'];u=min(1,max(0,(fr['time_s']-starttimes[stage])/T));up=30*u*u*(u-1)**2/T;upp=60*u*(2*u*u-3*u+1)/T**2
 worldcom=t+R@com;force=0;torque=0;rpm=0;boom=0
 if a['kind']=='roll':
  axis=np.array([1,0,0]) if a['axis']=='x' else np.array([0,1,0]);pivot=np.array(a['pivot'])/1000
  # Center the actual pin along its unchanged axis line between the two bot center projections.
  axisindex=0 if a['axis']=='x' else 1;pivot[axisindex]=(t0[axisindex]+pt[axisindex])/2
  omega=axis*a['angle']*up;alpha=axis*a['angle']*upp;r=worldcom-pivot
  acc=np.cross(alpha,r)+np.cross(omega,np.cross(omega,r));J=R@I@R.T+m*((r@r)*np.eye(3)-np.outer(r,r))
  speed=float(np.linalg.norm(np.cross(omega,r)));tau=float((J@alpha+np.cross(omega,J@omega)-np.cross(r,m*grav))@axis)
  torque=1.5*abs(tau)+(.0001 if u<1 else 0);force=1.5*np.linalg.norm(m*(acc-grav));rpm=abs(a['angle']*up)*60/(2*math.pi)*156.25
  local=R0.T@(pivot-t0);closure=np.linalg.norm(t+R@local-pivot)*1000;maxclosure=max(maxclosure,closure)
  roots=[]
  for center in [t,pt]:
   vec=pivot-center;root=center+vec/np.linalg.norm(vec)*.0118;roots.append((root*1000).tolist());boom=max(boom,np.linalg.norm(vec)*1000-11.8)
  fr['mechanism']=dict(kind='captured hinge',pivot_mm=(pivot*1000).tolist(),roots_mm=roots,axis=axis.tolist(),angle_rad=a['angle']*fr['phase'],closure_error_mm=closure,boom_extension_mm=boom,torque_required_mNm=torque*1000,required_input_rpm=rpm)
 else:
  delta=np.array(a['delta'])/1000;acc=delta*upp;distance=np.linalg.norm(delta);speed=distance*up;friction=.15*m*9.80665
  force=1.5*m*np.linalg.norm(acc)+friction;torque=force*.0005/.8;rpm=speed/.0005*60/(2*math.pi)
  unit=(t0-pt)/np.linalg.norm(t0-pt);rail=t0-unit*.0118;root=pt+unit*.0118;carriage=rail+delta*fr['phase'];closure=np.linalg.norm((t-unit*.0118)-carriage)*1000;maxclosure=max(maxclosure,closure)
  fr['mechanism']=dict(kind='captive linear guide',fixed_root_mm=(root*1000).tolist(),rail_start_mm=(rail*1000).tolist(),rail_end_mm=((rail+delta)*1000).tolist(),carriage_mm=(carriage*1000).tolist(),stroke_mm=distance*1000,closure_error_mm=closure,torque_required_mNm=torque*1000,required_input_rpm=rpm)
 fr['mechanism']['supply']='Ideal external supply assumed. No wireless delivery validation.'
 rows.append(dict(frame=k,time_s=fr['time_s'],stage=stage+1,kind=a['kind'],motor_input_rpm=rpm,required_torque_mNm=torque*1000,required_force_N=force,closure_error_mm=closure,com_speed_mm_s=speed*1000,com_accel_m_s2=float(np.linalg.norm(acc))))
roll=[q for q in rows if q['kind']=='roll'];slide=[q for q in rows if q['kind']=='slide'];peakroll=max(q['required_torque_mNm'] for q in roll);avail=2*.88*1.25*.8;peakslide=max(q['required_torque_mNm'] for q in slide)
bounds=[]
for k,a in enumerate(d['actions']):
 if a['kind']!='roll':continue
 fr=d['frames'][k*48];tr=fr['transforms'][f"B{a['bot']}"];R0=np.array(tr['R']).reshape(3,3);t0=np.array(tr['t'])/1000;axis=np.array([1.,0,0]) if a['axis']=='x' else np.array([0,1.,0]);pivot=np.array(a['pivot'])/1000;rr=t0+R0@com-pivot;rp2=rr@rr-(rr@axis)**2;Jaxis=axis@(R0@I@R0.T)@axis+m*rp2;amax=(10/math.sqrt(3))*abs(a['angle'])/a['motion_duration']**2;bounds.append(1.5*(m*9.80665*math.sqrt(rp2)+Jaxis*amax)*1000+.1)
report=dict(mass_g=m*1000,roll_peak_com_speed_mm_s=max(q['com_speed_mm_s'] for q in roll),maximum_COM_acceleration_m_s2=max(q['com_accel_m_s2'] for q in rows),peak_joint_force_N=max(q['required_force_N'] for q in rows),analytic_roll_input_speed_peak_rpm=1.875*180/.63/6*156.25,conservative_roll_torque_bound_mNm=max(bounds),conservative_bound_pass=max(bounds)<=avail,conservative_bound_plus25pct_mass_pass=1.25*(max(bounds)-.1)+.1<=avail,com_mm=(com*1000).tolist(),inertia_com_kgm2=I.tolist(),duration_s=6,roll_motion_s=.63,slide_motion_s=.27,capture_dwell_s=.05,roll_peak_deg_s=1.875*180/.63,roll_peak_output_rpm=1.875*180/.63/6,roll_peak_motor_rpm=max(q['motor_input_rpm'] for q in roll),gear_input_limit_rpm=15000,roll_required_mNm=peakroll,two_geared_motors_available_after_80pct_transmission_mNm=avail,nominal_roll_torque_margin=avail/peakroll,roll_speed_screen_pass=max(q['motor_input_rpm'] for q in roll)<=15000,nominal_roll_torque_screen_pass=peakroll<=avail,roll_mass_plus_25pct_margin=avail/(1.25*(peakroll-.1)+.1),slide_peak_motor_rpm=max(q['motor_input_rpm'] for q in slide),slide_required_motor_mNm=peakslide,slide_continuous_motor_mNm=.013,slide_torque_screen_pass=peakslide<=.013,slide_peak_mm_s=1.875*math.sqrt(288)/.27,max_ideal_constraint_closure_mm=maxclosure,max_deployed_boom_extension_mm=max(fr['mechanism'].get('boom_extension_mm',0) for fr in d['frames'] if fr['mechanism']),reserve_capacitance_min_F=.8,reserve_ESR_DC_max_ohm=1.5,reserve_charge_V=2.6,reserve_cutoff_V=1.9,reserve_load_W=.05,reserve_efficiency_assumed=.75,reserve_ideal_energy_to_load_J=.5*.8*(2.6**2-1.9**2)*.75,reserve_ideal_time_s=.5*.8*(2.6**2-1.9**2)*.75/.05,physical_latch_transfer_validated=False,full_actuator_transmission_implemented=False,connector_swept_volume_audited=False,hardware_6_second_assembly_validated=False,scope='Rigid pin/rail inverse dynamics, not forward dynamics or hardware validation. Coulomb slide friction coefficient 0.15; extra roll friction 0.1 mNm; torque sharing and 80% transmission efficiency assumed. 1.5 load multiplier applied. Sensors, commutation, brakes, clutches, tendon routing and 50 ms capture need proof.')
(p/'mechanism_report.json').write_text(json.dumps(report,indent=2,default=lambda x:x.item()));(p/'assembly.json').write_text(json.dumps(d,separators=(',',':'),default=lambda x:x.item()))
with (p/'actuator_trace.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(report,indent=2,default=lambda x:x.item()))
