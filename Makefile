security:
	bandit ./bot/*.py

style:
	pylint -j 4 ./bot/*.py

up:
	docker-compose up
# must be perfomed on running container
test:
	python3 ./bot/test_main.py