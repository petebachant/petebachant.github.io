---
comments: true
date: 2013-08-01 01:42:55+00:00
layout: post
slug: stepper-motor-control-with-the-beaglebone-black-and-python
title: Stepper motor control with the BeagleBone Black and Python
tags: ["BeagleBone", "Python", "automation"]
---

The BeagleBone Black (BBB) is a $45 credit-card-sized computer that runs
embedded Linux. I recently purchased a BBB along with an [$8 4-phase stepper
motor and
driver](http://www.amazon.com/gp/product/B0089JV2OM/ref=oh_details_o00_s00_i03?ie=UTF8&psc=1)
to start playing around with slightly "closer-to-the-metal" motion control.

My first objective with the BBB was to simply get the stepper to move, and for
this I started using the included Cloud9 IDE and BoneScript library. After a
while messing around and learning a little JavaScript, along with some help from
my programmer brother Tom, the stepper was moving in one direction using wave
drive logic. However, the code felt awkward. I decided I'd rather use Python,
since I'm a lot more comfortable with it, so I went out in search of Python
packages or modules for working with the BeagleBone's general purpose I/O (GPIO)
pins. I found two: Alexander Hiam's
[PyBBIO](https://github.com/alexanderhiam/PyBBIO) and Adafruit's
[Adafruit_BBIO](https://github.com/adafruit/adafruit-beaglebone-io-python).
Adafruit_BBIO seemed to be more frequently maintained and better documented, so
I installed it on the BeagleBone per their instructions, which was pretty quick
and painless.

{% include figure.html src="/images/bb-stepper.png" width="60%" caption="Stepper motor wired up to the BeagleBone Black." %}

Next, I wrote a small, simple python module,
[BBpystepper](https://github.com/petebachant/BBpystepper), with a `Stepper`
class for creating and working with a stepper control object. Currently the
control uses full-step drive logic, with wave drive available by changing
`Stepper.drivemode`. I may add half-stepping in the future, but for now
full-stepping gets the job done.


## Usage

After installing Adafruit_BBIO and BBpystepper on the BeagleBone, the module can be imported into a Python script or run from a Python interpreter. For example:

```python
>>> from bbpystepper import Stepper
>>> mystepper = Stepper()
>>> mystepper.rotate(180, 10) # Rotates motor 180 degrees at 10 RPM
>>> mystepper.rotate(-180, 5) # Rotates motor back 180 degrees at 5 RPM
>>> mystepper.angle
0.0
```


## Notes

  * By default the GPIO pins used are P8_13, P8_14, P8_15, and P8_16. These can be changed by modifying the `Stepper.pins` list.

  * By default the `Stepper.steps_per_rev` parameter is set to 2048 to match my motor (it has a built-in gearbox).

  * The code doesn't keep track of where it ends in the sequence of pins. It simply sets all pins low after a move. This means there could be some additional error in the `Stepper.angle` variable if the amount of steps moved is not divisible by 4.


## Final Thoughts

As mentioned previously, half-stepping would be a nice future add-on, along with
a more accurate way of keeping track of the motor shaft angle. Another logical
next step would be to use one of the BBB's Programmable Real-Time Units (PRUs)
to control the timing more precisely, therefore improving speed accuracy and
allowing synchronization with other processes, e.g. data acquisition. However,
for now this simple method gets the job done.
