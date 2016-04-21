# pyLog-GTK
Simple Logbook, written in python3.4 using GTK3


Entries are stored into, and retrived from pylog.dat

All entries are stored to a simple dictionary structure, where key is the time when its created, and title, and content are stored into a tuple in the dictionary. The dictionary are then written to file, using pickle.dump.

Window is a 2 tabbed notebook, where first tab is used to view entries, and second tab is used to append entries to list.
