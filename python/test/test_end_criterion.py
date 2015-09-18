from pycap import PropertyTree,EnergyStorageDevice,EndCriterion
import unittest

device_database=PropertyTree()
device_database.parse_xml('device.xml')
device=EnergyStorageDevice(device_database)

class capEndCriterionTestCase(unittest.TestCase):
    def test_time_limit(self):
        ptree=PropertyTree()
        ptree.put_string('end_criterion','time')
        ptree.put_double('duration',15)
        time_limit=EndCriterion.factory(ptree)
        time_limit.reset(0.0,device)
        self.assertFalse(time_limit.check(2.0,device))
        self.assertTrue(time_limit.check(15.0,device))
        self.assertTrue(time_limit.check(60.0,device))
    def test_voltage_limit(self):
        ptree=PropertyTree()
        ptree.put_string('end_criterion','voltage_greater_than')
        ptree.put_double('voltage_limit',1.7)
        voltage_limit=EndCriterion.factory(ptree)
        voltage_limit.reset(5.0,device)
        device.evolve_one_time_step_constant_voltage(0.2,1.3)
        self.assertFalse(voltage_limit.check(0.0,device))
        self.assertFalse(voltage_limit.check(60.0,device))
        device.evolve_one_time_step_constant_voltage(0.2,1.7)
        self.assertTrue(voltage_limit.check(45.0,device))
        device.evolve_one_time_step_constant_voltage(0.2,2.1)
        self.assertTrue(voltage_limit.check(45.0,device))
    def test_current_limit(self):
        ptree=PropertyTree()
        ptree.put_string('end_criterion','current_smaller_than')
    

if __name__ == '__main__':
    unittest.main()
