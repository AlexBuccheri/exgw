""" Converged settings for TiO2 ground state
TODO(Alex) We may want to use rgkmax = 9? Discuss with Andris
"""

converged_input_xml = """<?xml version="1.0" encoding="utf-8"?>
<input>

   <title>to2-rutile-PBEsol</title>

   <structure speciespath=".">
      <crystal  scale="1.000">
         <basevect>8.680645000000  0.000000000000  0.000000000000</basevect>
         <basevect>0.000000000000  8.680645000000  0.000000000000</basevect>
         <basevect>0.000000000000  0.000000000000  5.591116638050</basevect>
      </crystal>

      <species speciesfile="Ti.xml" rmt="1.80">
        <atom coord="0.000000000  0.000000000  0.000000000"></atom>
	    <atom coord="0.500000000  0.500000000  0.500000000"></atom>
      </species>

      <species speciesfile="O.xml" rmt="1.50">
	    <atom coord="0.303779258  0.303779258  0.000000000"></atom>
        <atom coord="0.696220742  0.696220742  0.000000000"></atom>
        <atom coord="0.803779258  0.196220742  0.500000000"></atom>
        <atom coord="0.196220742  0.803779258  0.500000000"></atom>
      </species>
   </structure>

   <groundstate
      do="fromscratch"
      rgkmax="8.0"
      ngridk="8 8 8"
      xctype="GGA_PBE_SOL"
      epsengy="1.e-6"
      gmaxvr="24.0"
      >
   </groundstate>

    {GW_INPUT}

</input>"""