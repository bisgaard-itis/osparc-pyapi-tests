SHELL=/bin/bash -o pipefail

PARALLEL_TASKS := 100

clean:
	rm -rf logs

parallel-master: clean
	# seq 20 | parallel --joblog test.log -N0 --bar --halt now,fail=1 ./run.sh
	cp osparc_conf_osparcmaster.json osparc_conf.json
	mkdir -p logs
	seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar 'set -o pipefail; ./run.sh {} 2>&1 | tee logs/{}.log'
	# seq ${PARALLEL_TASKS} | parallel --tmuxpane --joblog test.log --bar ./run.sh {} '>' logs/{}.log
	cat test.log
parallel-awsmaster: clean
	cp osparc_conf_osparcawsmaster.json osparc_conf.json
	mkdir -p logs
	# seq 20 | parallel --joblog test.log -N0 --bar --halt now,fail=1 ./run.sh
	#seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar ./run.sh {} '2>&1'
	#seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar ./run.sh {} '2>&1 |' tee logs/{}.log 
	seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar 'set -o pipefail; ./run.sh {} 2>&1 | tee logs/{}.log'
	cat test.log

