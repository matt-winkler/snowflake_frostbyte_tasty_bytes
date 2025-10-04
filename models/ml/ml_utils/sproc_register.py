import logging
import pandas as pd
from snowflake.snowpark import Session

logger = logging.getLogger('snowflake.snowpark.session')
logger.setLevel(logging.INFO)

def model(dbt, session):

    def write_to_feature_store(
        session: Session
    ) -> None:
        
        from snowflake.ml.feature_store import FeatureStore, CreationMode, Entity
    
        fs = FeatureStore(
            session=session,
            database="MATT_W_ANALYTICS_DEV",
            name="dbt_mwinkler_ml_feature_store",
            default_warehouse="MATT_W_DEV_WH",
            creation_mode=CreationMode.CREATE_IF_NOT_EXIST
        )
        
    write_to_feature_store_snowflake = session.sproc.register(
        func=write_to_feature_store,
        name="sproc_write_to_feature_store",
        is_permanent=True,
        replace=True,
        stage_location="@FORECAST_STAGE",
        packages=["snowflake-ml-python"]
    )
    
    return  pd.DataFrame.from_dict({'id': [1]})
