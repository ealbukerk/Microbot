"""Functional architecture checks only; not a pin-level ERC or SPICE IC model."""
from pathlib import Path
import math,json,csv
p=Path(__file__).parent
# Directed edges represent proposed reverse-blocking paths, NOT fitted PCB nets.
edges=[('RX5','IDEAL_A'),('IDEAL_A','LOGIC_SOURCE'),('RX5','CHARGER'),('CHARGER','CAP2V6'),('CAP2V6','IDEAL_B'),('IDEAL_B','LOGIC_SOURCE'),('LOGIC_SOURCE','CTRL_BUCKBOOST'),('CTRL_BUCKBOOST','CTRL3V3'),('RX5','MOTOR_BUCK'),('MOTOR_BUCK','ISOLATION_SWITCH'),('ISOLATION_SWITCH','MOTOR3V3')]
def reachable(start):
 out={start}
 for _ in range(20):
  for a,b in edges:
   if a in out:out.add(b)
 return out
# Constant-power outage model including max catalogue DC ESR.
v=2.6;C=.8;R=1.5;P=.05;eta=.75;dt=.001;trace=[]
for n in range(2001):
 demand=P/eta;disc=v*v-4*R*demand;current=(v-math.sqrt(max(0,disc)))/(2*R);terminal=v-current*R
 trace.append(dict(time_s=n*dt,cap_open_V=v,cap_terminal_V=terminal,current_A=current,logic_alive=terminal>=1.9,motor_enabled=False))
 if n<2000:v-=current*dt/C
checks=dict(scope='Proposed block graph and scalar range calculations. No pin-level netlist, regulator transient model, ERC, DRC or bench validation.',reserve_path_reaches_controls='CTRL3V3' in reachable('CAP2V6'),reserve_path_cannot_reach_motor_power='MOTOR3V3' not in reachable('CAP2V6'),two_second_controls_survive_ESR_model=all(q['logic_alive'] for q in trace),two_second_min_terminal_V=min(q['cap_terminal_V'] for q in trace),cap_max_charge_V_with_1pct_regulator_and_0p1pct_divider=2.604*1.012,cap_rating_V=2.7,charge_voltage_range_screen_pass=2.604*1.012<2.7,motor_rail_min_assumed_V=3.3*.97,driver_VM_min_V=3,motor_rail_range_screen_pass=3.3*.97>=3,logic_source_min_V=1.9,buckboost_min_input_V=1.8,normal_input_assumed_V=[4.75,5.25],OR_IC_max_V=5.5,poweroff_signal_isolation_part='2 x SN74AXC8T245RJWR; OE sequence and all paths need pin-level checking',MCU='STM32G431CBU6',driver='3 x DRV8311PRRWR',charger='BQ25173DSGR',control_converter='TPS63031DSKR',motor_converter='TPS62840DLCR',OR_IC='2 x LM66100DCKR',board_diameter_mm=20,board_thickness_mm=.6,board_layer_count=4,complete_routed_board_validated=False,exact_feedback_passives_and_coil_matching_frozen=False,PCB_ERC_pass=False,PCB_DRC_pass=False,hardware_functional_pass=False)
(p/'electrical_check.json').write_text(json.dumps(checks,indent=2));(p/'functional_topology.json').write_text(json.dumps(edges,indent=2))
with (p/'reserve_trace.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=trace[0]);w.writeheader();w.writerows(trace)
print(json.dumps(checks,indent=2))
