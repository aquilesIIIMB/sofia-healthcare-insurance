CREATE OR REPLACE TABLE `@PROJECT_ID.model_test_iris_us.test_dataset_iris_predictions` AS

WITH
  randomly_sorted_users AS (
    SELECT
      *,
      ROW_NUMBER() OVER(PARTITION BY species
      ORDER BY
        rand()) AS random_sort
    FROM
      `bigquery-public-data.ml_datasets.iris`     
)

SELECT
  * EXCEPT(random_sort)
FROM
  randomly_sorted_users
WHERE
  random_sort <= 5
