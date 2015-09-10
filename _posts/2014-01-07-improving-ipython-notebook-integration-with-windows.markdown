---
comments: true
date: 2014-01-07 20:58:04+00:00
layout: post
title: Improving IPython Notebook integration with Windows
tags:
- Python
---

<img class="float-right no-border" src="/images/ipython-windows-context-menu.png">


By default, the awesomely useful and fun [IPython Notebook](http://ipython.org/notebook.html) does not integrate with Windows so seamlessly. A console and then the notebook server must be opened in the proper directory in order to open a new or existing notebook. These extra steps make the IPython Notebook slightly less ideal for quickly jotting down ideas—one of its greatest uses!

Not to fear, however, as the Windows Registry can easily be modified to

  1. Open notebooks directly from Windows Explorer.
  2. Create a shortcut to launch the IPython Notebook server within the current directory.

Simply download and run [ipython.reg](https://drive.google.com/file/d/0BwMVIAlxIxfZVEZoUGpRVWdTTmM/edit?usp=sharing) to add the entries shown below to your registry automatically.

These entries were put together from instructions located [here](http://www.howtogeek.com/107965/how-to-add-any-application-shortcut-to-windows-explorers-context-menu/). A similar solution can also be found [here](http://cyrille.rossant.net/start-an-ipython-notebook-server-in-windows-explorer/).

```bat
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\ipynb]
@="Open IPython Notebook server here"

[HKEY_CLASSES_ROOT\Directory\Background\shell\ipynb\command]
@="\"C:\\Python27\\Scripts\\ipython.exe\" \"notebook\" \"%V\""

[HKEY_CLASSES_ROOT\Directory\shell\ipynb]
@="Open IPython Notebook server here"

[HKEY_CLASSES_ROOT\Directory\shell\ipynb\command]
@="\"C:\\Python27\\Scripts\\ipython.exe\" \"notebook\" \"%V\""

[HKEY_CLASSES_ROOT\ipynb_auto_file\shell\open\command]
@="\"C:\\Python27\\Scripts\\ipython.exe\" \"notebook\" \"%1\""
```
