# Hackathon: Tag & Probe, the HLT_Ele27_WPTight_Gsf efficiency with coffea

HLT_Ele27_WPTight_Gsf fires on an isolated electron with $p_T > 27$ GeV passing a tight online ID.
We measure its efficiency in 2016 data with Z → ee events, using the tag & probe method.

**Tag** electron:
- $p_T > 27$ GeV and $|\eta| < 2.5$
- not in the ECAL barrel-endcap transition region $1.4442 < |\eta| < 1.566$
- passes the tight cut-based ID
- matched ($\Delta R < 0.1$) to an HLT electron that fired HLT_Ele27_WPTight_Gsf

**Probe** electron:
- opposite charge to the tag
- passes the same tight cut-based ID
- the tag-probe invariant mass is less than 30 GeV away from the Z mass (91.1876 GeV)
- $|\eta| < 2.5$ and not in the transition region, like the tag

A probe is **passing** if it is also matched ($\Delta R < 0.1$) to an HLT electron that fired HLT_Ele27_WPTight_Gsf,
and **failing** otherwise. In each probe $p_T$ bin:

$$\text{efficiency} = \frac{\text{passing}}{\text{passing} + \text{failing}}$$

## What we do

Everything is in [`tag_and_probe.ipynb`](tag_and_probe.ipynb):

1. Write the steps of the measurement: select the events, match electrons to the trigger, make tag-probe pairs,
   select the tags, the probes and the Z candidates, and fill the passing and failing probe histograms.
   Then measure and plot the efficiency on one data file.
2. Scale up with a coffea processor and executor, as in the coffea lesson, to run on several data files and on
   Drell-Yan (Z → ee) simulation.
3. Plot the data and simulation efficiencies together.
4. Compute the data/simulation scale factors in each $p_T$ bin, with their uncertainties.
5. Bonus: a closure test, applying the scale factors to an independent simulation file.

The notebook only works in the BinderHub session (Option 0 in the [main README](../README.md)): it reads its
input files from `/data/mandi26`, which only exists there.
