Use (or not use) on your own risk. I made it for myself.

It is a desktop editor for  ARF (artinoise re.corder fingering) slapped together with duct tape and python code in haste.

I found very inconvenient to use phone app for extensive fingering system editing, some wrote this.


At the moment of version 0.0.3:


* Editing basically works. Can edit and export ARF files, and name them.
* I was able to make my own fingering that suites me, and it works fine on flute.
* It does not support keyboard mode fingerings, whatever they are.


UI is ugly as hell, but is tuned to fit  two running editors into one HD 1920x1080 so you can compare two fingering systems,
and should be simple enough to be usable.


Editor warns  you on:

1) amount of positions (variations)   which should be not more than 62 to work.
2) positions collisions (same positions for different notes) 

However editor does not enforce them.
It is up to you to fix these problems before uploading. 

P.S. 

Also, notes with positions (variants) containing only open holes are considered to be non existent.
So if you intend to delete "A#0" you just make sure it contains only one position with all holes being white.


Editor cannot upload ARF files yet, use stock app for that. 
In case if your new changes do not seem to apply, try to import under a different name.




Actual compiled editor binary to run on Windows can be downloaded here:

https://github.com/ignis32/artinoise_recorder_fingering_editor/releases


Others can probably launch from the code, using something like 

"python FingeringEditor.py"

