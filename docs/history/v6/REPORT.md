# V6: spherical bots, mechanism screening and six-second assembly target

The geometry and numerical checks have progressed. **A complete functional movement mechanism and correct routed circuit board have NOT been validated or implemented.** This delivery is an editable CAD candidate, an ideal constrained mechanism model, inverse-dynamics checks, a package layout, functional power-path calculations, and a detailed six-second animation. Physical auto-latching, load sharing, wire/tendon routing, motor commutation and the elevated wireless link remain unresolved. Do not read an animation or a green calculation as a production approval.

## Concrete changes

The cubic housing is replaced with a **23.6 mm diameter sphere** and **24 separate truncated-pyramid docking pods**. The body stays within a 24 mm cube while stowed. The sphere increased from the preliminary 22.4 mm candidate to clear the added reduction gears; it is larger than the early 6–8 mm control-sphere target. This is a six-face tiled docking alternative, not a restored three-arm/two-axis-per-arm architecture.

The previous linear motors are replaced with two rotary motor/gearhead candidates for lifting and one direct rotary motor candidate for sliding. A custom 20/25 tooth reduction is modeled on each geared output. A captured pin and captive rail are implemented as ideal joints in the numerical model and shown during motion. The full physical transmission to those moving joints, automated attachment mechanism and deployment hardware are not complete.

The reserve changes to a smaller 6.3 × 12 mm cylindrical 1 F capacitor. The proposed circuit now explicitly separates motor power from reserve-backed controls and includes partial-power-down signal buffers. A 20 mm circular PCB package layout is modeled with 71 bodies. It remains unrouted, with several passives, interfaces, protection and sensors unselected.

## Dimensions of each type of piece

All dimensions are mm. Nominal design dimensions are separated from trimmed CAD bounds. **BOM.csv / parts.json contain all 235 modeled part records, material, estimated mass, verification status and actual x/y/z bounds**, including every repeated pyramid and electronic package. Bounds for rotated parts are global axis-aligned dimensions, not vendor manufacturing drawings.

