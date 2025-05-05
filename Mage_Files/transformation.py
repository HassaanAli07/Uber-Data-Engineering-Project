import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df = df.drop_duplicates().reset_index(drop=True)
    df['trip_id'] = df.index
    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
    datetime_dim['pickup_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pickup_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pickup_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pickup_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pickup_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday

    datetime_dim['dropoff_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['dropoff_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['dropoff_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['dropoff_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['dropoff_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday

    datetime_dim['datetime_id'] = datetime_dim.index
    datetime_dim = datetime_dim[['datetime_id','tpep_pickup_datetime','pickup_hour','pickup_day','pickup_month','pickup_year','pickup_weekday','tpep_dropoff_datetime','dropoff_hour','dropoff_day','dropoff_month','dropoff_year','dropoff_weekday']]

    trip_distance_dim = df['trip_distance'].drop_duplicates().reset_index(drop=True)
    trip_distance_dim = trip_distance_dim.to_frame(name='trip_distance')
    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
    trip_distance_dim = trip_distance_dim[['trip_distance_id','trip_distance']]

    pickup_location_dim = df[['pickup_latitude','pickup_longitude']].drop_duplicates().reset_index(drop=True)
    pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
    pickup_location_dim = pickup_location_dim[['pickup_location_id','pickup_latitude','pickup_longitude']]
    
    dropoff_location_dim = df[['dropoff_latitude','dropoff_longitude']].drop_duplicates().reset_index(drop=True)
    dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
    dropoff_location_dim = dropoff_location_dim[['dropoff_location_id','dropoff_latitude','dropoff_longitude']]

    rate_code_dim = df['RatecodeID'].drop_duplicates().reset_index(drop=True)
    rate_code_dim = rate_code_dim.to_frame(name='RatecodeID')

    rate_code_name = {
    1 : 'Standard rate',
    2 : 'JFK',
    3 : 'Newark',
    4 : 'Nassau or Westchester',
    5 : 'Negotiated fare',
    6 : 'Group ride',
    99 : 'Null/unknown'
    }

    rate_code_dim['RateCode_name'] = rate_code_dim['RatecodeID'].map(rate_code_name)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim = rate_code_dim[['rate_code_id','RatecodeID','RateCode_name']]

    payment_type_dim = df['payment_type'].drop_duplicates().reset_index(drop=True)
    payment_type_dim = payment_type_dim.to_frame(name='payment_type')
    payment_type_dim['payment_type_id'] = payment_type_dim.index

    payment_type_name = {
    0 : 'Flex Fare trip',
    1 : 'Credit card',
    2 : 'Cash',
    3 : 'No charge',
    4 : 'Dispute',
    5 : 'Unknown',
    6 : 'Voided trip'
    }

    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
    payment_type_dim = payment_type_dim[['payment_type_id','payment_type','payment_type_name']]

    taxi_fact_table = df.merge(pickup_location_dim, on=['pickup_latitude','pickup_longitude'], how='left') \
                    .merge(dropoff_location_dim, on=['dropoff_latitude','dropoff_longitude'], how='left') \
                    .merge(datetime_dim, on=['tpep_pickup_datetime','tpep_dropoff_datetime'], how='left') \
                    .merge(trip_distance_dim, on='trip_distance', how='left') \
                    .merge(rate_code_dim, on='RatecodeID', how='left') \
                    .merge(payment_type_dim, on='payment_type', how='left') \
                    [['VendorID','datetime_id','rate_code_id','payment_type_id','pickup_location_id','dropoff_location_id','trip_distance_id','passenger_count','fare_amount','extra','mta_tax','tip_amount','tolls_amount','improvement_surcharge','total_amount']]
    

    return {
    "datetime_dim": datetime_dim.to_dict(orient="records"),
    "trip_distance_dim": trip_distance_dim.to_dict(orient="records"),
    "pickup_location_dim": pickup_location_dim.to_dict(orient="records"),
    "dropoff_location_dim": dropoff_location_dim.to_dict(orient="records"),
    "rate_code_dim": rate_code_dim.to_dict(orient="records"),
    "payment_type_dim": payment_type_dim.to_dict(orient="records"),
    "taxi_fact_table": taxi_fact_table.to_dict(orient="records")
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
