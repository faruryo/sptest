import traceback
from datetime import datetime
from typing import Dict

import ambient
import requests


class AmbientRepository:
    """
    A repository for storing data in Ambient.
    """

    def __init__(
        self, dataLink: Dict[int, Dict[str, str]]
    ):
        self.dataLink = dataLink

    def createDownload(self, data: dict):
        """
        data: {
            download: 12345.123,
            server: {
                id: "12345"
            },
            timestamp: '2021-01-03T07:27:13.070635Z'
        }
        """

        self._sentData("download", data["download"], data["server"]["id"], data["timestamp"])

    def createUpload(self, data: dict):
        """
        data: {
            upload: 12345.123,
            server: {
                id: "12345"
            },
            timestamp: '2021-01-03T07:27:13.070635Z'
        }
        """

        self._sentData("upload", data["upload"], data["server"]["id"], data["timestamp"])
    
    def _sentData(self, kind: str, data: float, server_id: str, timestamp: str):

        try:
            channel_id = self.dataLink[int(server_id)][kind]["channelId"]
            write_key = self.dataLink[int(server_id)][kind]["writeKey"]
            am = ambient.Ambient(channel_id, write_key)

            timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

            send_data = {
                "d1": data,
                "created": timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            }

            res = am.send(send_data)
            res.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            print('request failed: ', e)
            raise e
        except Exception as e:
            print(traceback.format_exc())
            raise e
