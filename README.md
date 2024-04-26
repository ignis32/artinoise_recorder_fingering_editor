Use (or not use) on your own risk. I made it for myself.

It is a desktop editor for  ARF (artinoise re.corder fingering) slapped together with duct tape and python code in haste.

I found very inconvenient to use phone app for extensive fingering system editing, therefore here it this.


At the moment of version 0.0.6:


* Editing basically works.
* Can  open, edit and export ARF file.
* Give a name to the fingering system
* You can modify positions by clicking on holes.
* You can create multiple positions for one note, or delete positions
* I was able to make my own fingering that suites me, and it works fine on my re.corder.
* It does not support keyboard mode fingerings, whatever they are.

UI is ugly as hell, but is tuned to fit  two running editors into one HD 1920x1080 monitor, so you can compare two fingering systems.
 
Editor warns  you on:
1) amount of positions (variations)   which should be not more than 62 to work, due to limitations of re.corder
2) positions collisions (overlaping positions for different notes, in other words when you tried to assign same combination of holes state to multiple notes).
However editor does not enforce them.
It is up to you to fix these problems before uploading, as phone artinoise app would decline such fingering file.

P.S. 

Also, notes with positions (variants) containing only open holes are considered to be non existent. 
Additionaly, it means that re.corder does not actually accept all-open-hole position as a real playable position by design.
So if you intend, for example to delete "A#0" (it is not a part of your fingering system) you just make sure it contains only one position with all holes being white (open).


Editor cannot upload ARF to re.corder files yet, use stock phone app for that. 
In case if your new changes do not seem to apply, try to import under a different name (fingering system name, not file name).
Phone app at the moment does not seem capable of deleting fingerings, but it can reset list of fingerings to default, removing all custom ones.


Actual compiled editor binary to run on Windows (made with pythoninstaller) can be downloaded here:

https://github.com/ignis32/artinoise_recorder_fingering_editor/releases


Others can probably launch from the code, using something like 

"python FingeringEditor.py"

But I actually have not tried that on other OSes yet.



"Print" function creates a png image with all the positions and their notes from your current fingering system. And puts it to "img/" folder, named after fingering system name .
This image is A4 sized, and it's intended purpose is to be printed.
