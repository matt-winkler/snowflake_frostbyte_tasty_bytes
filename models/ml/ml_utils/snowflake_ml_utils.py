import logging
import pandas as pd

from snowflake.snowpark import Session

logger = logging.getLogger('snowflake.snowpark.session')
logger.setLevel(logging.INFO)

def model(dbt, session):
    
    def create_entity(
        session: Session,
        database: str,
        feature_store_name: str,
        default_warehouse: str,
        entity_name: str,
        join_keys: str,
        **kwargs
    ) -> None:
        
        from snowflake.ml.feature_store import FeatureStore, CreationMode, Entity
    
        fs = FeatureStore(
            session = session,
            database = database,
            name = feature_store_name,
            default_warehouse = default_warehouse,
            creation_mode = CreationMode.CREATE_IF_NOT_EXIST
        )
        
        e = Entity(
            name = entity_name,
            join_keys = join_keys.split(','),
            desc = kwargs.get("description", None)
        )

        fs.register_entity(e)
    
    def create_feature_view(
    ) -> None:
        pass
        
    create_entity_snowflake = session.sproc.register(
        func=create_entity,
        name="snowflake_ml__create_entity",
        is_permanent=True,
        replace=True,
        stage_location="@FORECAST_STAGE",
        packages=["snowflake-ml-python"],
        execute_as='caller'
    )
    
    return  pd.DataFrame.from_dict({'id': [1]})
