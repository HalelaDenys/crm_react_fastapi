ENV_FILE=.env
DC=docker-compose
ENV_FILE_TEST=.env.test

up:
	${DC} --env-file ${ENV_FILE} up -d --build
down:
	${DC} --env-file ${ENV_FILE} down

upt:
	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} up --build -d --remove-orphans
downt:
	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} down

#test:
#	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} up --build -d --remove-orphans
#	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} exec -it fastapi_test_app bash -c "pytest -s -vvv"
#	${DC} -f docker-compose.test.yml --env-file ${ENV_FILE_TEST} down


#faststream docs serve src.infrastructure.fs_broker.broker:app --port 8081