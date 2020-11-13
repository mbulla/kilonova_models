# VALIDATION TESTS FOR POLARIZATION

This directory includes POSSIS validation tests for polarization. The tests are computed assuming the geometry described in Hillier (1994) as explained in Bulla, Sim & Kromer (2015). The geometry is shown in geometry.pdf.

# Numerical solutions in the optically-thick regime
pol_tau.pdf shows Fig. 5 of Bulla, Sim & Kromer (2015), where the results from POSSIS (symbols) are compared to the numerical simulations in Hillier (1994, lines). See Section 3.1 of Bulla, Sim & Kromer (2015) for more details.

# Analytic solutions in the optically-thin regime
pol_thin.pdf shows polarization vs inclination angle for four different cases where the averaged optical depth is equal to tau = 0.001, 0.003, 0.005, 0.007. The solid line is the analytic solution from Brown & McLean (1977) for the geometry assumed. The agreement with the analytic solution is excellent for orientations near the z axis (costheta=1) and for all orientations when tau=0.001 and tau=0.003. For larger values of tau, the analytic solution overestimates the polarization signal at orientations close to the equatorial plane (costheta=0). This is expected as the analytic solution in Brown & McLean (1977) is valid only in the optically thin regime.
