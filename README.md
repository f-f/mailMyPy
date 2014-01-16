mailMyPy
========

This is a simple script for auto-reply to emails matching your templates.

###Dependencies

This script runs on python3 and is written for the purpose of running as a cronjob.
To run it you'll need: **python3**, **lxml**, **postgresql** and **sqlalchemy**.

### Usage

To run it from the shell you simply need to cd to the project directory and then run 
	
	python3 main.py


Or, you can throw it in a cronjob:
First create a shell file in your home, and insert the following lines:
	
	#!/bin/bash
	cd /the/path/to/the/code/mailMyPy
	python3 main.py

From the shell run:

	crontab -e

Then append to the file:

	*/5 * * * * /home/$USER/mailMyPyCron.sh

(This is for 5 minutes interval, for more info run "man crontab")

### Further Improvements

For now it's stable for this basic usage, but it could be expanded in some directions to make it a powerful tool.
More on this soon.