| Piece | Quantity/bot | Dimensions / geometry | Material or construction | Status |
|---|---:|---|---|---|
| Central sphere | 1 | OD 23.6; ID 22.9; wall 0.35 | PEEK 450G target | CAD valid; molding, sealing, wall stress untested |
| Truncated-pyramid frames | 24 | Nominal base 4 × 4 at face-normal coordinate 8; tip 3.6 × 3.6 at 11.9; taper length 3.9; nominal wall 0.3 | PEEK | Root trimmed against the central sphere; actual exposed length varies by corner |
| Docking pole lands | 48 | 0.5 × 2 × 0.4; two per pyramid; outer plane at ±12 | Magnetic steel target | 2 mm² total pole area per pyramid; force NOT established |
| Magnet inserts | 48 | 0.5 × 2 × 0.5 | NdFeB, grade unselected | Polarity compatibility and switchable release unproven |
| Radial hollow supports | 24 | OD 0.90; ID 0.44; sphere-trimmed radial length | Ti-6Al-4V target | Geometric fit; weld/bond/fastener and fatigue unresolved |
| Motherboard | 1 | Ø20 × 0.6; 4 layers | FR4 / copper | Package placement, not routed circuitry |
| Control MCU | 1 | STM32G431CBU6; UFQFPN48 7 × 7 × 0.55 | Silicon/mold package | Package and capabilities checked; firmware not implemented |
| Qi receiver IC | 1 | BQ51013B RHL 4.5 × 3.5 × 1 body allocation | Silicon/mold package | Requires tuned network and a suitable transmitter |
| Receiver coil | 1 | Würth 760308101208; ferrite OD 10.3 ±0.3; maximum stack 1.68 | Copper/ferrite | Full 10.6 maximum OD modeled; leads/tuning and coupling unvalidated |
| Control buck-boost | 1 | TPS63031 DSK 2.5 × 2.5 × 0.8 allocation | Silicon/mold package | 3.3 V target; external network/routing incomplete |
| Capacitor charger | 1 | BQ25173 DSG 2 × 2 × 0.8 allocation | Silicon/mold package | 2.604 V target, 50 mA candidate; exact full circuit not frozen |
| Power OR diodes | 2 | LM66100 DCK 2.1 × 2 × 1.1 allocation | Silicon/mold package | Proposed reverse-blocking control-only paths |
| Motor rail converter | 1 | TPS62840 DLC 1.5 × 2 × 0.8 allocation | Silicon/mold package | 3.3 V / 750 mA capability; not tested in this board |
| BLDC power stages | 3 | DRV8311P RRW 3 × 3 × 0.8 | Silicon/mold package | Correct three-phase type; sensorless startup and control incomplete |
| Signal isolation buffers | 2 | SN74AXC8T245 RJW 4 × 2 × 0.6 allocation | Silicon/mold package | Ioff and supply-isolation candidate; OE/pin routing unverified |
| Power inductors | 2 | 2.5 × 2.5 × 1 reservations, 2.2 µH target | Composite allocation | Exact parts, saturation and final values unselected |
| Other passive reservations | 56 | 0402: 1 × 0.5 × 0.5 body allocation | Composite allocation | Individual values/order codes not all selected |
| Motor isolation switch | 1 | 1.5 × 1.5 × 0.8 reservation | Composite allocation | Exact switch and fault circuitry unselected |
| Rotary motors | 3 | FAULHABER 0308H003B: Ø3 × 8.4 housing, 0.35 g each | Vendor composite | 3 V nominal, 0.013 mN·m continuous reference; shaft/mount details need supplier CAD |
| Planetary gearheads | 2 | 03B 125:1: Ø3.4 × 6, 0.18 g each | Vendor composite | 0.88 mN·m continuous; input ≤15,000 rpm; assembled combo needs confirmation |
| Custom input pinions | 2 | 20 teeth, module 0.1; pitch Ø2.0; outside Ø2.2; width 0.5 | Hardened steel target | 20° involute approximation; custom manufacturing unqualified |
| Custom output gears | 2 | 25 teeth; pitch Ø2.5; outside Ø2.7; width 0.5 | Hardened steel target | Ratio 1.25; center distance 2.25; nominal backlash reduction 0.01 per tooth at pitch |
| Hinge-drive capstans | 2 | Tendon pitch radius 0.8; axial width 0.4 | Titanium target | Tendon route, preload and brake absent |
| Slide capstan | 1 | Pitch radius 0.5; axial width 0.6 | Titanium target | Direct drive; slip/wear and attachment unproven |
| Positive capture pin example | 1 | Ø0.8 × 3 | Steel target | Coupon geometry, not a proven transferable latch |
| Bearing sleeve example | 1 | OD 1.5; ID 0.84; length 2.8 | Titanium target | Nominal 0.02 radial clearance; retention/wear untested |
| Reserve cell | 1 | KYOCERA AVX SCCQ12B105MRB: Ø6.3 × 12 | EDLC composite | 1 F nominal, 0.8 F minimum, 2.7 V, max DC ESR 1.5 Ω; lead bends not modeled |

The 24 pods use four face locations `(u,v)=(±6,±6)` on each of the six ±X, ±Y, ±Z faces, with docking planes 12 mm from the bot center. Those locations support half-pitch tier offsets geometrically. Their magnetic polarities, guide angles and tolerance stack are not universally compatible by assertion. The earlier randomized mount angles are not used here; deliberate symmetry supports the pyramid lattice.

Stowed CAD dimensions are 24.000 × 24.000 × 24.000. The modeled parts have **zero positive-volume intersections** and valid solids. This does not validate unmodeled solder lands, lead bends, full booms or wiring. The deployed pin centered on an envelope edge projects 0.4 mm beyond that boundary; a strict 24 mm operational envelope and complete connector swept volumes have NOT passed. The inverse model requires up to **6.20 mm exposed boom reach beyond the sphere**. A dimensioned production boom/rail and its storage are still to design.

## Six-second timing and speed

Uniform half-second stages would ignore different travel and docking demands. The revised sequence uses six rolls and six slides, each followed by a 50 ms capture/verification allowance:

`6 × (0.63 + 0.05) + 6 × (0.27 + 0.05) = 6.000 seconds`.

Each move follows a quintic rest-to-rest profile `q=10u³−15u⁴+6u⁵`, with peak normalized velocity 1.875/T. The trajectory holds its endpoint during the reserved capture interval; latch actuation and verification would need to occur within it. Capture timing is assumed, not measured; a single slow capture breaks the six-second budget.

