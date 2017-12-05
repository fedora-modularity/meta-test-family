LOGFILE=test_output.log

prepare-docker:
	MODULE=docker URL=fedora mtf-env-set

test: prepare-docker
	MODULE=docker URL=fedora mtf --metadata 2>&1 | tee $(LOGFILE)
	grep DockerLint $(LOGFILE)
	grep Add1 $(LOGFILE)
	grep /bin/true $(LOGFILE)
	grep "3/3" $(LOGFILE)
	grep -v not_schedule $(LOGFILE)
	grep -v rpmvalidation $(LOGFILE)
	MODULE=docker URL=fedora mtf --metadata *.sh 2>&1 | tee $(LOGFILE) && true
	grep "4/4" $(LOGFILE)

