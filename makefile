help:
	@echo "Run build to start the app."
	@echo "Run test to test the app."

build:
	docker-compose up -d
	bash develop.sh

test:
	docker exec -it yara_challnge_web_1 pytest