| Requirement / screen | Result |
|---|---:|
| 180° roll motion time | 0.630 s |
| Average roll speed | 285.71°/s |
| Peak roll speed | 535.71°/s |
| Peak bot center-of-mass speed in a roll | 165.36 mm/s = 0.370 mph |
| Peak COM acceleration, sampled | 1.546 m/s² |
| Analytical peak roll motor input | 13950.89 rpm |
| Conservative all-angle roll torque bound | 1.418 mN·m |
| Peak hinge output speed | 89.29 rpm |
| Total reduction to hinge | 125 × 1.25 = 156.25:1 |
| Peak motor input speed, sampled | 13948 rpm |
| Gearhead continuous input ceiling | 15,000 rpm |
| Longest slide | 16.971 mm |
| Slide motion time | 0.270 s |
| Peak longest-slide speed | 117.85 mm/s = 0.264 mph |
| Peak direct slide motor speed | 2250 rpm |
| Estimated modeled bot mass | 4.616 g |
| Required peak hinge torque | 1.378 mN·m |
| Two geared drives after assumed 80% transmission efficiency | 1.760 mN·m |
| Nominal torque capacity / demand | 1.277× |
| Same screen at +25% mass/inertia | 1.037× |
| Required peak slide motor torque | 0.01006 mN·m |
| Motor continuous torque reference | 0.013 mN·m |
| Maximum ideal joint closure error | 1.41e-08 mm |

**The nominal speed/torque screens pass under stated assumptions; actual six-second assembly does not have a hardware validation pass.** CAD mass is used for inertia and center of mass, with a 1.5 multiplier on gravity/inertial load, 0.1 mN·m extra roll friction and slide friction coefficient 0.15. Two drives are assumed to share load evenly and the complete added transmission to be 80% efficient. These assumptions require measurements. Sensorless motors may have startup delay, missed commutation or inability to hold controlled torque at zero speed. The vendor advises against backdriving its gearheads; controlled braking and power-loss retention therefore need explicit supplier review and hardware proof. Stock gearhead torque limits are not evidence that the custom downstream transmission or automatic latch works.

A conservative torque bound combining maximum gravity moment with maximum angular acceleration also passes nominally at 1.418 mN·m. At +25% proportional mass/inertia its bound is 1.747 mN·m, barely below 1.760; this leaves essentially no tolerance for additional friction or unequal load sharing.

The modeled parts weigh 4.616 g; full deployable booms, all latches, guides, sensors, wiring and mounts are not represented completely in that mass. Under simple proportional mass/inertia scaling, torque capacity is exhausted at about 6.00 g, leaving roughly 1.38 g for missing hardware before this screen loses its margin. This is a sensitivity result, not a finished mass budget.

The custom gear pair was checked at 61 angles over one 18° input tooth period: **maximum nominal solid overlap 0 mm³**. That checks the sampled tooth geometry, not Hertz stress, lubricant, tooth tolerances, fatigue or 80% efficiency.

## Mechanical continuity and load checks

The ideal captured hinge/rail graph is connected for every one of the 577 poses. Flat magnetic lands alone are disconnected in 504 poses. The ideal retained constraint therefore addresses the former graph disconnect mathematically, while a real transferable pin/rail must still be built and tested. Connector switching at stage boundaries is assumed successful; the model is inverse dynamics, not a forward contact simulation proving self-assembly.

Minimum joint safe working load for 1.5 bot weights is 0.0679 N. A Ø0.8 mm pin in ideal double shear has average shear stress only 0.0675 MPa at that load. This says little about engagement, bearing stress in the thin frame, retention, alignment or fatigue. A solid pin is preferable to relying on unknown magnetic shear force as the sole load path. Permanent magnets in this candidate are alignment/holding candidates; a selectively releasable magnetic circuit has not been implemented. Power-loss brakes and a lock that holds under outage are required.

Multiple supports may share pyramid loads, but no fixed equal fraction is guaranteed during motion. The moving module is screened as supported through its active joint rather than dividing its load arbitrarily among neighbors. Full connector, base reaction, friction-cone, tipping and body/boom collision checks remain open. The 24 mm conservative BODY boxes are collision-free at all 577 sampled poses; that does not cover the deployed hardware or continuous time.

## Circuit board findings

