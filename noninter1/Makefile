parallel:
	# seq 20 | parallel --joblog test.log -N0 --bar --halt now,fail=1 ./run.sh
	seq 100 | parallel --joblog test.log -N0 --bar ./run.sh
	cat test.log
