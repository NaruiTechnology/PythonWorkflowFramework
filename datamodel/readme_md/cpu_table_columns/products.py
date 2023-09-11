
from buildingblocks.decorators import hierarchyValidation
from datamodel.readme_md.cpu_attribute import cpu_attribute


class products(cpu_attribute):
    @hierarchyValidation(cpu_attribute)
    def __init__(self, *args, **kwargs):
        super(products, self).__init__(*args, **kwargs)
