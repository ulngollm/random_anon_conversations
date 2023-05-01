install:
	pip install -r requirements.txt
venv-start:
	source venv/bin/activate
venv-stop:
	deactivate
venv-init:
	python3 -m venv venv
create-migration:
	touch db/migrations/$(shell date +'%Y%m%d%H%M%S').py
migrate:
	find db/migrations/ -exec python3 {} \; 
start:
	nohup python3 main.py &