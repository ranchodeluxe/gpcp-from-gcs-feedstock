# s3://gcorradini-forge-test-inputs/cache/agcd_v1_precip_total_r005_daily_1971.nc
# pangeo-forge-runner bake --repo=https://github.com/carbonplan/leap-pgf-example/ -f /Users/ranchodeluxe/apps/leap-pgf-example/feedstock/runner_config.py --Bake.job_name=agcd --Bake.bakery_class="pangeo_forge_runner.bakery.flink.FlinkOperatorBakery"
# pangeo-forge-runner bake --repo=https://github.com/ranchodeluxe/gpcp-from-gcs-feedstock.git --ref="test/integration" -f /Users/ranchodeluxe/apps/leap-pgf-example/feedstock/runner_config.py --FlinkOperatorBakery.task_manager_resources='{"memory": "2048m", "cpu": 0.2}' --FlinkOperatorBakery.job_manager_resources='{"memory": "2048m", "cpu": 0.2}' --Bake.job_name=recipe --Bake.bakery_class="pangeo_forge_runner.bakery.flink.FlinkOperatorBakery"

# --FlinkOperatorBakery.task_manager_resources='{"memory": "2048m", "cpu": 0.2}'

# Let's put all our data into s3!
BUCKET_PREFIX = "s3://gcorradini-forge-test-inputs"

c.TargetStorage.fsspec_class = "s3fs.S3FileSystem"
# Target output should be partitioned by job id
c.TargetStorage.root_path = f"{BUCKET_PREFIX}/{{job_name}}/output"
c.TargetStorage.fsspec_args = {
    "key": "ASIAWOY6ET4O2CUIFBDR",
    "secret": "+ok5ckfLdvyfdxrMFGm9Kv71QwKJQmW13XD6U3W+",
    "token": "IQoJb3JpZ2luX2VjEBYaCXVzLXdlc3QtMSJIMEYCIQCVRpRNz2Mp9PfHM8hu8KJCO33Eommvqdj41SPSGvfvGgIhAPSrhCBV301c8r6+ELzFF1ABIBuAQmmKx1tOsQRleB5mKu8BCC8QABoMNDQ0MDU1NDYxNjYxIgziMMYvsOhM/RsRVj4qzAGvvhXxNOnK9/LizREmoNv3SEKkDHwCE3dxG0wTx/oNI20aDU4aHukNGZaj58MYduAhNqJD0l1AzsG8vEyTF4sh0cmRnkCa1vUjPXnwJfLnrTOxGaZ2lV91eMC0dKQ/ZQTu2CsWa5tg2o9RnCRt7o+sNIKtGZacaRbtFpES2BmUSjdcDSM8GxBo0PA6dywYXeW0Q7j2IIOu43pLhoPqiaBHb7rSvsCPK37MzvmpgzqzooU7CXCSlWFJUh27l6edSgoP1L9GuzHzCqUSKdwwxJulqQY6lwG+A4B+5F9WzFE6wyVFWKrB06KMe0w5T0dzVXutsTrXNGX1gQs2ZSwpwxMbRHxS5QPun1atsb4v4ALwZgQpQR7Db/+QUcaJAeEmawC6MhGr8Y1uN6zuKTtyxKIsHwz0czR1z38dca3DjJkr03W0mp6M6j65sYjFyVlrJF913u0Cv7gbK7c5amJnIweIwxKo53nzDYIlhW/D",
    "client_kwargs":{"region_name":"us-west-2"}
}

c.InputCacheStorage.fsspec_class = c.TargetStorage.fsspec_class
c.InputCacheStorage.fsspec_args = c.TargetStorage.fsspec_args
# Input data cache should *not* be partitioned by job id, as we want to get the datafile
# from the source only once
c.InputCacheStorage.root_path = f"{BUCKET_PREFIX}/cache/input"