.PHONY: all clean

COUNT=bin/countwords.py

# Regenerate all results.
all : results/moby-dick.csv results/jane-eyre.csv results/time-machine.csv

# Regenerate results for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt ${COUNT}
	python ${COUNT} $< > $@

# Regenerate results for "Jane Eyre"
results/jane-eyre.csv : data/jane-eyre.txt ${COUNT}
	python ${COUNT} $< > $@

# Regenerate results for "The Time Machine"
results/time-machine.csv : data/time-machine.txt ${COUNT}
	python ${COUNT} $< > $@

# Remove all generated files.
clean :
	rm -f results/*.csv
