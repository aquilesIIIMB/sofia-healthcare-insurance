#!/bin/bash

while getopts ":m:v:t:c:g:n:i:s:" opt; do
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
        c)
            CPU_MACHINE_NAME=${OPTARG}
            ;;
        g)
            GPU_MACHINE_NAME=${OPTARG}
            ;;
        n)
            GPU_MACHINE_CORES=${OPTARG}
            ;;
        i)
            CONTAINER_IMAGE_URI=${OPTARG}
            ;;
        s)
            SERVICE_ACCOUNT=${OPTARG}
            ;;
        \?)
            echo "Invalid option: -$OPTARG" 1>&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

# Obtain the current date and time in the desired format
# For example, YYYYMMDD-HHMMSS
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Combine the constant and the timestamp to form the job name
JOB_NAME="${MODEL_NAME}-${TIMESTAMP}"

# Check if GPU cores and GPU type are provided
if [[ -n $GPU_MACHINE_CORES ]] && [[ -n $GPU_MACHINE_NAME ]]; then
    # Execute command including GPU details
    gcloud ai custom-jobs create \
      --region=us-central1 \
      --display-name=$JOB_NAME \
      --service-account=$SERVICE_ACCOUNT \
      --labels=application_name={{cookiecutter.applicationName}},git_project={{cookiecutter.projectName}},model_name=$MODEL_NAME,git_branch=$GIT_BRANCH,version=$VERSION,component=preprocessing \
      --worker-pool-spec="machine-type=$CPU_MACHINE_NAME,accelerator-type=$GPU_MACHINE_NAME,accelerator-count=$GPU_MACHINE_CORES,container-image-uri=$CONTAINER_IMAGE_URI"
else
    # Execute command without GPU details
    gcloud ai custom-jobs create \
      --region=us-central1 \
      --display-name=$JOB_NAME \
      --service-account=$SERVICE_ACCOUNT \
      --labels=application_name={{cookiecutter.applicationName}},git_project={{cookiecutter.projectName}},model_name=$MODEL_NAME,git_branch=$GIT_BRANCH,version=$VERSION,component=preprocessing \
      --worker-pool-spec="machine-type=$CPU_MACHINE_NAME,container-image-uri=$CONTAINER_IMAGE_URI"
fi
