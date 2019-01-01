# Regenerate results for "Moby Dick"
results/moby-dick.csv : data/moby-dick.txt
	python bin/countwords.py data/moby-dick.txt > results/moby-dick.csv
