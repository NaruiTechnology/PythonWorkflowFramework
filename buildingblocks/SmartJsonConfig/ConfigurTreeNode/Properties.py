import json

class Properties(object):
    def __init__(self, jsonconfig):
        properties = json.loads(jsonconfig)["Properties"]
        self.Type = properties['pType']
        self.Options = properties['Options']
        self.Default = properties['Default']
        self.CurrentValue = properties['CurrentValue']
