#!/usr/bin/env python
# This work is licensed under the Creative Commons Attribution-NonCommercial-
# ShareAlike 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative
# Commons, PO Box 1866, Mountain View, CA 94042, USA.

import numpy as np
from materials import MaterialLibrary
from dielectric.stacks import Stack

class Coating(object):
    def __init__(self, superstrate, substrate, layers):
        self.superstrate = MaterialLibrary.Instance().get_material(superstrate)
        self.substrate = MaterialLibrary.Instance().get_material(substrate)
        self.layers = [Layer(m, t) for m, t in layers]
        self.thickness = sum([l.thickness for l in self.layers])
        
    def create_stack(self, lambda0, AOI=0.0):
        """
        Returns an optical stack for a specific wavelength and AOI.
        """
        stacks_n = np.zeros(len(self.layers)+2)
        stacks_d = np.zeros(len(self.layers))
        stacks_n[0] = self.superstrate.n(lambda0)
        stacks_n[-1] = self.substrate.n(lambda0)
        for ii in range(0, len(self.layers)):
            stacks_n[ii+1] = self.layers[ii].material.n(lambda0)
            stacks_d[ii] = self.layers[ii].thickness
        return Stack(stacks_n, stacks_d, AOI)

class Layer(object):
    def __init__(self, material, thickness):
        self.material = MaterialLibrary.Instance().get_material(material)
        self.thickness = thickness
