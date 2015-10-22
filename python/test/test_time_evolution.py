from pycap import PropertyTree,EnergyStorageDevice,TimeEvolution
import unittest

device_database=PropertyTree()
device_database.parse_xml('device.xml')
device=EnergyStorageDevice(device_database.get_child('device'))

class capTimeEvolutionTestCase(unittest.TestCase):
    def test_evolve_constant_voltage(self):
        ptree=PropertyTree()
        ptree.put_string('mode','constant_voltage')
        ptree.put_double('voltage',2.1)
        evolve_one_time_step=TimeEvolution.factory(ptree)
        evolve_one_time_step(device,0.1)
        self.assertEqual(device.get_voltage(),2.1)
    def test_evolve_constant_current(self):
        ptree=PropertyTree()
        ptree.put_string('mode','constant_current')
        ptree.put_double('current',100e-3)
        evolve_one_time_step=TimeEvolution.factory(ptree)
        evolve_one_time_step(device,0.1)
        self.assertEqual(device.get_current(),100e-3)
    def test_evolve_constant_power(self):
        ptree=PropertyTree()
        ptree.put_string('mode','constant_power')
        ptree.put_double('power',0.3)
        evolve_one_time_step=TimeEvolution.factory(ptree)
        evolve_one_time_step(device,0.1)
        self.assertAlmostEqual(device.get_current()*device.get_voltage(),0.3)
    def test_evolve_constant_load(self):
        ptree=PropertyTree()
        ptree.put_string('mode','constant_load')
        ptree.put_double('load',120)
        evolve_one_time_step=TimeEvolution.factory(ptree)
        evolve_one_time_step(device,0.1)
        self.assertAlmostEqual(device.get_voltage()/device.get_current(),-120)
    def test_hold(self):
        ptree=PropertyTree()
        ptree.put_string('mode','hold')
        evolve_one_time_step=TimeEvolution.factory(ptree)
        device.evolve_one_time_step_constant_voltage(0.1,1.4)
        evolve_one_time_step(device,0.1)
        self.assertEqual(device.get_voltage(),1.4)
    def test_rest(self):
        ptree=PropertyTree()
        ptree.put_string('mode','rest')
        evolve_one_time_step=TimeEvolution.factory(ptree)
        evolve_one_time_step(device,0.1)
        self.assertEqual(device.get_current(),0.0)
    def test_invalid_time_evolution(self):
        ptree=PropertyTree()
        ptree.put_string('mode','unexpected')
        self.assertRaises(RuntimeError,TimeEvolution.factory,ptree)
    def test_constructor(self):
        self.assertRaises(RuntimeError,TimeEvolution)
        self.assertRaises(TypeError,TimeEvolution,PropertyTree())
    
if __name__ == '__main__':
    unittest.main()
