
#include "kcg_imported_functions.h"

kcg_real OxgQtyCal(
  /* EnvCtlWindowIndications::OxgQtyCal::Press */kcg_int Press,
  /* EnvCtlWindowIndications::OxgQtyCal::Temp */kcg_int Temp)
{
	double ConstOne = 0.0000000000547;
	double ConstTwo = 0.0000000526;

	double OT = Temp *36.25 - 91.25 + 273;
	double Z = ConstOne * (520 - OT)*(520 - OT) * ((Press - 1) * 22.2165)*((Press - 1) * 22.2165) - ConstTwo * (420 - OT)*(420 - OT) * (Press - 1) *22.2165 +1;
	
	double OxgQty = (Press - 1) * 22.2165 * 276.0072 / (Z * OT) / 1.275532;
	
	return (kcg_real)OxgQty;
}
