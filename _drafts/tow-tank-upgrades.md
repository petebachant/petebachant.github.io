---
author: Pete
comments: true
date: 2011-12-14 14:27:45+00:00
layout: page
published: false
slug: unh-tow-tank
title: UNH tow tank
wordpress_id: 600
---

In 2011, after finishing up my masters work and deciding to stay on for a PhD, I took on the task of upgrading the UNH Tow/Wave Tank. Using the tank throughout 2010 and 2011, I had become well-acquainted with the systems' inadequacies, which made me (possibly unfortunately) a perfect candidate for upgrading the tank using UNH's recently acquired $140k infrastructure grant from the US Department of Energy. Below is a summary of how each system was upgraded. See here for the full design report



## Linear guide system


The old linear guide system consisted of fiberglass tubes and plastic wheels mounted to the carriage. The system had failed structurally over its years of use, and band-aid fixes had been applied. Furthermore, the custom design made it difficult to add other carriages to the track, as they would need to conform to this non-standard geometry.



## Motion and control


With the old system, powered by a 10 hp induction motor, steady towing times with turbines at 1.4 m/s were only on the order of one second. Velocity control was open-loop, and there was no position control, beyond the eyeball of the operator, who had to guess and hope the tow carriage would coast to a stop before crashing into the end of the tank. The drive member—a 1/4" diameter wire rope—gave the system a very low spring constant, which produced large oscillations during acceleration and under the unsteady loading of e.g. a cross-flow turbine.

The servo and gearbox were sized based on my turbine towing requirements with help from Minarik/Kaman and Kollmorgen's Motioneering software.



## Data acquisition


The old data acquisition (DAQ) system required a PC or laptop on the carriage for collecting data, which was controlled via Remote Desktop through a WiFi network.



## Onboard accessories


The carriage was previously powered by 12 V automotive batteries and an inverter. This was only enough to run a low power data acquisition system. We wanted to be able to automate turbine loading (multiple kW) and run high frame-rate particle image velocimetry (PIV) system, at the very least. These would be impossible with the old system.



## Other additions


The turbine test bed was upgraded to allow total automation.



### YZ traversing carriage


A YZ traversing carriage was designed and built to automatically position instrumentation in the tank, e.g. velocity probes in turbine wakes. For more information see here.



## CAD


Full tow tank assembly 3D model
Carriage assembly 3D model
YZ traverse 3D model
Drawing package for custom manufactured parts from 2012 upgrades



## Acknowledgements


Thanks to the US Department of Energy for the infrastructure grant.
