def get_device_list(device_data):
    device_list = [
        {
            "enabled": device_info["device"]["enabled"],
            "device_id": device_info["device"]["device_id"],
            "device_name": device_info["device"]["device_name"],
            "host": device_info["device"]["host"],
            "protocol_name": device_info["device"]["protocol_name"],
            "connection_status": device_info["device"]["connection_status"],
        }
        for device_info in device_data.values()
    ]
    return device_list