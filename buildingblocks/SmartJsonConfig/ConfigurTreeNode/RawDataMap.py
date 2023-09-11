import json


class RawDataMap:
    def __init__(self, jsonconfig):
        datamap = json.loads(jsonconfig)['RawDataMap']
        self.Offset = datamap['Offset']
        self.Size = datamap['Size']
        self.Value = datamap['Value']
