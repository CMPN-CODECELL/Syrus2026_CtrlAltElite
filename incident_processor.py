def extract_info(incident):

    return {
        "service": incident.get("service"),
        "error": incident.get("error_log", ""),
        "description": incident.get("description", "")
    }