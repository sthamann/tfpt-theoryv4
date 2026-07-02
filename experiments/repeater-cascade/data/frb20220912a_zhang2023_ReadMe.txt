J/ApJ/955/142   Bursts from FAST obs. of FRB 20220912A in 2022   (Zhang+, 2023)
================================================================================
FAST observations of FRB 20220912A: burst properties and polarization
characteristics.
    Zhang Y.-K., Li Di, Zhang B., Cao S., Feng Yi, Wang W.-Y., Qu Y.,
    Niu J.-R., Zhu W.-W., Han J.-L., Jiang P., Lee K.-J., Li D.-Z., Luo R.,
    Niu C.-H., Tsai C.-W., Wang P., Wang F.-Y., Wu Z.-W., Xu H., Yang Y.-P.,
    Zhang J.-S., Zhou D.-J., Zhu Y.-H.
   <Astrophys. J., 955, 142 (2023)>
   =2023ApJ...955..142Z
================================================================================
ADC_Keywords: Radio sources; Transient; Polarization
Keywords: Radio transient sources

Abstract:
    We report the observations of FRB 20220912A using the
    Five-hundred-meter Aperture Spherical radio Telescope (FAST). We
    conducted 17 observations totaling 8.67hr and detected a total of
    1076 bursts with an event rate up to 390hr^-1^. The cumulative energy
    distribution can be well described using a broken power-law function
    with the lower- and higher-energy slopes of -0.38{\pm}0.02 and
    -2.07{\pm}0.07, respectively. We also report the L-band (1-1.5GHz)
    spectral index of the synthetic spectrum of FRB 20220912A bursts,
    which is -2.6{\pm}0.21. The average rotation measure value of the
    bursts from FRB 20220912A is -0.08{\pm}5.39rad/m^2^, close to
    0rad/m^2^ and was relatively stable over 2 months. Most bursts have
    nearly 100% linear polarization. About 45% of the bursts have circular
    polarization with Signal-to-Noise ratio >3, and the highest circular
    polarization degree can reach 70%. Our observations suggest that
    FRB20220912A is located in a relatively clean local environment with
    complex circular polarization characteristics. These various behaviors
    imply that the mechanism of circular polarization of FRBs likely
    originates from an intrinsic radiation mechanism, such as coherent
    curvature radiation or inverse Compton scattering inside the
    magnetosphere of the FRB engine source (e.g., a magnetar).

Description:
    FRB 20220912A has been observed since October 28th, 2022, using the
    center beam of the Five-hundred-meter Aperture Spherical radio
    Telescope (FAST) 19 beam receiver pointing to the coordinate of
    RAJ2000=23:09:04.9,DEJ2000=+48:42:25.4 reported by the Deep Synoptic
    Array (DSA-110; Ravi+ 2023ApJ...949L...3R).

    In 2022, 17 observations with a total of 8.67hr exposure time were
    carried out. A high-cadence calibration signal was periodically
    injected during the first minute of observation for the subsequent
    flux and polarization calibration. The data were recorded in fits
    format with a time resolution of 49.152us, covering the frequency
    bandwidth from 1 to 1.5GHz with 4096 frequency channels.

Objects:
    ----------------------------------------------------------
        RA   (ICRS)   DE        Designation(s)
    ----------------------------------------------------------
     23 09 04.89  +48 42 25.0   FRB 20220912A = FRB 20220912A
    ----------------------------------------------------------

File Summary:
--------------------------------------------------------------------------------
 FileName    Lrecl  Records  Explanations
--------------------------------------------------------------------------------
ReadMe          80        .  This file
table1.dat     144     1076  The properties of the FRB 20220912A bursts
--------------------------------------------------------------------------------

See also:
 J/other/PASA/33.45 : FRBCAT: The Fast Radio Burst Catalog (Petroff+, 2016)
 J/ApJ/888/40   : Fast radio bursts with AstroSat/CZTI (Anumarlapudi+, 2020)
 J/ApJS/257/59  : First CHIME/FRB Fast Radio Burst Cat. (CHIME/FRB Col.+, 2021)
 J/ApJ/922/115  : Additional bursts at 1.4GHz for FRB 121102 (Aggarwal+, 2021)
 J/other/Nat/598.267 : List of radio bursts (Li+, 2021)
 J/MNRAS/500/655  : Gal. DM contribution to the extragalactic FRBs (Das+, 2021)
 J/MNRAS/509/1227 : Hidden repeating fast radio bursts (Chen+, 2022)
 J/MNRAS/511/1961 : New CHIME/FRB I catalog updates released (Hashimoto+, 2022)
 J/A+A/675/A99  : FRBs search with Fermi-LAT (Principe+, 2023)
 J/AJ/168/153   : Image-based blind search for FRBs in MWA 8yrs (Kemp+, 2024)
 J/A+A/693/A279 : The Apertif fast radio burst sample (Pastor-Marazuela+, 2025)
 J/A+A/698/A18  : Selected CHIME FRB sample (Zhang+, 2025)

Byte-by-byte Description of file: table1.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label      Explanations
--------------------------------------------------------------------------------
  1-   4 I4     ---      ID         [0/1075] Burst ID
  6-  20 F15.9  d        MJD        [59880.4/59935.4] Modified Julian Date
                                     (JD-2400000.5) (1)
 22-  27 F6.2   pc/cm3   DM         [212/230] Dispersion measure
 29-  32 F4.2   pc/cm3 e_DM         [0.03/8.2] Uncertainty in DM
 34-  40 F7.1   mJy      FluxPk     [16.4/12251] Peak Flux, calculated within
                                     500MHz bandwidth
 42-  46 F5.1   mJy    e_FluxPk     [0.2/151] Flux Uncertainty
 48-  52 F5.2   ms       EW         [0.09/33] Equivalent width
 54-  59 F6.1   MHz      FreqPk     [868/1622] Peak Frequency obtained with
                                     Gaussian fitting
 61-  65 F5.1   MHz    e_FreqPk     [1.4/647] Uncertainty in PeakFreq
 67-  72 F6.1   MHz      BandWidth  [28/1147] FWHM of Gaussian fitting
 74-  80 F7.1   MHz    e_BandWidth  [3/38964] Uncertainty in BandWidth
 82-  87 F6.3   Jy.ms    Fluence    [0.002/38] Fluence, calculated within
                                     500MHz bandwidth
 89-  93 F5.3   Jy.ms  e_Fluence    [0/0.5] Uncertainty in Fluence
 95- 101 F7.2   10+29J   E          [0.13/2723] Energy, 10+36erg
103- 108 F6.1   rad/m2   RM         [-122.1/79.5] Rotation measure
110- 114 F5.1   rad/m2 e_RM         [0/218] Lower uncertainty in RM
116- 120 F5.1   rad/m2 E_RM         [0/167] Upper uncertainty in RM
122- 126 F5.1   %        LPol       [27/243] Linear polarization degree
128- 132 F5.1   %      e_LPol       [0/106] Uncertainty in LPol
134- 139 F6.1   %        CPol       [-130/71.4] Circular polarization degree
141- 144 F4.1   %      e_CPol       [0/76] Uncertainty in CPol
--------------------------------------------------------------------------------
Note (1): Corresponding to the barycentrical arrival time at 1.5GHz
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                    Prepared by [AAS], Emmanuelle Perret [CDS] 03-Dec-2025
