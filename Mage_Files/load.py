from os import path

from pandas import DataFrame

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mongodb import MongoDB

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
# def export_data_to_mongodb(df: DataFrame, **kwargs) -> None:
#     config_path = path.join(get_repo_path(), 'io_config.yaml')
#     config_profile = 'default'

#     MongoDB.with_config(ConfigFileLoader(config_path, config_profile)).export(
#         DataFrame(df['taxi_fact_table']),
#         collection='uber_data_collections',
#     )
def export_data_to_mongodb(df: DataFrame, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Define a dictionary with all the dataframes and their corresponding collection names
    dataframes_to_export = {
        'taxi_fact_table': 'uber_data_collections',  # Already loaded, but for consistency
        'datetime_dim': 'datetime_collection',
        'trip_distance_dim': 'trip_distance_collection',
        'pickup_location_dim': 'pickup_location_collection',
        'dropoff_location_dim': 'dropoff_location_collection',
        'rate_code_dim': 'rate_code_collection',
        'payment_type_dim': 'payment_type_collection',
    }

    # Loop through each dataframe and export it to its respective collection
    for dataframe_name, collection_name in dataframes_to_export.items():
        if dataframe_name in df:  # Ensure that the dataframe is available in the input df
            MongoDB.with_config(ConfigFileLoader(config_path, config_profile)).export(
                DataFrame(df[dataframe_name]),
                collection=collection_name,
            )

    return "Success"