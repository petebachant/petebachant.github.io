---
comments: true
date: 2013-08-24 23:57:47+00:00
layout: post
slug: automatic-email-openfoam
title: Automatically receive an email when an OpenFOAM simulation is complete
categories:
- OpenFOAM
- Python
tags:
- Automation
- CFD
- OpenFOAM
- Python
---

OpenFOAM runs can take a long time. Wouldn't it be nice to know when a
simulation is done without having to keep checking the terminal? As it turns
out, this is very easy to set up with Python (I got most of the code I used from
[here](http://alextrle.blogspot.com/2011/05/how-to-send-sms-message-with-python.html),
which details how to send an SMS). Simply create a script called `send_email.py`
in the OpenFOAM case directory that looks like this:

```python
#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("<username>", "<password>")

msg = MIMEText("The simulation is complete.")
msg["Subject"] = "Simulation finished"
msg["From"] = "Me"
msg["To"] = "Me"

server.sendmail("Me", "my_email_address@gmail.com", msg.as_string())
```

Replace all the relevant info with your own. Note that this assumes you're using
Gmail, but it can be adapted to any SMTP server. The script could also be
expanded to email team members, extract information about the run, etc.

Change the permissions such that the file can be executed as a program, then at
the bottom of your `Allrun` script add

    python send_email.py

Voila. Now you'll get an email when your simulation finishes, and can go off and
be productive elsewhere in the meantime.
