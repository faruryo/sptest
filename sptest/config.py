import yaml

_INI_CONF = {
    "speedtest": {
        "servers": None,
        "threads": 1
    },
    "ambient": {
        "channelId": 0,
        "writeKey": "",
        "dataLink": {}
    }
}


def load_config(filpath: str) -> dict:
    if not filpath:
        return _INI_CONF

    with open(filpath) as file:
        config = yaml.safe_load(file)
        if not config:
            return _INI_CONF

        return dict(_INI_CONF, **config)

    return _INI_CONF
