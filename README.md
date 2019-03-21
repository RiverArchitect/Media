# River Architect ![logo](https://github.com/sschwindt/RiverArchitect/raw/master/images/logo_small.ico)
River Architect is a Python 2 - based open-source package that supports stream designers with a set of 
GUI modules. The current core functionalities are:

 * Lifespan mapping of stream design features according to [Schwindt et al. (2019)][1] with the LifespanDesign and MaxLifespan modules.   
 
 * Calculate terraforming activities (mass differences and simple terrain modifications) with the ModifyTerrain module.
 
 * Evaluate habitat quality for various aquatic species with the HabitatEvaluation module.
 
 * Assess project cost-benefit with the ProjectMaker module.

# Requirements

 * Digital terrain elevation models (DEMs).
 
 * 2D hydrodynamic modeling of multiple steady flow scenarios.
 
 * ESRI ArcMap and licenses for SpatialAnalyst (coming soon: update for ArcPro and Python 3).
 
 * Batchfile launches are designed for working on any Windows platform.


# How to use it?
The quick version: Download [River Architect][5], right-click on [Start_River_Architect.bat][1] and open this batchfile in a text editor. Ensure that the file points to the correct python interpreter (ArcMap's python.exe -- typically stored in C:\Python27\ArcGISx6410.6\). Save edits, close the batchfile and double-click on it to launch River Architect.

The robust version:
1) Download the complete program file directory from [GitHub][2] (or [sample data][4]). 
2) Get started using the manual ([direct download link][3]) with the instructions in section 3 (Getting started). 
4) Run the packages for stream design (package overview in section 1 of the [documentation][3])


# About
The code was developed based on data from California's Yuba River and example results can be downloaded.

Future developments will focus on improving the GUIs, developing the ModifyTerrain module for automating
terraforming planning, and migrating to QGIS's Python core.


# Contributing
Do not hesitate to contact sschwindt [at] ucdavis.edu and gpast [at] ucdavis.edu for reporting bugs, suggestions, or any feedback.

Bug reports, feature requests, and pull requests are welcome on GitHub at https://github.com/sschwindt/RiverArchitect .


[1]: https://www.sciencedirect.com/science/article/pii/S0301479718312751 "Lifespan mapping"
[2]: https://github.com/sschwindt/RiverArchitect_development
[3]: https://github.com/sschwindt/RiverArchitect_development/blob/master/00_Documentation/CodeDocumentation.pdf
[4]: https://www.dropbox.com/s/pv9n2y0nmulidme/RiverArchitect_with_Example.zip?dl=0
[5]: https://github.com/sschwindt/RiverArchitect_development/archive/master.zip
