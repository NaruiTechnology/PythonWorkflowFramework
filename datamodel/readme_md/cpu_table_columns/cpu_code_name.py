from buildingblocks.decorators import hierarchyValidation
from datamodel.readme_md.cpu_attribute import cpu_attribute


class cpu_code_name(cpu_attribute):
    @hierarchyValidation(cpu_attribute)
    def __init__(self, *args, **kwargs):
        super(cpu_code_name, self).__init__(*args, **kwargs)
