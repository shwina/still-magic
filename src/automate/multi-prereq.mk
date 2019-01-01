.PHONY: clean

COUNT=bin/countwords.py

# Regenerate all results.
all : results/moby-dick.csv results/jane-eyre.csv

# Regenerate results for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt ${COUNT}
	python ${COUNT} data/moby-dick.txt > results/moby-dick.csv

# Regenerate results for "Jane Eyre"
results/jane-eyre.csv : data/jane-eyre.txt ${COUNT}
	python ${COUNT} data/jane-eyre.txt > results/jane-eyre.csv

# Remove all generated files.
clean :
	rm -f results/*.csv
