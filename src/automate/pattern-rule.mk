.PHONY: clean

COUNT=bin/countwords.py

# Regenerate all results.
all : results/moby-dick.csv results/jane-eyre.csv results/time-machine.csv

# Regenerate result for any book.
results/%.csv : data/%.txt ${COUNT}
	python ${COUNT} $< > $@

# Remove all generated files.
clean :
	rm -f results/*.csv
