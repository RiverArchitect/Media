from __future__ import division  # required to enforce correct division
# all classes log to "habitat_enhancement" logger
try:
    import sys, os, logging
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, logging).")

try:
    import arcpy
    from arcpy.sa import *
except:
    print("ExceptionERROR: No valid arcpy found.")

try:
    # import own module classes
    import cHabitatIO as chio
    import cFish as cf

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\.site_packages\\riverpy\\")
    import fGlobal as fg

except:
    print("ExceptionERROR: Missing RiverArchitect packages (required: cHabitatIO, RP/fGlobal).")


class CHSI:
    def __init__(self, hab_condition, cover_applies, unit):
        self.cache = os.path.dirname(os.path.abspath(__file__)) + "\\.cache\\"
        self.condition = hab_condition
        self.combine_method = "geometric_mean"
        self.cover_applies = cover_applies  # BOOL
        self.logger = logging.getLogger("habitat_evaluation")

        self.path_condition = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\01_Conditions\\" + self.condition + "\\"
        self.path_hsi = os.path.dirname(os.path.abspath(__file__)) + "\\HSI\\" + str(self.condition) + "\\"
        if self.cover_applies:
            p_ext = "cover"
        else:
            p_ext = "no_cover"
        self.path_csi = os.path.dirname(os.path.abspath(__file__)) + "\\CHSI\\" + str(self.condition) + "\\" + p_ext + "\\"
        self.path_wua_ras = os.path.dirname(os.path.abspath(__file__)) + "\\WUA\\Rasters\\" + str(self.condition) + "\\" + p_ext + "\\"
        fg.chk_dir(self.cache)
        fg.chk_dir(self.path_csi)
        fg.chk_dir(self.path_wua_ras)

        self.unit = unit
        if self.unit == "us":
            self.u_length = "ft"
            self.u_discharge = "cfs"
            self.ft2ac = 1 / 43560
        else:
            self.u_length = "m"
            self.u_discharge = "m3"
            self.ft2ac = 1

        self.xlsx_out = ""

    def calculate_wua(self, wua_threshold, fish):
        # wua_threshold =  FLOAT -- value between 0.0 and 1.0
        # fish = DICT -- fish.keys()==species_names; fish.values()==lifestages
        arcpy.CheckOutExtension('Spatial')
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.path_csi
        arcpy.env.extent = "MAXOF"
        self.logger.info(" >> Retrieving CHSI rasters ...")
        csi_list = arcpy.ListRasters()
        cc = 0  # appended in cache to avoid overwriting problems
        for species in fish.keys():
            for ls in fish[species]:
                self.logger.info(" -- Usable Area FOR " + str(species).upper() + " - " + str(ls).upper())
                fish_shortname = str(species).lower()[0:2] + str(ls[0])
                if self.cover_applies:
                    xsn = self.condition + "_" + fish_shortname + "_cov.xlsx"
                else:
                    xsn = self.condition + "_" + fish_shortname + ".xlsx"

                xlsx_name = os.path.dirname(os.path.abspath(__file__)) + "\\WUA\\" + xsn
                xlsx = chio.Write()
                xlsx.open_wb(xlsx_name, 0)

                Q = xlsx.read_column("B", 4)
                self.logger.info(" >> Reducing CHSI rasters to WUA threshold (" + str(wua_threshold) + ") ...")
                for csi in csi_list:
                    self.logger.info("    -- CHSI raster: " + str(csi))
                    if fish_shortname in str(csi):
                        ras_csi = arcpy.Raster(self.path_csi + str(csi))
                    else:
                        continue
                    dsc = arcpy.Describe(ras_csi)
                    coord_sys = dsc.SpatialReference
                    rel_ras = Con(Float(ras_csi) >= float(wua_threshold), Float(ras_csi))
                    self.logger.info("       * saving WUA-CHSI raster ...")
                    try:
                        rel_ras.save(self.path_wua_ras + str(csi))
                    except:
                        self.logger.info("ERROR: Could not save WUA-CHSI raster.")

                    ras4shp = Con(~IsNull(rel_ras), 1)

                    self.logger.info("       * converting WUA-CHSI raster to shapefile ...")
                    try:
                        shp_name = self.cache + str(cc) + "wua.shp"
                        arcpy.RasterToPolygon_conversion(ras4shp, shp_name, "NO_SIMPLIFY")
                        arcpy.DefineProjection_management(shp_name, coord_sys)
                    except arcpy.ExecuteError:
                        self.logger.info("ExecuteERROR: (arcpy) in RasterToPolygon_conversion.")
                        self.logger.info(arcpy.GetMessages(2))
                        arcpy.AddError(arcpy.GetMessages(2))
                    except Exception as e:
                        self.logger.info("ExceptionERROR: (arcpy) in RasterToPolygon_conversion.")
                        self.logger.info(e.args[0])
                        arcpy.AddError(e.args[0])
                    except:
                        self.logger.info("ERROR: Shapefile conversion failed.")

                    self.logger.info("       * calculating area ...")
                    area = 0.0
                    try:
                        arcpy.CalculateAreas_stats(shp_name, self.cache + str(cc) + "wua_eval.shp")
                        self.logger.info("         summing up area ...")
                        with arcpy.da.UpdateCursor(self.cache + str(cc) + "wua_eval.shp", "F_AREA") as cursor:
                            for row in cursor:
                                try:
                                    area += float(row[0])
                                except:
                                    self.logger.info("       WARNING: Bad value (" + str(row) + ")")
                    except arcpy.ExecuteError:
                        self.logger.info("ExecuteERROR: (arcpy) in CalculateAreas_stats.")
                        self.logger.info(arcpy.GetMessages(2))
                        arcpy.AddError(arcpy.GetMessages(2))
                    except Exception as e:
                        self.logger.info("ExceptionERROR: (arcpy) in CalculateAreas_stats.")
                        self.logger.info(e.args[0])
                        arcpy.AddError(e.args[0])
                    except:
                        self.logger.info("ERROR: Area calculation failed.")

                    self.logger.info("       * writing Usable Area to workbook:")
                    for q in Q.keys():
                        if str(int(q)) == str(csi).split(fish_shortname)[1]:
                            self.logger.info(
                                "         Discharge: " + str(q) + self.u_discharge + " and Usable Area: " + str(
                                    area) + " square " + self.u_length)
                            row = int("".join([str(s) for s in str(Q[q]) if s.isdigit()]))
                            xlsx.write_data_cell("F", row, (area * self.ft2ac))
                    cc += 1

                try:
                    xlsx.save_close_wb(xlsx_name)
                    self.xlsx_out = xlsx_name
                except:
                    self.logger.info("ERROR: Failed to save " + str(xlsx_name))
        arcpy.CheckInExtension('Spatial')
        if cc > 0:
            return "OK"
        else:
            return "NoMatch"

    def clear_cache(self, *args):
        # if args[0]==False: the cache folder itself is not deleted
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.cache
        ras_list = arcpy.ListRasters()
        shp_list = arcpy.ListFeatureClasses()
        try:
            for ras in ras_list:
                try:
                    arcpy.Delete_management(str(ras))
                except:
                    pass
            for shp in shp_list:
                try:
                    arcpy.Delete_management(str(shp))
                except:
                    pass
            try:
                arcpy.env.workspace = os.path.dirname(os.path.abspath(__file__))  # temporary workspace
                fg.rm_dir(self.cache)
                if not args[0]:
                    self.logger.info("        * restoring cache ...")
                    fg.chk_dir(self.cache)
                    arcpy.env.workspace = self.cache
            except:
                self.logger.info("   >> Cleared .cache folder (arcpy.Delete_management) ...")

        except:
            self.logger.info("WARNING: .cache folder will be removed by package controls.")

    def launch_chsi_maker(self, fish, combine_method, boundary_shp):
        try:
            self.combine_method = combine_method
        except:
            self.combine_method = "geometric_mean"

        return self.make_chsi(fish, boundary_shp)

    def make_boundary_ras(self, shapef):
        if not arcpy.Exists(self.path_hsi + "boundras"):
            self.logger.info("    * Converting to raster ...")
            try:
                arcpy.PolygonToRaster_conversion(in_features=shapef, value_field="Id",
                                                 out_rasterdataset=self.path_hsi + "boundras",
                                                 cell_assignment="CELL_CENTER", cellsize=1.0)
            except:
                self.logger.info(
                    "ERROR: Boundary shapefile in arcpy.PolygonToRaster_conversion. Check boundary shapefile.")
                self.logger.info(Exception.args[0])
                self.logger.info(arcpy.GetMessages())
        try:
            return arcpy.Raster(self.path_hsi + "boundras")
        except:
            return -1

    def make_chsi(self, fish, boundary_shp):
        # habitat suitability curves from Fish.xlsx
        # fish is a dictionary with fish species listed in Fish.xlsx
        # boundary_shp is either a full path of a shape file or an empty string for using "MAXOF"

        self.logger.info(" >> Raster combination method: " + str(self.combine_method))
        arcpy.CheckOutExtension('Spatial')
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.cache
        arcpy.env.extent = "MAXOF"

        if boundary_shp.__len__() > 0:
            self.logger.info(" >> Applying boundary shapefile ... ")
            boundary_ras = self.make_boundary_ras(boundary_shp)
            try:
                if boundary_ras == -1:
                    self.logger.info("ERROR: Boundary shapefile provided but raster conversion failed.")
                    return -1
            except:
                pass

        self.logger.info(" >> Retrieving hydraulic HSI rasters from:")
        self.logger.info("      " + self.path_hsi)
        arcpy.env.workspace = self.path_hsi
        __temp_list__ = arcpy.ListRasters()
        hsi_list = []
        [hsi_list.append(item) for item in __temp_list__]  # ensures that hsi_list is not a pointer but a real list
        del __temp_list__
        arcpy.env.workspace = self.cache

        cc = 0
        for species in fish.keys():
            for ls in fish[species]:
                self.logger.info(" -- Usable Area for " + str(species).upper() + " - " + str(ls).upper())
                fish_shortname = str(species).lower()[0:2] + str(ls[0])
                for ras in hsi_list:
                    if not (fish_shortname in str(ras)):
                        continue
                    cc += 1
                    # find dsi-rasters and match according velocity rasters
                    if str(ras)[0:3] == "dsi":
                        q = int(str(ras).split(fish_shortname)[-1])
                        self.logger.info("    --- combining rasters for Q = " + str(q) + " (" + self.combine_method + ") ...")

                        # load inundation area Raster (wetted area)
                        try:
                            self.logger.info("        * loading innundated area raster ...")
                            if q >= 1000:
                                h_ras_name = "h%003dk" % int(q/1000)
                            else:
                                h_ras_name = "h%003d" % q
                            if boundary_shp.__len__() > 0:
                                self.logger.info("        * clipping to boundary ...")
                                inundation_ras = Con(~IsNull(boundary_ras), arcpy.Raster(self.path_condition + h_ras_name))
                            else:
                                inundation_ras = arcpy.Raster(self.path_condition + h_ras_name)
                        except:
                            self.logger.info("ERROR: Cannot find flow depth raster for Q = " + str(q))
                            return -1

                        if self.cover_applies:
                            try:
                                # use higher hsi pixels if cover indicates relevance
                                cover_types = ["substrate", "boulders", "cobbles", "wood", "plants"]
                                arcpy.env.extent = arcpy.Extent(inundation_ras.extent.XMin, inundation_ras.extent.YMin,
                                                                inundation_ras.extent.XMax, inundation_ras.extent.YMax)
                                relevant_cov = []
                                for covt in cover_types:
                                    if arcpy.Exists(self.path_hsi + covt + "_hsi"):
                                        self.logger.info("        * adding cover: " + covt + "_hsi")
                                        relevant_cov.append(Float(arcpy.Raster(self.path_hsi + covt + "_hsi")))
                                self.logger.info("        * calculating cell statistics (maximum HSI values) ...")
                                cov_hsi = Float(CellStatistics(relevant_cov, "MAXIMUM", "DATA"))
                            except:
                                self.logger.info("ERROR: Could not add cover HSI.")
                                return -1
                        try:
                            self.logger.info("        * reading hydraulic HSI rasters ...")
                            dsi = Float(arcpy.Raster(self.path_hsi + str(ras)))
                            vsi = Float(arcpy.Raster(self.path_hsi + "vsi" + str(ras).strip("dsi")))
                            if self.cover_applies:
                                if self.combine_method == "geometric_mean":
                                    self.logger.info("        * combining hydraulic and cover HSI rasters (geometric mean)...")
                                    chsi = Con(~IsNull(inundation_ras), Con(Float(inundation_ras) > 0.0, Float(Float(dsi * vsi * cov_hsi) ** Float(1/3))))
                                if self.combine_method == "product":
                                    self.logger.info("        * combining hydraulic and cover HSI rasters (product)...")
                                    chsi = Con(~IsNull(inundation_ras), Con(Float(inundation_ras) > 0.0, Float(dsi * vsi * cov_hsi)))
                            else:
                                if self.combine_method == "geometric_mean":
                                    self.logger.info("        * combining hydraulic HSI rasters (geometric mean)...")
                                    chsi = Con(~IsNull(inundation_ras), Con(Float(inundation_ras) > 0.0, Float(SquareRoot(dsi * vsi))))
                                if self.combine_method == "product":
                                    self.logger.info("        * combining hydraulic HSI rasters (product)...")
                                    chsi = Con(~IsNull(inundation_ras), Con(Float(inundation_ras) > 0.0, Float(dsi * vsi)))
                            self.logger.info("        * saving as ...")
                            chsi.save(self.path_csi + "csi" + str(ras).strip("dsi"))
                            self.logger.info("        * clearing cache buffer ...")
                            del chsi, dsi, vsi
                            self.clear_cache(False)
                            self.logger.info("        * ok ...")
                        except:
                            self.logger.info("ERROR: Could not save CSI raster associated with " + str(ras) + ".")
                            return -1
                self.logger.info(" >> OK")
                arcpy.CheckOutExtension('Spatial')
        if cc > 0:
            return "OK"
        else:
            return "NoMatch"

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = CHSI (Module: Habitat Evaluation)")


