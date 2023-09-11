from buildingblocks.decorators import hierarchyValidation
from datamodel.readme_md.cpu_attribute import cpu_attribute
from datamodel.definitions import CpuSegment


class cpu_segment(cpu_attribute):
    @hierarchyValidation(cpu_attribute)
    def __init__(self, *args, **kwargs):
        super(cpu_segment, self).__init__(*args, **kwargs)
        segments = [e.value for e in CpuSegment]
        for i in range(0, len(segments)):
            self.__dict__[i] = segments[i]

