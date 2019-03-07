# River Architect ![logo](https://github.com/sschwindt/RiverArchitect/raw/master/images/logo_small.ico)
River Architect is a Python 2 - based open-source package that supports stream designers with a set of 
GUI modules. The current core functionalities are:

 * Lifespan mapping of stream design features according to [Schwindt et al. (2019)][1].
    + Modules: LifespanDesign and MaxLifespan
 * Calculating terraforming activities (mass differences and simple terrain modifications).
    + Module: ModifyTerrain
 * Habitat quality evaluations for various aquatic species.
    + Module: HabitatEvaluation
 * Project cost-benefit assessments.
    + Module: ProjectMaker

# Requirements

 * Digital terrain elevation models (DEMs).
 * 2D hydrodynamic modeling of multiple steady discharge scenarios.
 * ESRI ArcGIS licenses for SpatialAnalyst.
 * Batchfile launches are designed for working on any Windows platform.


# How to use it?

1) Download the complete program file directory tree as zip. 

2) The main programm and modules are contained in the [RiverArchitect/RiverArchitect/][2] directory.

3) Open the manual ([direct download link][3]) and follow the instructions in section 3 (Getting started)

4) Run the packages for stream design (package overview in section 1 of the [manual][3])


# About
The code was developed based on data from California's Yuba River and example results can be downloaded.

Future developments will focus on improving the GUIs, developing the ModifyTerrain module for automating
terraforming planning, and migrating to QGIS's Python core.


# Contributing
Do not hesitate to contact sschwindt [at] ucdavis.edu and gpast [at] ucdavis.edu for reporting bugs, suggestions, or any feedback.

Bug reports, feature requests, and pull requests are welcome on GitHub at https://github.com/sschwindt/RiverArchitect .


[1]: https://www.sciencedirect.com/science/article/pii/S0301479718312751 "Lifespan mapping"
[2]: https://github.com/sschwindt/RiverArchitect/tree/master/RiverArchitect
[3]: https://github.com/sschwindt/RiverArchitect/blob/master/RiverArchitect/00_Documentation/RiverArchitect_Manual_v01.pdf
