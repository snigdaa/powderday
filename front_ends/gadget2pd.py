import numpy as np
import yt
from yt import derived_field
import pdb,ipdb
import config as cfg




#need - 
#1. PartType4_Metallicity (newstar metals)
#2. PartType4_coordinates
#3. Parttype4_StelarFormationTiome
#4. PartType0_Density
#5. PartType0_Metallicity
#6. Parttype0_Coordinates
#7. Parttype0_Smoothed_Density


def gadget_field_add(fname,unit_base,bbox):
    
    
    def _starmetals_00(field,data):
        return data[('PartType4', 'Metallicity_00')]
        
    def _starmetals(field,data):
        return data[('PartType4', 'Metallicity')]

    def _starcoordinates(field,data):
        return data[('PartType4', 'Coordinates')]

    def _starformationtime(field,data):
        return data[('PartType4', 'StellarFormationTime')]

    def _gasdensity(fied,data):
        return data[('PartType0', 'Density')]

    def _gasmetals_00(field,data):
        return data[('PartType0', 'Metallicity_00')]
    
    def _gasmetals(field,data):
        return data[('PartType0', 'Metallicity')]

    def _gascoordinates(field,data):
        return data[('PartType0','Coordinates')]

    def _gassmootheddensity(field,data):
        return data[("deposit","PartType0_smoothed_density")]

    def _metaldens_00(field,data):
        return (data["PartType0","Density"]*data["PartType0","Metallicity_00"])

    def _metaldens(field,data):
        return (data["PartType0","Density"]*data["PartType0","Metallicity"])

    
    
        


    #load the ds
    ds = yt.load(fname,unit_base=unit_base,bounding_box=bbox,over_refine_factor=cfg.par.oref,n_ref=cfg.par.n_ref)
    ds.index


    #for the metal fields have a few options since gadget can have different nomenclatures
    if  ('PartType4', 'Metallicity_00') in ds.derived_field_list:
        ds.add_field(('starmetals'),function=_starmetals_00,units="code_metallicity",particle_type=True)
    else:
        ds.add_field(('starmetals'),function=_starmetals,units="code_metallicity",particle_type=True)

    if  ('PartType0', 'Metallicity_00') in ds.derived_field_list:
        ds.add_field(('gasmetals'),function=_gasmetals_00,units="code_metallicity",particle_type=True)
    else:
        ds.add_field(('gasmetals'),function=_gasmetals,units="code_metallicity",particle_type=True)

    if  ('PartType0', 'Metallicity_00') in ds.derived_field_list:
        ds.add_field(('metaldens'),function=_metaldens_00,units="g/cm**3", particle_type=True)
    else:
        ds.add_field(('metaldens'),function=_metaldens,units="g/cm**3", particle_type=True)


        
        
        
    ds.add_field(('starcoordinates'),function=_starcoordinates,units='code_length',particle_type=True)
    ds.add_field(('starformationtime'),function=_starformationtime,units='dimensionless',particle_type=True)
    ds.add_field(('gasdensity'),function=_gasdensity,units='code_mass/code_length**3',particle_type=True)
    ds.add_field(('gascoordinates'),function=_gascoordinates,units='code_length',particle_type=True)
    ds.add_field(('gassmootheddensity'),function=_gassmootheddensity,units='code_mass/code_length**3',particle_type=True)


    return ds