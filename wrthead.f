C
C$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
C WRTHEAD 
C$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
C write the headers for all the appropriate output files

      SUBROUTINE WRTHEAD (SMASS)

      IMPLICIT REAL*8 (A-H,O-Z)
      IMPLICIT LOGICAL*4(L)
C MHP 10/02 added proper dimensions for flaol2, fopal2
      CHARACTER*256 FISO,FLAOL2, FOPAL2
      COMMON/CKIND/RESCAL(4,50),NMODLS(50),IRESCA(50),LFIRST(50),
     1       NUMRUN
      COMMON/ZRAMP/RSCLZC(50), RSCLZM1(50), RSCLZM2(50),
     *             IOLAOL2, IOOPAL2, NK,
     *             LZRAMP, FLAOL2, FOPAL2
      COMMON/TRACK/ITRVER
      COMMON/LABEL/XENV0,ZENV0
      COMMON/CONST/CLSUN,CLSUNL,CLNSUN,CMSUN,CMSUNL,CRSUN,CRSUNL,CMBOL
      COMMON/CONST3/CDELRL,CMIXL,CMIXL2,CMIXL3,CLNDP,CSECYR
      COMMON/LUOUT/ILAST,IDEBUG,ITRACK,ISHORT,IMILNE,IMODPT,ISTOR,IOWR
      COMMON/LUNUM/IFIRST, IRUN, ISTAND, IFERMI,
     1    IOPMOD, IOPENV, IOPATM, IDYN,
     2    ILLDAT, ISNU, ISCOMP, IKUR
      COMMON/CHRONE/LRWSH, LISO, IISO, FISO
      COMMON/CCOUT2/LDEBUG,LCORR,LMILNE,LTRACK,LSTPCH
      SAVE

      IF (IRESCA(NK) .EQ. 1) THEN
         WRITE(IOWR, 47) NK, XENV0, ZENV0, CMIXL, NMODLS(NK)
      ELSE IF (IRESCA(NK) .EQ. 2) THEN
         WRITE(IOWR, 48) NK, XENV0, ZENV0, CMIXL, NMODLS(NK)
      ELSE IF (IRESCA(NK) .EQ. 3) THEN
         WRITE(IOWR, 49) NK, XENV0, ZENV0, CMIXL, NMODLS(NK)
      END IF
  47  FORMAT(/, ' RUN=',I2,' EVOLVE  ', ' X=',F8.6,
     *       ' Z=',F8.6,' CMIXL=', F8.6, ' NO.MODS=', I5)
  48  FORMAT(/, ' RUN=',I2,' RESCALE ', ' X=',F8.6,
     *       ' Z=',F8.6,' CMIXL=', F8.6, ' NO.MODS=', I5)
  49  FORMAT(/, ' RUN=',I2,' RESCALE&EVOLVE ', ' X=',F8.6,
     *       ' Z=',F8.6,' CMIXL=', F8.6, ' NO.MODS=', I5)

      IF (LISO) THEN
C header stuff for isochrone output 
         GMMASS = SMASS*CMSUN           
         WRITE(IISO, 1495) GMMASS,
     *        XENV0,ZENV0,CMIXL,CMBOL
 1495    FORMAT(7X, 1P5E16.8)
      END IF

      IF (LTRACK .AND. LFIRST(NK)) THEN
C ITRVER identifies version of track out file.  If you change
C the track out file then change this version number.
         WRITE(ITRACK, 1500)ITRVER,SMASS,XENV0,ZENV0,CMIXL
 1500    FORMAT('#Version=',i3,'  Mtot/Msun =',1PE16.8,
     *        '  Initial: X =',1PE16.8,' Z =',1PE16.8,
     *        '  Mix. length =', 1PE16.8)  
         IF(ITRVER .EQ. 0) THEN      
C            WRITE(ITRACK, 1503)
C 1503       FORMAT(
C     1'# Model #, shells, AGE(Gyr), log(L/Lsun), log(R/Rsun), log(g),',
C     1' log(Teff), Mconv. core (Msun), Mconv. env, R,T,Rho,P,cappa env',/,
C     2'# Central: log(T), log(RHO), log(P), BETA, ETA, X, Y, Z',/,
C     3'# Luminosity: ppI, ppII, ppIII, CNO, triple-alpha,',
C     3' He-C, gravity, neutrinos (old)',/,
C     3'# Cl SNU, Ga SNU, Neutrinos (1E10 erg/CM^2 at earth): pp, pep, hep, Be7,',
C     3' B8, N13, O15, F17 2xdiagnostic',/,
C     4'# Central Abundances: He3, C12, C13, N14, N15, O16,',
C     4' O17, O18',/,
C     5'# Surface Abundances: He3, C12, C13, N14, N15, O16,',
C     5' O17,O18 H2, Li6, Li7, Be9 X Y Z Z/X',/,
C     6'# Jtot, KE rot tot, total I, CZ I, Omega center, surface, Prot (day), Vrot (km/s), TauCZ (sec) ',/,
C     7'# H shell loc: mass frac-base, midpoint, top; radius frac-',
C     7'base, midpoint, top, Pphot, mass (msun)')
            
