.PHONY: build-ve install

build-ve:
	virtualenv ve

install:
	source ve/bin/activate
	pip install -r REQUIREMENTS.txt

# Most of these are pulled directly from the pbcommand CLI examples
py-tool-contracts:
	python -m pbcommand.cli.examples.dev_txt_app --emit-tool-contract >  tool-contracts/dev_example_tool_contract.json
	python -m pbcommand.cli.examples.dev_app --emit-tool-contract > tool-contracts/dev_example_dev_txt_app_tool_contract.json
	python -m pbcommand.cli.examples.dev_quick_hello_world emit-tool-contracts -o tool-contracts
	python -m pbsmrtpipe.pb_tasks.dev emit-tool-contracts -o tool-contracts
	hello_world.py emit-tool-contracts -o tool-contracts
	
py-tc: py-tool-contracts

clean:
	find py-examples -name "0.*" -delete 
	find r-examples -name "0.*"  -delete
	rm -rf py-examples/*/job_output
	rm -rf r-examples/*/job_output

test-py:
	cd py-examples/01-helloworld/ && pbtestkit-runner --debug testkit.cfg
test-r:
	cd r-examples/01-helloR/ && pbtestkit-runner --debug testkit.cfg
	cd r-examples/02-pbcommandr-dev/ && pbtestkit-runner --debug testkit.cfg
	cd r-examples/03-pbcommandr-all/ && pbtestkit-runner --debug testkit.cfg

r-tool-contracts:
	hello_world.R emit-tc tool-contracts

r-tc: r-tool-contracts

test: test-py test-r
	