The board is **Ø20 mm, 0.6 mm, four layers**, with 71 package bodies, nominal 0.25 mm body clearances and 0.30 mm edge margin. CAD package overlap and the 2D placement checks pass. The body layout is shown in BoardLayout.svg and board_placement.csv. Actual copper, lead pads, land patterns, all connectors and antenna/optical routes are absent. Body clearance is not a fabrication courtyard or DRC rule. Several parts are placeholders; no complete KiCad/Gerber production board is supplied.

Proposed functional power paths:

- Wireless receiver 5 V → LM66100 A → control source → TPS63031 → 3.3 V controls.
- Wireless receiver 5 V → BQ25173 → 2.604 V EDLC → LM66100 B → the same control source.
- Wireless receiver 5 V → TPS62840 → dedicated motor isolation switch → 3.3 V motor rail → three DRV8311P power stages.
- STM32G431 controls the drivers through two SN74AXC8T245 partial-power-down buffers; OE must disable before motor rail loss. Exact signal directions, analog sensing and backfeed paths still need pin-level verification.

The reserve path reaches controls and has no directed POWER path to motors in the functional graph. Signal isolation is included because merely splitting supply rails does not prevent GPIO phantom powering. This graph is not a pin netlist or an electrical certification.

| Electrical screen | Result / assumption |
|---|---|
| EDLC minimum capacitance | 0.8 F |
| DC ESR used | 1.5 Ω maximum |
| Nominal charge / logic cutoff | 2.6 / 1.9 V |
| Emergency control/communication load | 50 mW budget; normal active motor-control draw can be higher |
| Conversion efficiency | 75% assumed |
| Two-second simulated minimum loaded capacitor voltage | 2.4940 V |
| Worst charge target with assumed tolerances | 2.6352 V < 2.7 V rating |
| Proposed motor rail minimum | 3.201 V > driver 3.0 V minimum |
| Driver bus vs motor nominal | 3.3 V rail, 3 V nominal motor; current/PWM limiting required and unvalidated |
| Complete pin-level electrical rule check | NOT RUN / incomplete netlist |
| PCB routing/design-rule check | NOT RUN / unrouted |
| Startup, motor current limit, EMI, receiver tuning | UNVALIDATED |
| Two-second reserve bench test | NOT PERFORMED |
| Correct functioning circuit board | NOT VALIDATED |

The receiver coil is a real 13 µH candidate but needs matching and a transmitter coupling map. Its catalogue power-capability number is NOT harvested power at ten feet. The earlier documented 915 MHz, 3 W EIRP, 0 dBi reference yields about 0.22 mW RF at ten feet before conversion, far below controls or motion. No new ten-foot power source has been proven here. The six-second movement calculation assumes an ideal supply at each bot. A powered mat under the ground layer does not establish power for rotated/elevated modules.

## Estimate at 10,000 units

**Budgetary engineering estimate, low confidence. Every line price below is an assumption, not a supplier quote.** FAULHABER lists the selected precision parts as quote-on-request; a verified 10,000-unit drive price is unavailable. No orders or quotation requests were sent. Production yield and labor are also unmeasured.

| Item | Quantity | Extended low USD/bot | Extended high USD/bot |
|---|---:|---:|---:|
| Precision motor + 03B gearhead | 2 | 200 | 500 |
| Bare precision motor | 1 | 50 | 120 |
| Populated 4 layer PCB, ICs and passives | 1 | 25 | 55 |
| Capacitor, coil and flex interconnect | 1 | 5 | 12 |
| Sphere, 24 docks, magnets and supports | 1 | 12 | 35 |
| Captured mechanisms, custom gears and tendons | 1 | 8 | 25 |
| Assembly, calibration and functional test | 1 | 20 | 60 |

Direct subtotal: **$320–$807/bot**. With assumed 90% yield: **$356–$897/bot recurring**, approximately $3.56–$8.97 million for 10,000 delivered bots. Allowing $0.5–$2.0 million nonrecurring engineering/tooling amortized over the batch gives **$406–$1097/bot**, or **$4.06–$10.97 million total**. Taxes, shipping, power mat/beam equipment, external battery, certification, warranty and redesign are excluded. Custom commodity drives could reduce cost, but their performance is not established and no lower-cost design is qualified. Do not present these assumed prices as a quote or precise manufacturing cost.

## Validation ledger

