SHELL=/bin/bash -o pipefail

PARALLEL_TASKS := 100

clean:
	rm -rf logs

parallel-master: clean
	cp osparc_conf_osparcmaster.json osparc_conf.json
	mkdir -p logs
	seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar 'set -o pipefail; ./run.sh {} 2>&1 | tee logs/{}.log'
	cat test.log
parallel-awsmaster: clean
	cp osparc_conf_osparcawsmaster.json osparc_conf.json
	mkdir -p logs
	seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar 'set -o pipefail; ./run.sh {} 2>&1 | tee logs/{}.log'
	cat test.log
plot:
	python read_log.py
