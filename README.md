---------------------------------------
 river-architect / README.txt
---------------------------------------

River Architect is a Python 2 - based open-source package that supports stream designers with a set of 
GUI modules. The current core functionalities are:

 - Lifespan mapping of stream design features according to Schwindt et al. (2019): 
					https://www.sciencedirect.com/science/article/pii/S0301479718312751 .
 - Calculating terraforming activities (mass differences and simple terrain modifications).
 - Habitat quality evaluations for various aquatic species.
 - Project cost - benefit assessments.

The requirements are:

 - Digital terrain elevation models (DEMs).
 - 2D hydrodynamic modeling of multiple steady discharge scenarios.
 - ESRI ArcGIS licenses for SpatialAnalyst.
 - Batchfile launches are designed for working on any Windows platform.

The code was developed based on data from California's Yuba River and example results can be downloaded.

Future developments will focus on improving the GUI, developing the ModifyTerrain module for automating
terraforming planning, and providing a version that works with QGIS's Python core.


---------------------------------------
 MISC COMMENTS AND SUGGESTIONS
---------------------------------------

 - Please read the user manual in 00_Documentation / RiverArchitect_Manual.pdf for notes on how to setup
   and use River Architect.
   
 - Do not hesitate to contact sschwindt [at] ucdavis.edu and gpast [at] ucdavis.edu for reporting bugs,
   suggestions, or any feedback.

   
---------------------------------------
 Thank you for using River Architect
---------------------------------------
