from datetime import datetime, timezone


def datetime_to_unix(datetime_str: str) -> int:
    """
    Convert a datetime string in the format 'YYYY-MM-DDTHH:MM:SS.sssZ' to Unix time.

    Args:
        datetime_str: The datetime string to convert.

    Returns:
        Unix time as an integer.
    """
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(dt.timestamp())


def unix_to_datetime(unix_time: int) -> str:
    """
    Convert Unix time to a datetime string in the format 'YYYY-MM-DDTHH:MM:SS.sssZ'.

    Args:
        unix_time: The Unix time to convert.

    Returns:
        Datetime string in the specified format.
    """
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"
