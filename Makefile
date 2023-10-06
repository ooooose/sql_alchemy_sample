build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

shell:
	docker-compose exec app bash

logs:
	docker-compose logs -f app

ps:
	docker-compose ps -a
