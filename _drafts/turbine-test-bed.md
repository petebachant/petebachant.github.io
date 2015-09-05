---
author: Pete
comments: true
date: 2011-12-14 14:27:45+00:00
layout: page
published: false
slug: No Content Found
title: UNH-CORE turbine test bed
wordpress_id: 600
---

In 2010–2011, as part of my masters research, I designed and built a turbine test bed for use with the UNH tow/wave tank. The first iteration allowed measurement of mechanical power (torque and RPM) and overall turbine drag for vertical axis turbines. The turbine was loaded with a manually actuated hydraulic disk brake, and could operate up to turbine diameter Reynolds numbers $$Re_D \approx 1.4 \times 10^6$$.

The test bed was then upgraded as part of the 2012 Tow Tank Upgrades. The tank's new capabilities increased steady-state towing time and the ability to fully automate experiments. Turbine loading was automated via servomotor and controlled by the tow tank's main motion controller. I also designed and built a YZ traversing carriage for automatic positioning of an acoustic Doppler velocimeter (ADV) probe for detailed turbine wake measurements. The upgrades increased the number of tows per experiment drastically. In 2011, a "big" set of experiments was about 100 runs. In 2014, a Reynolds number dependence study (yet to be published) tipped the scales at just over 1,500 runs.

To fully automate experiments, I built a Python GUI app called TurbineDAQ, which also required writing ACSpy, daqmx, and PdCommPy-Python wrapper packages for communicating with the motion controller, data acquisition hardware, and ADV, respectively. All code is open source and available via GitHub.

## Acknowledgements
Thanks to:
* The US Department of Energy for an infrastructure grant, which was used to rebuild the tow tank systems, including the turbine test bed.
* Lucid Energy Technologies LLP for donating turbines and hydrofoil strut sections.
* igus inc. for donating a slewing ring bearing for the servo motor mount.
