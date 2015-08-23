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
	hello_world_quick.py emit-tool-contracts -o tool-contracts
	
py-tc: py-tool-contracts

clean-all:
	rm -rf py-examples/*/job_output
	rm -rf r-examples/*/job_output
	
	


