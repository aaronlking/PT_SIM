msg="\n\n\#\#\n\#\#\n\#\# This file was generated by a script. Don't edit it.\n\#\#\n\#\#"


all: ptsim ptsim-clock theBigDiffer

ptsim: scripts/pt-sim.sh
	cp scripts/pt-sim.sh ptsim
	@echo -e ${msg} >> ptsim

ptsim-clock: scripts/pt-sim-clock.sh
	cp scripts/pt-sim-clock.sh ptsim-clock
	@echo -e ${msg} >> ptsim-clock

# Hard - Coded Quick Testing.
theBigDiffer: scripts/theBigDiffer.sh
	cp scripts/theBigDiffer.sh theBigDiffer
	@echo -e ${msg} >> theBigDiffer

# Hard - Coded Quick Testing.
# I can probably use script from 460::P2.
check: ptsim ptsim-clock theBigDiffer
	sh theBigDiffer

clean:
	rm -f ptsim ptsim-clock theBigDiffer *.out

# My typos aren't going away anytime soon.
celan: 
	rm -f ptsim ptsim-clock theBigDiffer *.out
