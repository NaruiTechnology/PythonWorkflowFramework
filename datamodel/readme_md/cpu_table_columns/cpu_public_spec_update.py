from buildingblocks.decorators import hierarchyValidation
from datamodel.readme_md.cpu_attribute import cpu_attribute


class cpu_public_spec_update(cpu_attribute):
    @hierarchyValidation(cpu_attribute)
    def __init__(self, *args, **kwargs):
        super(cpu_public_spec_update, self).__init__(*args, **kwargs)
