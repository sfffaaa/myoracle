HOME_FOLDER=`echo $$HOME`

GETH_PID:=$(shell ps aux | grep geth | grep -v grep | grep -v make | awk '{print $$2}')
GETH_PATH="$(HOME_FOLDER)/myoracle/backend/travisCI"

TRUFFLE_PID:=$(shell ps aux | grep truffle | grep "truffle develop" | grep -v grep | grep -v make | awk '{print $$2}')
TRUFFLE_PATH="$(HOME_FOLDER)/myoracle/solidity"

BACKEND_PATH="$(HOME_FOLDER)/myoracle/backend"
SOLIDITY_PATH="$(HOME_FOLDER)/myoracle/solidity"

.PHONY: install uninstall clean geth truffle test_backend test_solidity stop

stop: stop_geth stop_truffle
	@echo "stop all chain"

test_backend:
	@[ -n "$(GETH_PID)" ] || (echo "You should execute 'make geth' first!"; exit 1)
	(cd $(BACKEND_PATH); sh testcase/test_run.sh)

test_solidity:
	@[ -n "$(TRUFFLE_PID)" ] || (echo "You should execute 'make truffle' first!"; exit 1)
	(cd $(SOLIDITY_PATH); truffle test)

stop_geth:
	@[ -z "$(GETH_PID)" ] || (kill $(GETH_PID))

stop_truffle:
	@[ -z "$(TRUFFLE_PID)" ] || (kill $(TRUFFLE_PID))

geth: stop_truffle
	@echo "start geth!! $(GETH_PID)"
	@[ -n "$(GETH_PID)" ] || (cd $(GETH_PATH); sh startnode1.sh)

truffle: stop_geth
	@echo "start truffle!!"
	@[ -n "$(TRUFFLE_PID)" ] || (cd $(TRUFFLE_PATH); truffle develop)

install:
	pip3 install -r "$(BACKEND_PATH)/requirements.txt"

uninstall:
	echo "do nothing"

clean:
	find . -name '*.swp' -delete

help:
	@echo "Have several config for useage:"
	@echo "    install uninstall clean geth truffle test_backend test_solidity stop"
	@echo "Frequenctly use:"
	@echo "    geth truffle test_backend test_solidity stop"
