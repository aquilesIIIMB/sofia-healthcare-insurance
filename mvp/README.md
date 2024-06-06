# MVP

# Project Manifest Documentation

## Manifest
This section contains the overall configuration and specifications of the project.
[manifest.json](./manifest.json)

### Technical Information
Information related to the technical aspects of the project.

| Parameter | Description |
| --------- | ----------- |
| `projectName` | The name of the Git project, as defined in the project's configuration (`{{cookiecutter.projectName}}`). |
| `appName` | The name of the application associated with this project (`{{cookiecutter.applicationName}}`). |
| `modelingFrequency` | The frequency at which the modeling tasks are performed. This could be a cron expression or a simple description like 'daily' or 'weekly' and specify the time execution. |
| `predictionConsumptionFrequency` | Details how often predictions are made if they are scheduled. Can be a time interval, a cron expression or an empty value. |
| `embeddingConsumptionFrequency` | Details how often embeddings are consumed. Can be a time interval, a cron expression or an empty value. |

#### Prediction Type
Details the type of predictions made by the model.

| Parameter | Description |
| --------- | ----------- |
| `batchInference` | Indicates whether the model performs batch inference (`true` or `false`). |
| `onlineInference` | Indicates if the model is capable of performing online inference (`true` or `false`). |
| `vectorEngine` | Indicates if a vector engine is used to enable the embedding consumption (`true` or `false`). |

#### Model Type
The type of model used in the project.

| Parameter | Description |
| --------- | ----------- |
| `classification` | Indicates if it's a classification model (`true` or `false`). |
| `regression` | Indicates if the model is a regression model (`true` or `false`). |
| `recommendation` | Indicates if the model is used for recommendations (`true` or `false`). |
| `clustering` | Indicates if it's a clustering model (`true` or `false`). |
| `timeSeries` | Indicates if the model is used for time series forecasting (`true` or `false`). |

#### Additional Technical Information

| Parameter | Description |
| --------- | ----------- |
| `algorithmType` | The type of algorithm used in the model. Could be CNN, Transformers, LightFM, collaborative filtering, etc |
| `dataSourcesUsed` | A list of data sources used in the project. This could be Bigquery URIs or/and GCS Bucket URIs |
| `featureSchema` | The schema of the features used in the model. |
| `predictionSchema` | The schema of the predictions. |

### Business
Information related to the business aspect of the project.

#### Development Team
Details of the team developing this project.

| Parameter | Description |
| --------- | ----------- |
| `businessUnit` | The business unit to which the development team belongs. |
| `area` | The specific area or department of the development team. |
| `team` | The name of the development team. |
| `techLead` | The tech lead of the development team. |
| `productOwner` | The product owner for this project. |
| `costCenter` | The cost center associated with the development team. |

#### Consumption Team
Details of the teams consuming the output of this project.

| Parameter | Description |
| --------- | ----------- |
| `businessUnit` | The business unit to which the consumption team belongs. |
| `area` | The specific area or department of the consumption team. |
| `team` | The name of the consumption team. |
| `teamFocal` | The main contact person of the consumption team. |
| `costCenter` | The cost center associated with the consumption team. |
| `consumptionFrequency` | How frequently the team consumes the output of the model. |

### Management
Information related to the management of the project.

| Parameter | Description |
| --------- | ----------- |
| `projectFocal` | The main contact person for the project. |
| `modelingSupport` | Individuals or teams providing support for modeling tasks. |
| `dataSupport` | Individuals or teams providing data support. |

#### Sensitive Data Handling

| Parameter | Description |
| --------- | ----------- |
| `sensitiveDataConsumer.personallyIdentifiableInformation` | Indicates if personally identifiable information is consumed (`true` or `false`). |
| `sensitiveDataConsumer.financialInformation` | Indicates if financial information is consumed (`true` or `false`). |
| `sensitiveDataConsumer.healthData` | Indicates if health data is consumed (`true` or `false`). |
| `sensitiveDataExposer.personallyIdentifiableInformation` | Indicates if personally identifiable information is exposed (`true` or `false`). |
| `sensitiveDataExposer.financialInformation` | Indicates if financial information is exposed (`true` or `false`). |
| `sensitiveDataExposer.healthData` | Indicates if health data is exposed (`true` or `false`). |
