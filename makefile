help:
	@echo "Run build to start the app."
	@echo "Run test to test the app."

build:
	docker-compose up -d

test:
	docker exec -it organization-repositories-checker_web_1 pytest