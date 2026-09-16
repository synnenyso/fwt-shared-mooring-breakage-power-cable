# fwt-shared-mooring-breakage-power-cable
Additional data, files and scripts supporting the article *"Early-Stage Evaluation of the Consequences of Accidental Line Breakage in Shared Mooring Systems With Suspended Intra-Array Power Cables"* [1].

## Folder description: 
**plot_layouts** : files for visualization of intra-array power cable layouts for the system used in the case study in [1].

**fig_intra-array-power-cable-layouts**: visualization of all suspended cable topologies (SC) included in the case study. Images are only included for a given location and orientation of the substation cable connection (SCC). All other combinations can be visualized using the scripts in "plot-layouts".

**fig_res_allLayouts** : 
**__fig_intra-array-power-cable-layouts.7z** : visualization of result from all considered intra-array power cable layouts for the mooring systems considered in the article. Results include probability of system failure (Pf), expected costs of repair, with and without acquisition costs (C and C_A), and expected loss in revenue (R) during damage state.
The files are named as following: type_SC_X1_X2_SCC_Zdeg, where type = Pf, C, C_A or R, and X1 and X2 the first- and last SC topology in the current image, and Z the orientation of the SCC cable (in degrees). 

**How to understand the results**: 
The horizontal axis identifies the SC topology numbers, and the vertical axis gives the number of the FWT the SCC is connected to (for the given cable orientation). The colour scale in the images is used to easily identify the best (blue, or pink for zero values) and worst (red) performance. The probability of failure represents, as defined in [1], the probability of system failure considering a set of environmental load cases and all possible line break scenarios. The expected costs of repair and the expected loss in revenue are given relative to the highest and lowest values for all considered layout for the given mooring system. 



[1] : Nyboe, et. al, 2026, *"Early-Stage Evaluation of the Consequences of Accidental Line Breakage in Shared Mooring Systems With Suspended Intra-Array Power Cables"*
