# What does River Architect?

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

Download the complete program file directory tree from  @ https://github.com/sschwindt/RiverArchitect/tree/master/RiverArchitect

Or download particular modules; note that all modules require the .site_packages/ and the 01_Conditions/ folders.

Please read the user manual in 00_Documentation / RiverArchitect_Manual.pdf for notes on how to setup and use River Architect.


# About
The code was developed based on data from California's Yuba River and example results can be downloaded.

Future developments will focus on improving the GUI, developing the ModifyTerrain module for automating
terraforming planning, and providing a version that works with QGIS's Python core.

Do not hesitate to contact sschwindt [at] ucdavis.edu and gpast [at] ucdavis.edu for reporting bugs,
   suggestions, or any feedback.


# Contributing

Do not hesitate to contact sschwindt [at] ucdavis.edu and gpast [at] ucdavis.edu with suggestions or any feedback.

Bug reports, feature requests, and pull requests are welcome on GitHub at https://github.com/sschwindt/RiverArchitect .


[1]: https://www.sciencedirect.com/science/article/pii/S0301479718312751 "Lifespan mapping"
