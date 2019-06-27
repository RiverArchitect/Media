# River Architect ![logo](https://github.com/sschwindt/RiverArchitect/raw/master/images/logo_small.ico)
[River Architect](https://github.com/RiverArchitect/Welcome/raw/master/docs/RiverArchitect.pdf) is a Python3-based open-source code that supports river designers with a set of GUI modules. Sample data can be downloaded [here](https://github.com/RiverArchitect/SampleData/archive/master.zip). The current core functionalities are:

 * Lifespan mapping of stream design features according to [Schwindt et al. (2019)][1] with the [LifespanDesign](https://github.com/RiverArchitect/Welcome/wiki/LifespanDesign) and [MaxLifespan](https://github.com/RiverArchitect/Welcome/wiki/MaxLifespan) modules.   

 * Terraforming concepts with the [ModifyTerrain](https://github.com/RiverArchitect/Welcome/wiki/ModifyTerrain) module using threshold value-based DEM modifications or the sophisticated [River Builder](https://github.com/RiverArchitect/Welcome/wiki/RiverBuilder).

 * Evaluate ecohydraulic and morphological site and river assets within the Eco-Morphology modules for [calculating Seasonal Habitat Area](https://github.com/RiverArchitect/Welcome/wiki/SHArC) and optimizing [habitat connectivity](https://github.com/RiverArchitect/Welcome/wiki/Connectivity).

 * Generate construction plans, cost estimates, and variant efficiency metrics with the [ProjectMaker](https://github.com/RiverArchitect/Welcome/wiki/ProjectMaker) module.
 
 * Produce high-quality maps with *River Architect*'s built-in [Mapping routines](https://github.com/RiverArchitect/Welcome/wiki/Mapping).



# Requirements

 * Digital terrain elevation models (DEMs).

 * 2D hydrodynamic modeling of multiple steady flow scenarios.

 * Esri's *ArcPro* *Python* environment with *SpatialAnalyst* license (Windows only).



# Installation and Quick Usage
The quick version: Download [River Architect][5] and double-click on [Start_River_Architect.bat][1]. Modifications of the batchfile might be required, for example, to fit the conda environment. The standard environment is `"%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy"`, which typically refers to `"C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat"`. ArcGIS provides more information on running stand-alone Python scripts on their [website](https://pro.arcgis.com/en/pro-app/arcpy/get-started/using-conda-with-arcgis-pro.htm).

The robust version:

 1. Download the program file directory from [GitHub][2] (or [sample data][4]). 
 1. Follow the detailed [Installation][6] instructions for setting up the Environment.
 1. Read the [Signposts][7] to learn about the terminology used in *River Architect* and create river [*Conditions*](https://github.com/RiverArchitect/Welcome/wiki/Signposts#new-condition) with the [GetStarted](https://github.com/RiverArchitect/Welcome/wiki/Signposts#getstarted) module to start analyses. 
 1. The application of *River Architect*'s modules are described on their Wiki pages:
   * Lifespan mapping
     + [Lifespan and Design map creation](https://github.com/RiverArchitect/Welcome/wiki/LifespanDesign)
     + [Best Lifespan identification](https://github.com/RiverArchitect/Welcome/wiki/MaxLifespan)
   * Terraforming
     + [ModifyTerrain](https://github.com/RiverArchitect/Welcome/wiki/ModifyTerrain)
     + [Volume Assessment (earthworks)](https://github.com/RiverArchitect/Welcome/wiki/VolumeAssessment)
   * Eco-Morphology
     + [SHArC (Seasonal Habitat Area Calculator)](https://github.com/RiverArchitect/Welcome/wiki/SHArC)
     + [Connectivity Analyses](https://github.com/RiverArchitect/Welcome/wiki/Connectivity)
   * [ProjectMaker](https://github.com/RiverArchitect/Welcome/wiki/ProjectMaker)


In addition to the module descriptions, the [*River Architect* Wiki](https://github.com/RiverArchitect/Welcome/wiki) also provides detailed solutions for [Troubleshooting](https://github.com/RiverArchitect/Welcome/wiki/Troubleshooting).

Please note that *River Architect* has undergone important changes since the last stable Python2 version ([download last stable Python2-River-Architect][8]).

# Documentation
An overview presentation can be downloaded [here](https://github.com/RiverArchitect/Welcome/raw/master/docs/RiverArchitect.pdf). The usage of River Architect is described in the [*River Architect*'s Wiki][3].


# About
The code was developed based on data from California's Yuba River and example results can be downloaded.

Future developments will focus on improving the GUIs, developing the ModifyTerrain module for automating
terraforming planning, and migrating to QGIS's Python core.


# Contributing
Do not hesitate to contact river.architect.program [at] gmail.com for reporting bugs, suggestions, or any feedback.

Bug reports, feature requests and pull requests are welcome ([submit here](https://github.com/RiverArchitect/Welcome).

# Acknowledgment
*River Architect* is the result of research projects funded by

 - The [Yuba County Water Agency](https://www.yubawater.org/) (Marysville, California, USA) under Award #201016094 and Award #10446), and
 - The [USDA National Institute of Food and Agriculture](https://nifa.usda.gov/), Hatch project number CA-D-LAW-7034-H.


[1]: https://www.sciencedirect.com/science/article/pii/S0301479718312751 "Lifespan mapping"
[2]: https://github.com/sschwindt/RiverArchitect_development
[3]: https://github.com/RiverArchitect/Welcome/wiki
[4]: https://www.dropbox.com/s/pv9n2y0nmulidme/RiverArchitect_with_Example.zip?dl=0
[5]: https://github.com/sschwindt/RiverArchitect_development/archive/master.zip
[6]: https://github.com/RiverArchitect/Welcome/wiki/Installation
[7]: https://github.com/RiverArchitect/Welcome/wiki/Signposts
[8]: https://www.dropbox.com/s/8d6c096r4ouzxy2/RiverArchitect_Py2.zip?dl=0
