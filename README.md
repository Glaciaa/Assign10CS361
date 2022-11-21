# Assign10CS361

This code can be run in visual studio 2019 if you open it via the .sln file. You will need to run both programs at the same time,
which can be done with the commands

py module1.py

and

py Assign10.py

module1.py is the microservice that was created by my partner. I have been working with him to modify the code slightly to make it fit
better with my project. 

At the moment, the issue is that the program will freeze and crash whenever attempting to receive data from a message queue. I am
using tkinter and rabbitmq in python to attempt this. At the moment, I am really struggling to find a way to allow my original program
(Assign10.py) to receive data at all, so any guidance on this issue would be very helpful. 

To recreate this issue, click the import button at the top right of the window when running Assign10.py. This will call the "acceptInput"
function, which tries to receive a note from the microservice.