| Check | Status |
|---|---|
| Stowed CAD bounds and valid solids | PASS geometry |
| Modeled part overlap | PASS geometry |
| Custom gear tooth motion, 61 samples | PASS nominal geometry |
| Board body placement | PASS nominal geometry |
| Reserve discharge with maximum listed ESR | PASS simplified electrical model |
| Roll and slide speed/torque | PASS stated nominal inverse-dynamics assumptions |
| Ideal retained joint closure and graph | PASS mathematical model |
| Complete physical movement mechanism | INCOMPLETE |
| Working six-second pyramid assembly | NOT VALIDATED |
| Transferable capture, brakes, 50 ms handoff | UNIMPLEMENTED / unmeasured |
| Operational envelope and connector collisions | UNVALIDATED; pin can protrude beyond stowed boundary |
| Complete correct circuit board | INCOMPLETE / no pin-level ERC or routing DRC |
| Magnetic holding/release | UNVALIDATED |
| Elevated and ten-foot wireless power | UNRESOLVED; previous reference link fails |
| Thermal, endurance, fatigue and 10k cost | UNVALIDATED / unquoted |

## Evidence

- [FAULHABER 0308 motor datasheet](https://www.faulhaber.com/fileadmin/Import/Media/EN_0308_B_DFF.pdf): continuous motor reference, size, mass and current. Do not substitute stall torque.
- [FAULHABER 03B 125:1 gearhead](https://eshop.faulhaber.com/en/03B-125-1/03B-125-1): output torque/input-speed ceiling, size and mass. No public 10k quote.
- [KYOCERA AVX SCC datasheet](https://datasheets.kyocera-avx.com/AVX-SCC.pdf): SCCQ12B105MRB size, capacitance and max DC ESR.
- [Würth 760308101208](https://www.we-online.com/components/products/datasheet/760308101208.pdf): exact coil envelope and electrical characteristics.
- [STM32G431 datasheet](https://www.st.com/resource/en/datasheet/stm32g431cb.pdf): UFQFPN48 package and controller capabilities; not a ready three-motor firmware implementation.
- [BQ51013B](https://www.ti.com/product/BQ51013B), [TPS63031](https://www.ti.com/product/TPS63031), [BQ25173](https://www.ti.com/product/BQ25173), [LM66100](https://www.ti.com/product/LM66100), [TPS62840](https://www.ti.com/product/TPS62840), [DRV8311](https://www.ti.com/product/DRV8311), [SN74AXC8T245](https://www.ti.com/product/SN74AXC8T245): supplier component capabilities. Full application circuits, thermal design, matching and pin-level wiring are still required.
- [Victrex 450G](https://www.victrex.com/en/products/polymers/peek-polymers/450g), [TIMETAL 6-4](https://www.timet.com/documents/datasheets/alpha-and-beta-alloys/timetal-6-4.pdf): candidate material properties; not thin-part, weld, bond or fatigue qualification.

## Reproduce and inspect

SixSecondAssembly.mp4 and SixSecondAssembly.gif are saved demonstrations, rendered directly from CAD meshes and the same trajectory. They show the target motion, not a physical test. After recovery, the local browser preview was verified to render the detailed bots and reach stage 12 at 6.000 seconds; BrowserVerified.png records the result. This verifies software playback only.

Open RefinedBots.html through a local server for the detailed WebGL demonstration. Default view has no cube envelopes; use slow replay to inspect the active pin/rail, or inspect one bot and reveal internal components. The meshes are generated from FreeCAD. The visible moving connector represents ideal constraints; it is not a fully dimensioned physical actuator assembly.

Build order: design_board.py → plan_assembly.py (NumPy) → BuildSphere.FCMacro (FreeCAD) → AuditInertia.FCMacro (FreeCAD) → analyze.py (NumPy) → audit_topology.py → check_electrical.py → cost_and_layout.py → write_report.py. BuildSphere saves Bot24.FCStd, Bot24.step, Swarm14.FCStd, BOM and meshes, then closes FreeCAD automatically. AuditInertia exports mass properties and checks custom gear geometry, then closes FreeCAD. CAD and physics files remain editable.

The next validation work must implement the complete captured boom/rail, latch and brake with sensors, then prove the closed-loop motion on real hardware; finish a complete schematic and routed PCB with ERC/DRC and bench tests; and demonstrate loaded wireless power at every required pose. Those are concrete missing engineering deliverables, not details that can be waived by speeding up the animation.
