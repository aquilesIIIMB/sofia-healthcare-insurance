#!/bin/bash

while getopts ":m:v:t:p:d:" opt; do
    echo ${getopts}
    case ${opt} in
        m)
            MODEL_NAME=${OPTARG}
            ;;
        v)
            VERSION=${OPTARG}
            ;;
        t)
            GIT_BRANCH=${OPTARG}
            ;;
        p)
            PYTHON_VERSION=${OPTARG}
            ;;
        d)
            CONTAINER_DESCRIPTION=${OPTARG}
            ;;
        \?)
            echo "Usage: cmd "
            exit 1
            ;;
        :)
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            exit 1
            ;;
    esac
done

repository=us-central1-docker.pkg.dev
project=ml-framework-maas
app_prefix=$(basename "$(dirname "$(dirname "$PWD")")")
project_prefix=$(basename "$(dirname "$(dirname "$(dirname "$(dirname "$PWD")")")")")
img_name=$(basename "$PWD")

gcloud artifacts repositories create $project_prefix --repository-format=docker --location=us-central1 --description="${CONTAINER_DESCRIPTION}" --labels=application_name={{cookiecutter.applicationName}},git_project={{cookiecutter.projectName}},model_name=$MODEL_NAME,git_branch=$GIT_BRANCH,version=$VERSION
docker build --tag $repository/$project/$project_prefix/$app_prefix/$MODEL_NAME/$img_name:$VERSION --build-arg PYTHON_VERSION=$PYTHON_VERSION .
docker image prune --force
docker push $repository/$project/$project_prefix/$app_prefix/$MODEL_NAME/$img_name:$VERSION

echo "CONTAINER_IMAGE_URI:"
echo $repository/$project/$project_prefix/$app_prefix/$MODEL_NAME/$img_name:$VERSION
