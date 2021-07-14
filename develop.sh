#!/bin/sh
export CONTAINER="organization-repositories-checker_web_1"
export IMAGE="organization-repositories-checker_web"
if [ $(docker ps -a | grep ${CONTAINER} | wc -l) == 1 ]; then
    docker start ${CONTAINER}
    docker exec -it ${CONTAINER} sh
else
    docker image build -t ${IMAGE} -f Dockerfile.develop .
    docker run -it --network host -w /app --name ${CONTAINER} -v ${PWD}:/app ${IMAGE} sh
fi
