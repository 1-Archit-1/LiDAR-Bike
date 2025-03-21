def extract_timestamp(filename:str, data_type:str)->float:
    """extract timestamp from filename"""
    try:
        timestamp_part = filename.replace(data_type+'_', '').replace('.bin', '')
        timestamp_main, timestamp_decimal = timestamp_part.split('_')
        timestamp = float(f"{timestamp_main}.{timestamp_decimal}")
        return timestamp
    except Exception as e:
        raise ValueError(f"Error in extract_timestamp: {e}")