C G Somers 11/14; Added option to create .track file header. Uncomment the following
C     block if desired.
c$$$            WRITE(ITRACK, 1504)
c$$$ 1504       FORMAT(
c$$$     2'       Mconv.core      Mconv.env     Rcore     Tcore      Rho_core     P_core     kappa_env   ',
c$$$     2' log(T)_cen     log(Rho)_cen     log(P)_cen        BETA             ETA            X_cen      ',
c$$$     2'     Y_cen           Z_cen          ppI_lum         ppII_lum       ppIII_lum        CNO_lum   ',
c$$$     2'    3-alpha_lum       He-C_lum        gravity       OLD NUTRINOS   Cl SNU    Ga SNU    **pp** ',
c$$$     2'   **pep**   **hep**   **Be7**   **B8**    **N13**   **O15**   **F17**  **diag1** **diag2**   ',
c$$$     2'   He3_cen        C12_cen         C13_cen         N14_cen         B10_cen         O16_cen     ',
c$$$     2'    B11_cen         O18_cen         He3_surf        C12_surf        C13_surf        N14_surf  ',
c$$$     2'      B10_surf        O16_surf        B11_surf        O18_surf        H2_surf         Li6_surf',
c$$$     2'        Li7_surf        Be9_surf         X_surf          Y_surf          Z_surf         Z/X_su',
c$$$     2'rf          Jtot         KE_rot_tot       total I           CZ I         Omega_surf      Omega',
c$$$     2'_cen       Prot (days)     Vrot (km/s)     TauCZ (s)       Mfrac_base      Mfrac_midp      Mfr',
c$$$     2'ac_top       Rfrac_base      Rfrac_midp      Rfrac_top         P_phot           Mass     ',/,
c$$$     2'# ')
C G Somers END.

C     V SMEDILE 3/2024 Modified SOMERS to make pandas.read_csv easier
C     Block if desired
            WRITE(ITRACK, 1505)
 1505       FORMAT(
     1'  ',/,
     2'    Step    Shls     Age(Gyr)      log(L/Lsun)    log(R/Rsun)        log(g)        log(Teff)',
     2'       Mconv.core      Mconv.env     Rcore     Tcore      Rho_core     P_core     kappa_env   ',
     2' log(T)_cen     log(Rho)_cen     log(P)_cen        BETA             ETA            X_cen      ',
     2'     Y_cen           Z_cen          ppI_lum         ppII_lum       ppIII_lum        CNO_lum   ',
     2'    3-alpha_lum       He-C_lum        gravity       OLD_NUTRINOS   Cl_SNU    Ga_SNU    **pp** ',
     2'   **pep**   **hep**   **Be7**   **B8**    **N13**   **O15**   **F17**  **diag1** **diag2**   ',
     2'   He3_cen        C12_cen         C13_cen         N14_cen         B10_cen         O16_cen     ',
     2'    B11_cen         O18_cen         He3_surf        C12_surf        C13_surf        N14_surf  ',
     2'      B10_surf        O16_surf        B11_surf        O18_surf        H2_surf         Li6_surf',
     2'        Li7_surf        Be9_surf         X_surf          Y_surf          Z_surf         Z/X_su',
     2'rf          Jtot         KE_rot_tot       total_I           CZ_I         Omega_surf      Omega',
     2'_cen       Prot(days)     Vrot(km/s)     TauCZ(s)       Mfrac_base      Mfrac_midp      Mfr',
     2'ac_top       Rfrac_base      Rfrac_midp      Rfrac_top         P_phot           Mass     ',/,
     2'  ')
C      V Smedile END.

         ELSE IF(ITRVER .EQ. 1) THEN      
            WRITE(ITRACK, 1506)
 1506       FORMAT(
     1'# Model #, shells, AGE, log(L/Lsun), log(R/Rsun), log(g),',
     1' log(Teff), Mconv. core, Mconv. env.)' ,/,
     2'# Central: log(T), log(RHO), log(P), BETA, ETA, X, Y, Z',/,
     3'# Luminosity: ppI, ppII, ppIII, CNO, triple-alpha,',
     3' He-C, gravity, neutrinos (old)',/,
     3' Neutrinos (1E10 erg/CM^2 at earth): pp, pep, hep, Be7,',
     3' B8, N13, O15, F17',/,
     4'# Central Abundances: He3, C12, C13, N14, N15, O16,',
     4' O17, O18',/,
     5'# Surface Abundances: He3, C12, C13, N14, N15, O16,',
     5' O17,O18',/,
     6'    "        " cont: H2, Li6, Li7, Be9',/,
     7'# H shell loc: mass frac-base, midpoint, top; radius frac-',
     7'base, midpoint, top')
         ELSE IF(ITRVER .EQ. 2) THEN
            WRITE(ITRACK, 1505)
            WRITE(ITRACK, 1510)
 1510       FORMAT(
     1' Jtot, K.E. Rotation, OMEGAsurf, OMEGAcenter')
         ELSE IF(ITRVER .EQ. 3) THEN
	    WRITE(ITRACK, 1515)
 1515       FORMAT(
     1'#Model #, shells, AGE, log(L/Lsun), log(R/Rsun), log(g),',
     1' log(Teff), Mconv. core, Mconv. env., % Grav Energy, X env')
         END IF 
      END IF

      RETURN
      END
