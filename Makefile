install:
	pip install -r requirements.txt
venv-start:
	source venv/bin/activate
venv-stop:
	deactivate
venv-install:
	python3 -m venv venv
create-migration:
	touch db/migrations/$(shell date +'%Y%m%d%H%M%S').py