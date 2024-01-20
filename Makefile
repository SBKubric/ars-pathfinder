init:
	bash ./init.sh
	bash ./compose/local/export-requirements.sh
	bash ./compose/production/export-requirements.sh

cdev:
	bash ./compose/local/export-requirements.sh

idev:
	bash ./compose/local/install.sh

cprod:
	bash ./compose/production/export-requirements.sh

local:
	docker compose -f local.yml up -d
