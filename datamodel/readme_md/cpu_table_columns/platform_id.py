from buildingblocks.decorators import hierarchyValidation
from datamodel.readme_md.cpu_attribute import cpu_attribute


class platform_id(cpu_attribute):
    @hierarchyValidation(cpu_attribute)
    def __init__(self, *args, **kwargs):
        super(platform_id, self).__init__(*args, **kwargs)
