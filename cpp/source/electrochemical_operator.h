#ifndef CAP_ELECTROCHEMICAL_OPERATOR_H
#define CAP_ELECTROCHEMICAL_OPERATOR_H

#include <cap/operator.h>

namespace cap
{

//////////////////// ELECTROCHEMICAL OPERATOR PARAMETERS //////////////////////
enum CapacitorState
{
  GalvanostaticCharge,
  GalvanostaticDischarge,
  PotentiostaticCharge,
  PotentiostaticDischarge,
  Initialize,
  Relaxation,
  CustomConstantCurrent,
  CustomConstantVoltage,
  CustomConstantLoad
};

/**
 * This class encapsulates the parameters used in ElectrochemicalOperator.
 */
template <int dim>
class ElectrochemicalOperatorParameters : public OperatorParameters<dim>
{
public:
  ElectrochemicalOperatorParameters(
      std::shared_ptr<boost::property_tree::ptree const> d)
      : OperatorParameters<dim>(d)
  {
  }

  CapacitorState capacitor_state;
  double custom_constant_current_density;
  double custom_constant_voltage;
  double custom_constant_load_density;
};

//////////////////////// ELECTROCHEMICAL OPERATOR ////////////////////////////
/**
 * Create the system of equations associated with the electro-chemical reactions
 * happening in a supercapacitor.
 */
template <int dim>
class ElectrochemicalOperator : public Operator<dim>
{
public:
  ElectrochemicalOperator(
      std::shared_ptr<OperatorParameters<dim> const> parameters);

  void
  reset(std::shared_ptr<OperatorParameters<dim> const> parameters) override;

  /**
   * Compute the heat generated inside the supercapacitor. This is the source
   * term of ThermalOperator.
   */
  void compute_heat_source(
      dealii::BlockVector<double> const &,
      dealii::Vector<double> &) const; // TODO: template 1st argument

protected:
  void compute_electrical_operator_contribution();

  void compute_dirichlet_boundary_values(double const);

  void compute_neumann_boundary_contribution(double const);

  void compute_robin_boundary_contribution(double const);

  CapacitorState capacitor_state;
  unsigned int solid_potential_component;
  unsigned int liquid_potential_component;
  unsigned int temperature_component;
  double alpha;
  dealii::types::boundary_id anode_boundary_id;
  dealii::types::boundary_id cathode_boundary_id;
};

} // end namespace cap

#endif // CAP_ELECTROCHEMICAL_OPERATOR_H