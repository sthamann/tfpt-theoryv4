"""TFPT recovery comb on neutron-star crust-cooling curves.

A self-contained port of the injection-validated log-periodic recovery-comb detector
(experiments/recovery-comb-domains, experiments/pulsar-glitch-recovery) applied to a genuinely
new observational domain: the crust-cooling relaxation of quasi-persistent neutron-star transients.
Crust cooling is the cleanest *floor-terminated* relaxation-to-attractor in nature outside the
horizon -- its purpose here is to serve as the independent SECOND data world the comb needs.

Nothing is claimed. See README.md for the firewall + observable semantics.
"""

from .comb import LAMBDA, MIN_COMB_PERIODS, OMEGA, EPS_PREDICTED

__all__ = ["LAMBDA", "MIN_COMB_PERIODS", "OMEGA", "EPS_PREDICTED"]