class HHSI:
    def __init__(self, geo_input_path, condition, *unit_system):

        # general directories and parameters
        self.cache = os.path.dirname(os.path.realpath(__file__)) + "\\.cache\\"
        self.condition = condition
        self.dir_in_geo = geo_input_path
        self.path_hsi = os.path.dirname(os.path.realpath(__file__)) + "\\HSI\\" + str(condition) + "\\"
        self.error = False
        self.flow_dict_h = {}
        self.flow_dict_u = {}
        self.fish = cf.Fish()
        self.logger = logging.getLogger("habitat_evaluation")
        self.raster_dict = {}
        self.ras_h = []
        self.ras_u = []

        fg.chk_dir(self.cache)
        fg.clean_dir(self.cache)
        fg.chk_dir(self.path_hsi)
        fg.chk_dir(self.dir_in_geo)

        # set unit system variables
        try:
            self.units = unit_system[0]
        except:
            self.units = "us"
            print("WARNING: Invalid unit_system identifier. unit_system must be either \'us\' or \'si\'.")
            print("         Setting unit_system default to \'us\'.")

    def clear_cache(self, *args):
        # if args[0]==False: the cache folder itself is not deleted
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.cache
        ras_list = arcpy.ListRasters()
        shp_list = arcpy.ListFeatureClasses()
        try:
            for ras in ras_list:
                try:
                    arcpy.Delete_management(str(ras))
                except:
                    pass
            for shp in shp_list:
                try:
                    arcpy.Delete_management(str(shp))
                except:
                    pass
            try:
                arcpy.env.workspace = os.path.dirname(os.path.abspath(__file__))  # temporary workspace
                fg.rm_dir(self.cache)
                if not args[0]:
                    self.logger.info("        * restoring cache ...")
                    fg.chk_dir(self.cache)
                    arcpy.env.workspace = self.cache
            except:
                self.logger.info(" >> Cleared .cache folder (arcpy.Delete_management) ...")

        except:
            self.logger.info("WARNING: .cache folder will be removed by package controls.")

    def make_boundary_ras(self, shapef):
        if not arcpy.Exists(self.path_hsi + "boundras"):
            self.logger.info("    * Converting to raster ...")
            try:
                arcpy.PolygonToRaster_conversion(in_features=shapef, value_field="Id",
                                                 out_rasterdataset=self.path_hsi + "boundras",
                                                 cell_assignment="CELL_CENTER", cellsize=1.0)
            except:
                self.logger.info(
                    "ERROR: Boundary shapefile in arcpy.PolygonToRaster_conversion. Check boundary shapefile.")
                self.logger.info(Exception.args[0])
                self.logger.info(arcpy.GetMessages())
        try:
            return arcpy.Raster(self.path_hsi + "boundras")
        except:
            return -1

    def make_hhsi(self, fish_applied, boundary_shp):
        # habitat suitability curves from Fish.xlsx
        # fish_applied is a dictionary with fish species listed in Fish.xlsx
        # boundary_shp is either a full path of a shape file or an empty string for using "MAXOF"

        self.read_hyd_rasters()

        arcpy.CheckOutExtension('Spatial')
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.cache
        arcpy.env.extent = "MAXOF"

        if boundary_shp.__len__() > 0:
            boundary_ras = self.make_boundary_ras(boundary_shp)
            try:
                if boundary_ras == -1:
                    self.logger.info("ERROR: Boundary shapefile provided but raster conversion failed.")
                    return -1
            except:
                pass

        for species in fish_applied.keys():
            self.logger.info(" >> FISH SPECIES  : " + str(species))
            for ls in fish_applied[species]:
                self.logger.info("         LIFESTAGE: " + str(ls))
                self.logger.info("   >> Calculating DEPTH HSI (DSI)")
                self.logger.info("    > Retrieving hhsi curve from Fish.xlsx ...")
                curve_data = self.fish.get_hsi_curve(species, ls, "h")
                self.logger.info("      - OK")
                for rh in self.ras_h:
                    self.logger.info("   -> DISCHARGE: " + str(self.flow_dict_h[str(rh)]))
                    rh_ras = arcpy.Raster(self.dir_in_geo + rh)
                    self.logger.info("    > Raster calculation: Depth HSI ...")
                    if boundary_shp.__len__() > 0:
                        __temp_h_ras__ = Con(~IsNull(boundary_ras), Float(rh_ras))
                        rh_ras = __temp_h_ras__
                    ras_out = self.nested_con_raster_calc(rh_ras, curve_data)
                    self.logger.info("      - OK")
                    ras_name = "dsi_" + str(species[0:2]).lower() + str(ls)[0] + str(self.flow_dict_h[str(rh)])
                    self.logger.info("    > Saving: " + self.path_hsi + ras_name + " ...")
                    try:
                        ras_out.save(self.path_hsi + ras_name)
                        self.logger.info("      - OK")
                    except:
                        self.logger.info("ERROR: Could not save HHSI (depth) raster (corrupted data?).")

                self.logger.info("   >> Calculating VELOCITY HSI")
                self.logger.info("    > Reading hhsi curve from Fish.xlsx ...")
                curve_data = self.fish.get_hsi_curve(species, ls, "u")
                self.logger.info("      - OK")
                for ru in self.ras_u:
                    self.logger.info("   -> DISCHARGE: " + str(self.flow_dict_u[str(ru)]))
                    rh_ras = arcpy.Raster(self.dir_in_geo + ru)
                    self.logger.info("    > Raster calculation: Velocity HSI  ... ")
                    if boundary_shp.__len__() > 0:
                        __temp_h_ras__ = Con(~IsNull(boundary_ras), Float(rh_ras))
                        rh_ras = __temp_h_ras__
                    ras_out = self.nested_con_raster_calc(rh_ras, curve_data)
                    self.logger.info("      - OK")
                    ras_name = "vsi_" + str(species[0:2]).lower() + str(ls)[0] + str(self.flow_dict_u[str(ru)])
                    self.logger.info(
                        "    > Saving: " + self.path_hsi + ras_name + " ...")
                    try:
                        ras_out.save(self.path_hsi + ras_name)
                        self.logger.info("      - OK")
                    except:
                        self.logger.info("ERROR: Could not save HHSI (velocity) raster (corrupted data?).")

            self.logger.info(" >> FISH SPECIES " + str(species).upper() + " COMPLETE.")
        arcpy.env.workspace = self.cache
        arcpy.CheckInExtension('Spatial')

    def nested_con_raster_calc(self, ras, curve_data):
        arcpy.env.extent = "MAXOF"
        # curve_data = [[x-values], [y-values(hsi)]]
        __ras__ = [ras * 0]  # initial raster assignment
        index = 0
        i_par_prev = 0.0
        i_hsi_prev = curve_data[1][0]
        for i_par in curve_data[0]:
            __ras__.append(Float(Con((Float(ras) >= Float(i_par_prev)) & (Float(ras) < Float(i_par)), (
                                     Float(i_hsi_prev) + (
                                      (Float(ras) - Float(i_par_prev)) / (Float(i_par) - Float(i_par_prev)) * Float(
                                        curve_data[1][index] - i_hsi_prev))), Float(0.0))))
            i_hsi_prev = curve_data[1][index]
            i_par_prev = i_par
            index += 1

        return Float(CellStatistics(__ras__, "SUM", "DATA"))

    def read_hyd_rasters(self):
        # uses negotiated HHSI script
        arcpy.CheckOutExtension('Spatial')
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.dir_in_geo
        arcpy.env.extent = "MAXOF"

        # obtain just the depth files
        self.logger.info(" >> Retrieving rasters for hydraulic HSI calculation.")
        all_rasters = arcpy.ListRasters()
        arcpy.env.workspace = self.cache

        for rn in all_rasters:
            if (rn[0] == "h") or (rn[0] == "u"):
                try:
                    if str(rn).endswith("k"):
                        # multiply "k"-raster name discharges with 1000
                        thousand = 1000.0
                    else:
                        thousand = 1.0
                    if rn[0] == "h":
                        self.logger.info("     -- Adding flow depth raster: " + str(rn))
                        _Q_ = float(str(rn).split("h")[1].split("k")[0]) * thousand
                        self.flow_dict_h.update({str(rn): int(_Q_)})
                        self.ras_h.append(str(rn))
                    if rn[0] == "u":
                        self.logger.info("     -- Adding flow velocity raster: " + str(rn))
                        _Q_ = float(str(rn).split("u")[1].split("k")[0]) * thousand
                        self.flow_dict_u.update({str(rn): int(_Q_)})
                        self.ras_u.append(str(rn))
                except:
                    self.logger.info("ERROR: Failed to add raster.")

        arcpy.env.workspace = self.cache
        arcpy.CheckInExtension('Spatial')

    def __call__(self, *args):
        print("Class Info: <type> = HHSI (Module: Habitat Evaluation)")


