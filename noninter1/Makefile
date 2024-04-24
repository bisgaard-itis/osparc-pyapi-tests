
PARALLEL_TASKS := 100

clean:
	rm -rf logs

parallel-master: clean
	# seq 20 | parallel --joblog test.log -N0 --bar --halt now,fail=1 ./run.sh
	cp osparc_conf_osparcmaster.json osparc_conf.json
	mkdir -p logs
	seq ${PARALLEL_TASKS} | parallel -j ${PARALLEL_TASKS} --tag -v --joblog test.log --bar stdbuf -oL ./run.sh {} '2>&1 |' tee logs/{}.log
	# seq ${PARALLEL_TASKS} | parallel --tmuxpane --joblog test.log --bar ./run.sh {} '>' logs/{}.log
	cat test.log
parallel-awsmaster:
	# seq 20 | parallel --joblog test.log -N0 --bar --halt now,fail=1 ./run.sh
	seq ${PARALLEL_TASKS} | parallel --joblog test.log -N0 --bar ./run.sh
	cat test.log

