Welcome to the River Architect ![logo](https://github.com/RiverArchitect/Welcome/raw/master/images/logo_small.ico) Wiki
======================================================
<details><summary> Table of Contents </summary><p>

1. [Setup River Architect][1]
   - [Installation](Installation#started)
   - [Program file structure](Installation#structure)
   - [Requirements](Installation#req)
   - [Logfiles](Installation#logs)
1. [Get started, terminology and signposts][2]
   - [Welcome and **Condition** creation](Signposts#getstarted)
       + [Create *Condition*s](Signposts#new-condition)
	   + [Analyze Flows](Signposts#ana-flows)
	   + [Input definition files](Signposts#inpfile)
	   + [Map extent definition files](Signposts#inmaps)
   - [Geofile conventions](Signposts#terms)
   - [Prepare input Rasters](Signposts#inputs)
1. Modules
   - Lifespans
       * The [`LifespanDesign` module][3] maps sustainable [features](River-design-features)
         + [Parameter hypothesis](LifespanDesign-parameters)
         + [River design and restoration **features**](River-design-features)
         + [Input definition files](Signposts#inpfile)
         + [Code extension and modification](LifespanDesign-code)
       * Identification of best-performing [features](River-design-features) with the [`MaxLifespan` module][4]
         + [Quick GUIde](MaxLifespan#actgui)
         + [Working principles](MaxLifespan#actprin)
         + [Code extension and modification](MaxLifespan#actcode)
   - Morphology (Terraforming)
       * [River **Reach** definitions](RiverReaches)
       * [[ModifyTerrain]]
           + [Quick GUIde](ModifyTerrain#mtgui)
           + [Threshold-based Grading or Widening (Broaden)](ModifyTerrain#mtdemmod)
           + [River Builder](RiverBuilder)
           + [Working principle](ModifyTerrain#mtprin)
           + [Code extension and modification](ModifyTerrain#mtcode)
       * [[VolumeAssessment]]
           + [Quick GUIde](VolumeAssessment#gui)
           + [Working principle](VolumeAssessment#vaprin)
           + [Set level of detection](VolumeAssessment#vacode)
   - Ecohydraulics
       * Assess habitat area with the [`SHArC` module][6]
           + [Quick GUIde](SHArC#hegui)
           + [Define **Aquatic Ambiances** for **Fish**](SHArC#hefish)
           + [**SHArea** calculation](SHArC#herunSHArea)
           + [Working principles](SHArC-working-principles#heprin)
           + [Predefined **Fish** species](SHArC#hefish)
           + [Edit Fish template](aqua-modification#hecode)
       * [Habitat Connectivity](Connectivity)
           + Wiki pending.
       * Make eco-morphological assessments of river conditions with the [`EcoMorphology` module][60]
           + Implementation pending.
   - [`ProjektMaker`][7] generates cost-benefit plans and tables of river designs
     * [Quick GUIde](ProjectMaker#pmquick)
     * [**Cost** quantity assessment](ProjectMaker#pmcq)
     * [Ecological (habitat) benefit assessment (Calculate **SHArea**)](ProjectMaker#pmSHArea)
   - [`Tools`][8] contain beta-version routines (under development)
1. [FAQ][9]
1. [Troubleshooting and Error message handling][10]
     * [Known issues](Troubleshooting#issues)
     * [How to troubleshoot](Troubleshooting#howto)
     * [Error messages](Troubleshooting#error-messages)
     * [Warning messages](Troubleshooting#warning-messages)

</p></details>

***

[*River Architect*](https://github.com/RiverArchitect/Welcome/raw/master/docs/RiverArchitect.pdf) serves for the GIS-based planning of habitat enhancing river design features regarding their lifespans, parametric characteristics, optimum placement in the terrain, and ecological benefit. A main graphical user interface (GUI) provides five modules for generating lifespan and design maps, action (optimum lifespan) maps, terrain modification (terraforming) assessment of digital elevation models (DEM), habitat evaluation, and project cost-benefit analyses.

*River Architect* invites to analyses and modifications of the longevity and ecological quality of riverscapes. Different planning bases ("conditions") can be easily created using an introductory module called **[GetStarted](Signposts#getstarted)**. **Lifespan**, **Morphology (Terraforming)** and **Ecohydraulic** assessments can then be created on the basis of the *Conditions*, including the creation of project plans and cost tables with a **Project Maker** module.

[**Lifespan**][3] maps indicate the expected longevity of restoration features as a function of terrain change, morphological characteristics, and 2D hydrodynamic modeling results. **Design maps** are a side product of [lifespan and design mapping][3] and indicate required feature dimensions for stability, such as the minimum required size of angular boulders to avoid their mobilization during floods (more information in [Schwindt et al.2019][11]). **Best lifespan maps** result from the comparison of lifespan and design maps of multiple restoration features and assign features with the highest longevity to each pixel of a raster. Thus, the [**Max Lifespan**][4] module assess optimum features as a function of highest lifespans among comparable feature groups such as terraforming or vegetation planting species.

**Morphology (Terraforming)** includes routines to [**Modify Terrain**][5] for river restoration purposes. Currently, two terrain modification algorithms are implemented: (1) Threshold value-based terrain modifications in terms of [grading](River-design-features#grading) or [widening / broaden rivers](River-design-features#berms) for riparian forest establishment; and (2) [River Builder](RiverBuilder) for the creation of synthetic river valley. A **[Volume Assessment](VolumeAssessment)** module can compares an original (pre-project or pre-terraforming application) and a modified DEM (\"with implementation\" or post-feature application) to determine required earth movement (terraforming volumes) works.

**Ecohydraulics** assessments include the evaluation of the ecohydraulic state and connectivity of riverscapes. The **[Habitat Area](SHArC)** (Seasonal Habitat Area Calculator) module applies user-defined flows (discharges) for the spatial evaluation of the habitat suitability index (*HSI*) in terms of Seasonal Habitat Area (SHArea). The hydraulic habitat suitability results from 2D hydrodynamic numerical model outputs of flow depth and velocity. In addition, a  \"cover\" option can be used to assess ecohydraulic effects of cobble, boulder, vegetation, and streamwood. The **[Habitat Connectivity](Connectivity)** module provides insights into the connection of wetted areas on floodplains and how these may be improved to enhance the survivorship of fry / juvenile fish.

The [**Project Maker**][7] module creates preliminary construction plans and evaluates the costs for gain in usable habitat for target fish species and lifestages. A unit cost workbook provides relevant costs and the gain in usable habitat area results from the *SHArC* module.

A set of [**Tools**][8] provides *Python* console scripts that are under development and will be implemented in future versions of the *River Architect* GUI.

*River Architect* represents a comprehensive tool for state-of-the-art planning of ecologic river modifications. The integrated application of *River Architect* to habitat enhancing project planning is illustrated in the following flowchart. 
The modules and tool-scripts can also be individually applied for other purposes than suggested in the flowchart.

![flowchart](https://github.com/RiverArchitect/Welcome/raw/master/images/flowchart.png)

The procedure of project design following the flowchart involves the following steps:

1.  Generate a terrain elevation model (DEM).

2.  Determine relevant discharges for 2D hydrodynamic modeling:

    -   At least three annual discharges describing the \"most of the time\" - situation of the considered river for habitat evaluation assessments. *River Architect*'s *Tools* contain scripts for generating flow duration curves from gaging station data.

    -   At least three flood discharges against which potential [restoration features](River-design-features) have to withstand (determine lifespan intersects).

3.  Run a 2D hydrodynamic model (steady) with all determined discharges to generate hydraulic snap-shots of the river.

4.  Create a [Condition](Signposts#conditions) using the [GetStarted](Signposts#getstarted) module. The *Condition* should include *GeoTIFFs* of the initial (existing or pre-project) river state:

    -   A detrended digital elevation model (DEM);

    -   Flow depth and velocity for multiple discharges Rasters from 2D hydrodynamic modeling (see [Signposts](Signposts#conditions));

    -   A substrate map (`dmean` for metric or `dmean_ft` for U.S. customary units); relevant methods are described in [Detert et al. (2018)][12]; [Stähly et al. (2017)][13]; and [Jackson et al. (2013)][14];

    -   Datasets that can be used to assess design feature stability, such as [side channel design criteria](River-design-features#sidechnl);

    -   Topographic change Rasters (Topographic Change Detection or DEM differencing according to [Wyrick and Pasternack 2016][15]);

    -   A depth to groundwater table Raster (`d2w`);

    -   A morphological unit Raster (see [Wyrick and Pasternack (2014)][16]).

5.  Apply the [*LifespanDesign*][3] module to [framework (terraforming) features](River-design-features#featoverview).

6.  Lifespan and Design maps, as well as expert assessment, serve for the identification of relevant [framework (terraforming) features](River-design-features#featoverview).

7.  Iterative terraforming (if relevant):

    -   Use the [*ModifyTerrain*][5] module for creating synthetic river valley with [River Builder](RiverBuilder); or apply threshold value-based terrain [grading](River-design-features#grading) or [broadening of the river bed](River-design-features#berms). *Please note that both routines require post-processing with computer-aided design (translation into real world coordinates and / or edge smoothing).*

    -   Re-compile the flow depth and velocity maps (re-run 2D model) with the modified DEM.

    -   Verify the suitability of the modified DEM (e.g., barrier height to ensure flood safety and habitat suitability with the [[SHArC]] module); if the verification show weaknesses adapt the terraforming and re-compile the flow depth and velocity maps until terraforming is satisfactory.

    -   Use the *[[VolumeAssessment]]* module (Morphology tab) to compare pre- (initial) and post-project (modified) DEMs for determining required excavation and fill volumes.

8.  Apply the [*LifespanDesign*][3] module to [vegetation plantings](River-design-features#plants) and [(other) bioengineering features](River-design-features#bioeng) based on the terraformed DEM (or the original / initial DEM if no terraforming applies).

9.  Use the [*MaxLifespan*][4] module to identify best performing (highest lifespan) [vegetation plantings](River-design-features#plants) and [(other) bioengineering features](River-design-features#bioeng).

10. If the soils are too coarse (i.e., the capillarity is not high enough to enable plant root growth), apply the connectivity feature ["incorporate fine sediment in soils"](River-design-features#finesed).

11. If gravel augmentation methods are applicable: Consecutively apply the [*LifespanDesign*][3] and [*MaxLifespan*][4] modules to [connectivity features](River-design-features#featoverview) to foster self-sustaining, artificially created ecomorphological patterns within the terraforming process.\
    If gravel is added in-stream, re-run the numerical model for the assessment of [gravel stability](River-design-features#rocks) with the [*LifespanDesign*][3] module and the combined habitat suitability with the [*SHArC*][6] module to compare the [**S**easonal **H**abitat **Area** (**SHArea**)](SHArC#herunSHArea) before and after enhancement of [Aquatic Ambiances for target fish species (lifestages)](SHArC#hefish).

12. Use the [*SHArC*][6] to assess the *"existing"* (pre-project) and *"with implementation"* (post-project) habitat suitability in terms of annually usable habitat area (SHArea).

13. Use the *[[ProjectMaker]]* to calculate costs, the net gain in SHArea, and their ratio as a metric defining the project trade-off.

The working principles of the [*LifespanDesign*][3], [*MaxLifespan*][4], [*ModifyTerrain*][5], *[[VolumeAssessment]]*, [*SHArC*][6], and [*ProjectMaker*][7] modules are explained on their own Wiki pages. The differentiation between [terraforming (framework)](River-design-features#featoverview), [vegetation plantings and other bioengineering](River-design-features#featoverview), and [connectivity features](River-design-features#featoverview) is described within the [LifespanDesign Wiki](River-design-features). The [[Installation]] Wiki pages describe the propper installation, file organization and environment of *River Architect*.

***

[1]: https://github.com/RiverArchitect/Welcome/wiki/Installation
[2]: https://github.com/RiverArchitect/Welcome/wiki/Signposts
[3]: https://github.com/RiverArchitect/Welcome/wiki/LifespanDesign
[4]: https://github.com/RiverArchitect/Welcome/wiki/MaxLifespan
[5]: https://github.com/RiverArchitect/Welcome/wiki/ModifyTerrain
[6]: https://github.com/RiverArchitect/Welcome/wiki/SHArC
[60]: https://github.com/RiverArchitect/Welcome/wiki/EcoMorphology
[7]: https://github.com/RiverArchitect/Welcome/wiki/ProjectMaker
[8]: https://github.com/RiverArchitect/Welcome/wiki/Tools
[9]: https://github.com/RiverArchitect/Welcome/wiki/FAQ
[10]: https://github.com/RiverArchitect/Welcome/wiki/Troubleshooting
[11]: https://www.sciencedirect.com/science/article/pii/S0301479718312751
[12]: http://www.sciencedirect.com/science/article/pii/S1001627918300350
[13]: https://ascelibrary.org/doi/abs/10.1061/%28ASCE%29HY.1943-7900.0001286
[14]: http://www.yubaaccordrmt.com/Annual%20Reports/Mapping%20and%20Modeling/LYRsubstrate20131218.pdf
[15]: https://onlinelibrary.wiley.com/doi/full/10.1002/esp.3854
[16]: http://www.sciencedirect.com/science/article/pii/S0169555X14000099
