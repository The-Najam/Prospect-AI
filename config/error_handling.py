def is_rate_limit_error(error: Exception) -> bool:
    status_code = getattr(error, "status_code", None)
    response = getattr(error, "response", None)
    response_status = getattr(response, "status_code", None)

    if status_code == 429 or response_status == 429:
        return True

    message = str(error).lower()
    return (
        "rate limit" in message
        or "too many requests" in message
        or "status code: 429" in message
        or " 429" in message
    )
