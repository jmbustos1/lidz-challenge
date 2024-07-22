.PHONY: django postgres dockerup api

django:
	docker exec -it lidz-django /bin/bash

postgres:
	docker exec -it lidz-postgres /bin/bash

api:
	docker exec -it lidztest-api-1 /bin/bash

dockerup:
	sudo docker-compose up
