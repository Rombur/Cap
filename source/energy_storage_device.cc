#include <cap/resistor_capacitor.h>
#ifdef WITH_DEAL_II
  #include <cap/supercapacitor.h>
#endif

namespace cap {

std::shared_ptr<cap::EnergyStorageDevice>
buildEnergyStorageDevice(std::shared_ptr<cap::Parameters const> params)
{
    std::shared_ptr<boost::property_tree::ptree const> database = params->database;
    std::string const type = database->get<std::string>("type", "unknown_type");
    if (type.compare("SeriesRC") == 0)
        return std::make_shared<cap::SeriesRC>(params);
    else if (type.compare("ParallelRC") == 0)
        return std::make_shared<cap::ParallelRC>(params);
    else if (type.compare("SuperCapacitor") == 0)
    {
#ifdef WITH_DEAL_II
        int const dim = database->get<int>("dim");
        if (dim == 2)
            return std::make_shared<cap::SuperCapacitor<2>>(params);
        else if (dim ==3)
            return std::make_shared<cap::SuperCapacitor<3>>(params);
        else
            throw std::runtime_error("dim="+std::to_string(dim)+" must be 2 or 3");
#else
        throw std::runtime_error("reconfigure with deal.II");
#endif
    }
    else
        throw std::runtime_error("invalid energy storage type ``"+type+"''\n");
}



EnergyStorageDevice::
~EnergyStorageDevice() = default;



void
EnergyStorageDevice::
evolve_one_time_step_changing_voltage(double const time_step, double const voltage)
{
    // this is meant to be a linear change of the voltage over the time step (ramp)
    // TODO: if not implemented use the step version
    this->evolve_one_time_step_constant_voltage(time_step, voltage);
}



void
EnergyStorageDevice::
evolve_one_time_step_changing_current(double const time_step, double const current)
{
    this->evolve_one_time_step_constant_current(time_step, current);
}



void
EnergyStorageDevice::
evolve_one_time_step_changing_power(double const time_step, double const power)
{
    this->evolve_one_time_step_constant_power(time_step, power);
}



void
EnergyStorageDevice::
evolve_one_time_step_changing_load(double const time_step, double const load)
{
    this->evolve_one_time_step_constant_load(time_step, load);
}

} // end namespace cap
