# Copyright (c) 2016, the Cap authors.
#
# This file is subject to the Modified BSD License and may not be distributed
# without copyright and license information. Please refer to the file LICENSE
# for the text and further information on this license. 

from pycap import PropertyTree, EnergyStorageDevice
from mpi4py import MPI
import unittest

comm = MPI.COMM_WORLD

valid_device_input = [
    "series_rc.info",
    "parallel_rc.info",
#    "super_capacitor.info",
    ]


class capEnergyStorageDeviceWrappersTestCase(unittest.TestCase):
    def test_energy_storage_device_factory(self):
        # valid input to buid an energy storage device
        for filename in valid_device_input:
            ptree = PropertyTree()
            ptree.parse_info(filename)
            EnergyStorageDevice(ptree, comm)
        # invalid device will throw an exception
        ptree = PropertyTree()
        ptree.put_string('type', 'InvalidDevice')
        self.assertRaises(RuntimeError, EnergyStorageDevice, ptree, comm)

    def test_energy_storage_device_not_copyable(self):
        ptree = PropertyTree()
        ptree.parse_info('series_rc.info')
        device = EnergyStorageDevice(ptree, comm)
        from copy import copy, deepcopy
        self.assertRaises(RuntimeError, copy, device)
        self.assertRaises(RuntimeError, deepcopy, device)

    def test_inspect_device(self):
        ptree = PropertyTree()
        ptree.parse_info('super_capacitor.info')
        device = EnergyStorageDevice(ptree, comm)
        # method inspect() takes no argument and returns a dictionary
        data = device.inspect()
        self.assertTrue(isinstance(data, dict))
        for key in [
            'anode_electrode_interfacial_surface_area',
            'anode_electrode_mass_of_active_material',
            'anode_electrode_double_layer_capacitance',
            'anode_electrode_thickness',
            'cathode_electrode_interfacial_surface_area',
            'cathode_electrode_mass_of_active_material',
            'cathode_electrode_double_layer_capacitance',
            'cathode_electrode_thickness',
            'geometric_area',
            ]:
            self.assertTrue(key in data)
        print(data)

if __name__ == '__main__':
    unittest.main()
