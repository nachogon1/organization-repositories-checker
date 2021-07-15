help:
	@echo "Run build to start the app."
	@echo "Run test to test the app."
	@echo "Run schedule to activate the organization checker cron job."

build:
	docker-compose up -d

schedule:
	docker exec -it organization-repositories-checker_web_1 python scheduler/scripts.py

test:
	docker exec -it organization-repositories-checker_web_1 pytest