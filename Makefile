#init fresh dev environment
init:
	bash ./init.sh
	bash ./compose/local/export-requirements.sh
	bash ./compose/production/export-requirements.sh

#export fixed dev dependencies to requrements/local.txt (for docker)
cdev:
	bash ./compose/local/export-requirements.sh

#install dev dependencies and sync
idev:
	bash ./compose/local/install.sh

#export fixed prod dependencies to requrements/production.txt (for docker)
cprod:
	bash ./compose/production/export-requirements.sh

#grpc generation
protoc:
	python -m grpc_tools.protoc -I . --python_out=./src/lib/ --grpc_python_out=./src/lib/ ./pathfinder.proto --mypy_out=./src/lib/

#build docker image for local development. Need cdev to be run first
local:
	docker compose -f local.yml up -d
