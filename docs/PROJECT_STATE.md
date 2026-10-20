# Design state — V7

Imported 19 October 2026 from the locally recovered design. This repository contains the current editable project, simulation assets, CAD exports, screenshots, raw numerical outputs and cost models. Earlier hub designs are superseded; their requirements evolution is summarized below.

## Current geometry and motion

- 24 mm stowed bounds; 23.6 mm OD / 22.9 mm ID PEEK sphere.
- 24 triangular docking pods, with 8 mm equilateral nominal bases, 3.6 mm landing sides and 3.9 mm rise. Root geometry is sphere/face-sector trimmed. Nominal slope is 71.96 degrees to the landing plane, still steep.
- Split circular steel poles and custom NdFeB pieces replace the square magnetic lands. Magnetic holding, polarity compatibility and selective release are unmeasured.
- 235 modeled pieces per bot; estimated mass 4.6378 g. CAD reports valid solids, 24 mm stowed bounds and no detected internal intersections.
- Fourteen bots form a 3×3 base, 2×2 middle and single apex. The target uses six rolls and six slides, including twelve assumed 50 ms capture dwells, in six seconds.
- Nominal inverse-dynamics screening passes with the retained precision drives and assumed transmission efficiency/friction. The complete tendon, latch, brake and drive routing is not implemented. Connector swept-contact checks and physical assembly remain open.

## Power and electronics

Each bot is intended to receive continuous external wireless power. A 1 F capacitor reserves control/communication power for at least two seconds in the scalar model while motion pauses. A ground mat and an external source within ten feet were requested; power delivery to elevated poses has not been demonstrated.

The Ø20 × 0.6 mm four-layer board has 71 modeled package bodies with checked body placement. It has no completed pin-level netlist, copper routing, ERC/DRC, firmware or functional bench validation. The MCU is STM32G431CBU6; three DRV8311 stages, receiver, charger, converters and isolation parts are packaging/circuit candidates, not a finished motherboard.

## Cost at 10,000 units

All figures are unquoted engineering allowances. Structural feedstock only: $0.39–$1.48 per bot, excluding bought components and fabrication. Current purchased/fabricated parts: $300–$747 before final assembly. Current assembled estimate at 90% yield: $355.56–$896.67; with allocated NRE: $405.56–$1,096.67. The future custom-drive spending target is $47.67 at 90% yield, excluding NRE; it has not been achieved and no cheap drive replacement is fitted in CAD.

## Requirement evolution

- Power hubs were removed. The latest design has no 240 mm hub.
- The earlier 2 mph relative movement requirement was dropped; the current metric is a six-second target assembly.
- Joint safety intent is support for 1.5× bot weight. Shared loading does not establish magnetic retention or system strength without measured geometry and load paths.
- V6 square collars were replaced by V7 triangular ramps to improve approach geometry. Geometry alone does not demonstrate climbing.

## Next engineering work

1. Implement and bench-test a complete captured movement, brake and transfer mechanism.
2. Measure magnetic retention, release, shear/peel, polarity and tolerance behavior.
3. Finish schematic, PCB routing, ERC/DRC, firmware and loaded power/thermal tests.
4. Demonstrate wireless power at every formation pose.
5. Source and qualify a cost-reduced drive; obtain supplier quotes rather than treating spending caps as prices.
6. Validate full connector/body swept geometry, physical six-second motion and endurance.

Potential first applications: powered tabletop research/education kits, physical terrain/data displays, tactile diagrams and lightweight adaptive fixtures. These are application ideas, not validated capabilities.
