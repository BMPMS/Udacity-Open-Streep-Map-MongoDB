The aim of this project is to analyse and clean OpenStreetMap data from my local area and then perform a data query.

The code for this project is split into several python files as follows:

* **iterative.py** - checks unique tags to get an idea of the size and shape of the streetmap data
* **getusers.py** - counts the number of users
* **tagtypes.py** - check the ‘k’ value of the tags and check in case there were any weird tags which wouldn’t work as keys in Mongo DB or whether I was unintentionally missing any key data.
* **audit.py** - looks at the street names for inconsistencies.
* **mung1.py** - transfers the data into MongoDB
* **mongo.py** - queries the MongoDB database
* **mongoclean.py** - performs the data cleaning according to the plan.

This was a learning project.  Having gone through the process I concluded that it would have been easier to import the data into MongoDB earlier - next time!
