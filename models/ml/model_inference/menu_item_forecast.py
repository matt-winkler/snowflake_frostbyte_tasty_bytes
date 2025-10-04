import snowflake.snowpark.functions as F
from snowflake.snowpark import Session
import logging

logger = logging.getLogger('snowflake.snowpark.session')
logger.setLevel(logging.INFO)

def model(dbt, session):
    #dbt.config(packages=["snowflake-ml-python"])
    # def write_to_feature_store(
    #     session: Session
    # ) -> None:
    #     from snowflake.ml.feature_store import FeatureStore, CreationMode, Entity

    #     fs = FeatureStore(
    #         session=session,
    #         database="MATT_W_ANALYTICS_DEV",
    #         name="dbt_mwinkler_ml_feature_store",
    #         default_warehouse="SNOWFLAKE_LEARNING_WH",
    #         creation_mode=CreationMode.CREATE_IF_NOT_EXIST
    #     )
    
    # write_to_feature_store_snowflake = session.sproc.register(
    #     func=write_to_feature_store,
    #     name="sproc_write_to_feature_store",
    #     is_permanent=True,
    #     replace=True,
    #     stage_location="@FORECAST_STAGE",
    #     packages=["snowflake-ml-python"]
    # )

    # feature_store_result = write_to_feature_store_snowflake(
    #     session
    # )

    df_future_dates = dbt.ref("get_sales_short_term_trends")

    #this is to reference the UDF creation 
    demand_forecast_udf = dbt.ref("demand_forecast_train_metrics")

    feature_cols = df_future_dates.drop(
        "MENU_ITEM_ID",
        "MENU_TYPE",
        "CITY",
        "LOCATION_ID",
        "DATE",
        "YEAR",
    ).columns


    df_predictions = df_future_dates.select(
        F.dateadd("day", -(F.col("day_of_week") + 9), F.col("date")).alias("forecast_execution_date"),
        "location_id",
        "date",
        "shift",
        "menu_item_id",
        F.call_udf("udf_xgboost_predict_demand", [F.col(c) for c in feature_cols]).alias("prediction")
    )

    return df_predictions