class CovHSI(HHSI):
    def __init__(self, raster_input_path, condition, geofile_name, *unit_system):
        try:
            HHSI.__init__(self, raster_input_path, condition, unit_system[0])
        except:
            # if no unit_system is provided
            HHSI.__init__(self, raster_input_path, condition)

        self.cover_type = str(geofile_name).split(".")[0]
        self.cell_size = float()  # initialization for points to raster export variable
        if self.units == "us":
            self.geofile_dict = {"substrate": "dmean_ft", "boulders": "boulders.shp", "cobbles": "dmean_ft",
                                 "wood": "wood.shp", "plants": "plants.shp"}
        else:
            self.geofile_dict = {"substrate": "dmean", "boulders": "boulders.shp", "cobbles": "dmean",
                                 "wood": "wood.shp", "plants": "plants.shp"}

        if not (self.geofile_dict[self.cover_type][-4:-1] == ".sh"):
            try:
                self.logger.info(" >> Identified cover type (input raster): " + self.geofile_dict[self.cover_type])
                self.input_raster = arcpy.Raster(raster_input_path + self.geofile_dict[self.cover_type])
            except:
                self.logger.info("ERROR: Could not find the cover input geofile (" + self.geofile_dict[self.cover_type] + ").")
        else:
            self.logger.info(" >> Identified cover type (input shapefile): " + self.geofile_dict[self.cover_type])
            self.input_raster = self.convert_shp2raster(self.dir_in_geo + self.geofile_dict[self.cover_type])

    def call_analysis(self, curve_data):
        if self.cover_type == "substrate":
            return self.nested_con_raster_calc(self.input_raster, curve_data)
        if (self.cover_type == "plants") or (self.cover_type == "wood") or (self.cover_type == "boulders"):
            return self.spatial_join_analysis(self.input_raster, curve_data)
        if self.cover_type == "cobbles":
            return self.substrate_size_analysis(self.input_raster, curve_data)

    def convert_shp2raster(self, shapefile):
        cov_raster = "cov_ras"  # name of the temporarily used cover raster
        arcpy.PolygonToRaster_conversion(shapefile, "cover", self.cache + cov_raster,
                                         cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=1)
        return arcpy.Raster(self.cache + cov_raster)

    def crop_input_raster(self, fish_species, fish_lifestage, depth_raster_path):
        # crop (cover) input_raster to the minimum flow depth defined in Fish.xlsx, associated with a given dsicharge
        try:
            curve_data = self.fish.get_hsi_curve(fish_species, fish_lifestage, "h")
            h_min = curve_data[0][0]
        except:
            self.logger.info(
                "WARNING: Could not get minimum flow depth for defined fish species/lifestage. Setting h min to 0.1 (default).")
            h_min = 0.1
        try:
            h_raster = arcpy.Raster(depth_raster_path)
            __temp__ = Con((Float(h_raster) >= h_min), self.input_raster)
            self.input_raster = __temp__
        except:
            self.logger.info("ERROR: Could not crop raster to defined flow depth.")
        # assign relevant cell_size for point to raster conversion
        try:
            self.cell_size = float(arcpy.GetRasterProperties_management(h_raster, property_type="CELLSIZEX")[0])
        except:
            self.logger.info("WARNING: Could not get flow depth raster properties. Setting output cell size to 3.0 (default).")
            self.cell_size = 3.0  # default assignment

    def define_grain_size(self, grain_type):
        if "cobbles" in grain_type:
            metric_size = [0.064, 0.256]  # cobble min and max size in meters
        if "boulders" in grain_type:
            metric_size = [0.256, 100]  # boulder min and max (fictive) size in meters

        try:
            if self.units == "us":
                return [uss / 0.3047992 for uss in metric_size]
            if self.units == "si":
                return metric_size
        except:
            pass

    def make_covhsi(self, fish_applied, depth_raster_path):
        # habitat suitability curves from Fish.xlsx
        # fish_applied is a dictionary with fish species listed in Fish.xlsx
        arcpy.CheckOutExtension('Spatial')
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.cache
        arcpy.env.extent = "MAXOF"
        self.logger.info("* * * CREATING " + str(self.cover_type).upper() + " COVER RASTER * * *")
        for species in fish_applied.keys():
            self.logger.info(" >> FISH SPECIES  : " + str(species))
            for ls in fish_applied[species]:
                self.logger.info("         LIFESTAGE: " + str(ls))
                self.logger.info("   -> Retrieving " + self.cover_type + " curve from Fish.xlsx ...")
                curve_data = self.fish.get_hsi_curve(species, ls, self.cover_type)
                if depth_raster_path.__len__() > 0:
                    self.logger.info("   -> Cropping to relevant depth regions ...")
                    self.crop_input_raster(species, ls, depth_raster_path)
                else:
                    try:
                        self.cell_size = float(arcpy.GetRasterProperties_management(self.input_raster, property_type="CELLSIZEX")[0])
                    except:
                        self.cell_size = 1.0
                self.logger.info("   -> Calculating cover HSI raster ...")
                try:
                    ras_out = self.call_analysis(curve_data)
                except:
                    self.logger.info("ERROR: Cover raster calculation (check input data).")
                    arcpy.CheckInExtension('Spatial')
                    self.error = True

                self.logger.info("      - OK")
                ras_name = self.cover_type + "_hsi"
                self.logger.info(
                    "   -> Saving: " + self.path_hsi + ras_name + " ...")
                try:
                    ras_out.save(self.path_hsi + ras_name)
                    self.logger.info("      - OK")
                except:
                    self.logger.info("ERROR: Could not save " + self.cover_type + " HSI raster (corrupted data?).")
                    self.error = True

            if not self.error:
                self.logger.info(" >> " + self.cover_type + " cover HSI raster creation " + str(species).upper() + " complete.")
            else:
                self.logger.info(" >> Could not create cover HSI raster. Check error messages.")

        arcpy.CheckInExtension('Spatial')

    def spatial_join_analysis(self, raster, curve_data):
        # uses curve radius data and to mark all points within this radius of the input raster

        self.logger.info("   -> Converting raster to points ...")
        try:
            cov_points = self.cache + "cov_points.shp"
            arcpy.RasterToPoint_conversion(raster, cov_points)
            zero_raster = Con((IsNull(raster) == 1), (IsNull(raster) * 1), 1)
            all_points = self.cache + "all_points.shp"
            arcpy.RasterToPoint_conversion(zero_raster, all_points)
        except:
            self.error = True
            self.logger.info("ERROR: Could not perform spatial radius operations (RasterToPoint_conversion).")
        self.logger.info("   -> Delineating " + self.cover_type + " effect radius (spatial join radius: " + str(curve_data[0][0]) + ") ...")
        try:
            out_points = self.cache + "spatjoin.shp"
            rad = float(curve_data[0][0])
            arcpy.SpatialJoin_analysis(target_features=all_points, join_features=cov_points,
                                       out_feature_class=out_points, join_operation="JOIN_ONE_TO_MANY",
                                       join_type="KEEP_COMMON", field_mapping="", match_option="CLOSEST",
                                       search_radius=rad, distance_field_name="")
        except:
            self.error = True
            self.logger.info("ERROR: Could not perform spatial radius operations (SpatialJoin_analysis).")
        self.logger.info("   -> Converting points back to raster ...")
        try:
            arcpy.PointToRaster_conversion(in_features=out_points, value_field="grid_code",
                                           out_rasterdataset=self.cache + "cov_points",
                                           cell_assignment="MEAN", cellsize=self.cell_size)
            __temp_ras__ = arcpy.Raster(self.cache + "cov_points")
            self.logger.info("   -> Assigning spatial HSI value (" + str(curve_data[1][0]) + ") where applies (raster calculator) ...")
            __ras__ = Con(__temp_ras__ > 0, curve_data[1][0])  # assign HSI value
        except:
            self.error = True
            self.logger.info("ERROR: Could not perform spatial radius operations (back conversion).")
        if not self.error:
            return Float(CellStatistics([__ras__], "SUM", "DATA"))
        else:
            return -1

    def substrate_size_analysis(self, raster, curve_data):
        self.logger.info("   -> Sorting out relevant grain sizes ...")
        # retain only values of interest
        __ras__ = Con(Float(raster) >= self.define_grain_size(self.cover_type)[0],
                      Con(Float(raster) < self.define_grain_size(self.cover_type)[1], 1.0))
        return self.spatial_join_analysis(__ras__, curve_data)

    def __call__(self, *args):
        print("Class Info: <type> = CovHSI (Module: Habitat Evaluation)")


