/-
  TFPT Carrier — Sanity check
  ---------------------------

  Concrete `#eval` statements that print human-readable diagnostics
  without invoking any tactic. Run with:

      lake env lean TfptCarrier/Sanity.lean

  Expected output:

      0
      !![0, 0, 0, 0, 0; 0, 0, 0, 0, 0; 0, 0, 0, 0, 0;
         0, 0, 0, 0, 0; 0, 0, 0, 0, 0]

  i.e. `tr Y = 0` and the carrier polynomial `6 Y² − Y − 1` evaluates
  to the zero 5×5 matrix.
-/

import TfptCarrier.Hypercharge

namespace TFPT.Carrier.Sanity

open TFPT.Carrier.Hypercharge

-- Trace of the hypercharge matrix.
#eval Y.trace

-- Carrier polynomial  6 Y² − Y − 1  evaluated on the concrete model.
#eval ((6 : ℚ) • (Y * Y) - Y - 1)

end TFPT.Carrier.Sanity
