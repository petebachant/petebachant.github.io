---
comments: true
date: 2014-03-12 00:19:51+00:00
layout: post
slug: yz-traversing-carriage
title: YZ traversing carriage
---

{% include figure.html src="/images/yz-traverse-photo.png" caption="Traversing carriage assembly installed as part of the UNH CORE turbine test bed." width="80%" %}

In order to perform turbine wake measurements in UNH's tow tank, I designed and built a 2-axis positioning system for our Nortek Vectrino acoustic Doppler velocimeter. Some specifications are shown in the table below:

---

<center>

|  |  |
|:----------|:------|
| Cross-stream (y-axis) travel | 3.0 m |
| Vertical (z-axis) travel | 1.2 m |
| Max drag force (estimated) | 25 N at 2 m/s |

</center>

---


## Components

The frame is constructed mostly from 80/20 15 series t-slot framing and hardware, with some custom brackets to mount to 1.25" pillow block linear bearings.

Attached to the frame are two Velmex BiSlide linear stages, with the y-axis driven by a stepper/belt and the z-axis driven by a stepper/ball screw. An additional igus DryLin polymer linear bearing, along with a second carriage on the z-stage BiSlide provide additional moment loading capacity.

{% include figure.html src="/images/yz-traverse-rendering.jpg" caption="SolidWorks rendering of the YZ traverse assembly." width="80%" %}

The Vectrino probe is clamped in a cantilevered bar attached to a NACA 0020 strut. The foil is attached to an 80/20 extrusion, which mounts to the z-axis linear stage via two custom adapter blocks. Note that the adapter blocks' odd  odd trapezoidal shape is due to the fact they're made from recycled material.

Two igus Energy Chain cable carriers span the horizontal and vertical axes to keep the Vectrino and motor cables from tangling during operation.



## Actuation and control


The stepper motors are driven by an ACS UDMlc drive controlled by an ACS NTM EtherCAT master controller, which provides synchronized operation with the tow and turbine axes through ACS' SPiiPlus interface. In addition to the ability to write motion control programs with their ACSPL+ language, COM, and C library, the [ACSpy](https://github.com/petebachant/ACSpy) Python wrapper for the C library allows incorporating motion commands into Python programs, e.g., [TurbineDAQ](https://github.com/petebachant/TurbineDAQ).



## CAD file download


A full assembly of this design, minus some minor hardware, is available for download in (SolidWorks 2012 format) [here](https://drive.google.com/file/d/0BwMVIAlxIxfZQk5FWW5FR3NIaWs/edit?usp=sharing). Contact me if you would like something similar designed and/or built.