class FlowAssessment:
    def __init__(self):
        self.Q_flowdur = []
        self.exceedance_abs = []  # absolute exceedance duration in days
        self.exceedance_rel = []  # relative exceedance duration in percent
        self.logger = logging.getLogger("habitat_evaluation")

    def calculate_relative_exceedance(self):
        self.logger.info(" >> Calculating relative flow exceedances ...")
        max_d = max(self.exceedance_abs)
        for val in self.exceedance_abs:
            try:
                self.exceedance_rel.append(float(val / max_d))
            except:
                self.exceedance_rel.append(0.0)
                self.logger.info("WARNING: Could not divide " + str(val) + " by " + str(max_d) + ".")
        self.logger.info(" >> OK")

    def get_flow_data(self, *alternative_flowdur):
        # *alternative_flowdur can be an optional alternative workbook  with flow duration curve data
        #     --> anyway, the alternative must have Q_flowdur data in col B and exceedance days in col C (start_row=2)
        self.logger.info(" >> Retrieving flow data ...")
        try:
            hydro_wb = alternative_flowdur[0]
        except:
            hydro_wb = os.path.dirname(os.path.realpath(__file__)) + "\\hydrograph.xlsx"
        self.logger.info(" >> Source: " + str(hydro_wb))
        data_reader = chio.Read(hydro_wb)
        self.Q_flowdur = data_reader.read_column("B", 2)  # cfs or m3
        self.exceedance_abs = data_reader.read_column("C", 2)  # days

        # interpolate zero-probability flow
        Q_max = float(self.Q_flowdur[-1] - (self.Q_flowdur[-2] - self.Q_flowdur[-1]) / float(self.exceedance_abs[-2] - self.exceedance_abs[-1]))
        self.Q_flowdur.append(Q_max)
        self.exceedance_abs.append(0)

        # add data consistency (ensure that self.Q_flowdur and self.exceedance are the same length)
        __ex__ = []
        for iq in range(0, self.Q_flowdur.__len__()):
            try:
                __ex__.append(self.exceedance_abs[iq])
            except:
                self.Q_flowdur.insert(0, Q_max)
                self.logger.info(
                    "WARNING: Flow_duration[...].xlsx has different lengths of \'Q_flowdur\' and \'exceedance days\' columns.")
        self.exceedance_abs = __ex__
        self.logger.info(" >> OK")
        self.calculate_relative_exceedance()

    def interpolate_flow_exceedance(self, Q_value):
        # Q_value is a FLOAT discharge in cfs or m3s
        self.logger.info(" >> Interpolating exceedance probability for Q_flowdur = " + str(Q_value))
        try:
            Q_value = float(Q_value)
        except:
            self.logger.info("ERROR: Invalid interpolation data type (type(Q_flowdur) == " + type(Q_value) + ").")

        if Q_value <= max(self.Q_flowdur):
            if not(Q_value <= min(self.Q_flowdur)):
                # find closest smaller and higher discharge
                iq = 0
                for qq in sorted(self.Q_flowdur, reverse=True):
                    # iterate Q_flowdur list (start from lowest)
                    if iq == 0:
                        Q_lower = self.Q_flowdur[iq]
                        ex_lower = 1.0
                    else:
                        Q_lower = self.Q_flowdur[iq - 1]
                        ex_lower = float(self.exceedance_rel[iq - 1])
                    Q_higher = self.Q_flowdur[iq]
                    ex_higher = self.exceedance_rel[iq]
                    if Q_value > qq:
                        self.logger.info(" -->> qq: " + str(qq))
                        self.logger.info(" -->> Q_value: " + str(Q_value))
                        break
                    iq += 1
            else:
                Q_lower = Q_value
                ex_lower = 1.0
                Q_higher = min(self.Q_flowdur)
                ex_higher = 1.0
        else:
            self.logger.info(" >> HIGH DISCHARGE. Annual exceedance probability close to zero.")
            Q_lower = max(self.Q_flowdur)
            ex_lower = 0.0
            Q_higher = Q_value
            ex_higher = 0.0
        try:
            self.logger.info(" -->> ex_low: " + str(ex_lower))
            self.logger.info(" -->> ex_high: " + str(ex_higher))
            self.logger.info(" -->> Q_low: " + str(Q_lower))
            self.logger.info(" -->> Q_high: " + str(Q_higher))
            pr_exceedance = ex_lower + ((Q_value - Q_lower) / (Q_higher - Q_lower)) * (ex_higher - ex_lower)
            self.logger.info(" -->> Expected exceedance duration (per year): " + str(pr_exceedance * 100) + "%")
            return pr_exceedance
        except:
            self.logger.info("ERROR: Could not interpolate exceedance probability of Q = " + str(Q_value) + ".")
            return 0.0

    def __call__(self, *args):
        print("Class Info: <type> = FlowAssessment (Module: Habitat Evaluation)")


