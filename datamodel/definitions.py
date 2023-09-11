#-------------------------------------------------------------------------------
# This file contains 'Framework Code' and is licensed as such
# under the terms of your license agreement with Intel or your
# vendor. This file may not be modified, except as allowed by
# additional terms of your license agreement.
#
## @file
#
# Copyright (c) 2019, Intel Corporation. All rights reserved.
# This software and associated documentation (if any) is furnished
# under a license and may only be used or copied in accordance
# with the terms of the license. Except as permitted by such
# license, no part of this software or documentation may be
# reproduced, stored in a retrieval system, or transmitted in any
# form or by any means without the express written consent of
# Intel Corporation.
#-------------- -----------------------------------------------------------------
from enum import Enum


class CpuTableColumn(Enum):
    def __str__(self):
        return self.value
    cpu_segment = 'cpu_segment'
    mcu_file_name = 'mcu_file_name'
    cpu_code_name = 'cpu_code_name'
    cpu_core_stepping = 'cpu_core_stepping'
    platform_id = 'platform_id'
    cpu_id = 'cpu_id'
    cpu_public_spec_update = 'cpu_public_spec_update'
    intel_product_spec = 'intel_product_spec'
    cpu_nda_spec_update = 'cpu_nda_spec_update'
    processor_model = 'processor_model'
    products = 'products'

class CpuSegment(Enum):
    def __str__(self):
        return self.value
    DESKTOP = 'Desktop'
    SERVER = 'Server'
    MOBILE = 'Mobile'
    SOC = 'SOC'


class ReleaseTarget(Enum):
    def __str__(self):
        return self.value
    DEBUG = 'debug'
    PRODUCTION = 'production'
    PRODUCTION_CANDIDATE = 'production candidate'
    ALPHA = 'alpha'
    BETA = 'beta'


class ReadmeTableColumn(Enum):
    def __str__(self):
        return self.value
    CPUSegment = 0
    McuFileName = 1
    CPUCodeName = 2
    CPUCoreStepping = 3
    PlatformID = 4
    CPUID = 5


class TransactionStatus(Enum):
    def __str__(self):
        return self.value
    IDLE = 'Idle'
    PROGRESS = 'Progress'
    FAILED = 'Failed'
    ABORTED = 'Aborted'
    COMPLETED = 'Completed'


class Environment(Enum):
    def __str__(self):
        return self.value
    PRODUCTION = 'Production'
    TESTING = 'Testing'


class DataSource(Enum):
    def __str__(self):
        return self.value
    HSD = 'HSD'
    LOCAL = 'Local'


class TaskFrequecy(Enum):
    def __str__(self):
        return self.value
    MONTHLY = 'Monthly'
    DAILY = 'Daily'
    HOURLY = 'Hourly'


class Consts:
    PROPERTY_CHANGED = 'PropertyChanged'
    CONFIG_CHANGED = 'ConfigChanged'
    JSON_WORK_SHEET = 'McuRelease.json'
    USER_NAME = '%USER_NAME%'
    PASSWORD = '%PASSWORD%'
    RELEASE_TO = '%RELEASE_TO%'
    DEV_ROOT = '%DEV_ROOT%'
    WORK_SHEET = '%WORK_SHEET%'
    MCU = 'Mcu'
    MCUS = 'Mcus'
    STATES = 'States'
    STATUS = 'status'
    MCU_FILE_PREFIX_PATTERN = '(m|M|mu)'
    PARAMETERS = 'parameters'
    SETUP_PACKAGE = 'setup_state'
    PROCESSING_PACKAGE = 'processing_state'
    PUBLISH_PACKAGE = 'publish_state'
    CPU_CODE_NAME = 'CPUCodeName'
    STEPPING = 'Stepping'
    CPU_SEGMENT = 'CpuSegment'
    RELEASE_TARGET = 'ReleaseTarget'
    SANDBOX = '%SAND_BOX%'
    STAGING = '%STAGING%'
    SETUP_STATE_OBJ_PREFIX = 'setup_'
    PUBLISH_STATE_OBJ_PREFIX = 'publish_'
    PROCESSION_STATE_OBJ_PREFIX = 'processing_'
    HSD_STATE_OBJ_PREFIX = 'hsd_'
    STATE_OBJ_SUFFIX = '_state'
    STATE_DATA = 'stateData'
    SKIP = 'skip'
    CRTOOLS = '%CRTOOLS%'
    TRANSCTION_COMPLETE = 'transactionComplete'
    GUID = 'GUID'
    UNANNOUNCED = 'Unannounced'
    TAG = '%TAG%'
    PREVIOUS_TAG = '%PREVIOUS_TAG%'
    REPO_NAME = '%REPO_NAME%'
    SCOPE = '%SCOPE%'
    GITHUB_TOKEN = '%GITHUB_TOKEN%'
    GIT_EXPORT_INI = '%GIT_EXPORT_INI%'
    COMPLETED_MSG = '--- Completed ---'
    FAILED_MSG = '--- Failed ---'
    GUID_STRING = '%GUID_STRING%'
    PACKAGE_PATH_TEMPLATE = '%SAND_BOX%/microcode_release-sandbox/%SCOPE%/%RELEASE_TO%'
    REGEX_GUILD_PATTERN = '(\{){0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}(\}){0,1}'
    REGEX_GIT_STATUS_STAGED_PATTERN = r'^(((new file:)|(modified:)|(deleted:)\\s+).*((.py)|(.json)|(.ini)|(.md)|(.MD)|(.INF)|(.inc)|(.INC))$'
    REGEX_GIT_STATUS_NEW_PATTERN = '(new file:)\s+.*((.py)|(.json)|(.ini)|(.md)|(.MD)|(.INF)|(.inf)|(.inc)|(.INC))'
    REGEX_GIT_STATUS_MODIFIED_PATTERN = '(modified:)\s+.*((.py)|(.json)|(.ini)|(.md)|(.MD)|(.INF)|(.inf)|(.inc)|(.INC))'
    REGEX_GIT_STATUS_DELETED_PATTERN = '(deleted:)\s+.*((.py)|(.json)|(.ini)|(.md)|(.MD)|(.INF)|(.inf)|(.inc)|(.INC))'
    REGEX_GIT_STATUS_REPLACE_PATTERN = '((\t)?(new file:)|(modified:)\s+)'
    INC_FILE_PATTERNS = '^(m|M|mu).*([a-f0-9]{3}).inc$'
    MCU_PATTERNS = '(((m([a-f0-9]{7})_([a-f0-9]{8})))|(m_([a-f0-9]{2})_([a-f0-9]{5})_([a-f0-9]{8}))' \
                   '|(m_([0-9]{2})([a-f0-9]{5})([a-f0-9]{5})([a-f0-9]{8}))|(m([a-f0-9]{7})([a-f0-9]{3}))' \
                   '|(m([a-f0-9]{7}))|(M([A-Z0-9]{10}))|(m([a-f0-9]{7})([a-f0-9]{8})([a-f0-9]{8}))' \
                   '|(m([a-f0-9]{10}))|(m([a-f0-9]{10})([a-f0-9]{2}))' \
                   '|(mu([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{8})([a-f0-9]{8}))|(mu([a-f0-9]{6}))' \
                   '|(m_([a-f0-9]{2}_([a-f0-9]{5}))_([a-f0-9]{5})_([a-f0-9]{8}))' \
                   '|(m([a-f0-9]{7})_([a-f0-9]{3}))|(m([a-f0-9]{7}_([a-f0-9]{8})_([a-f0-9]{8})))' \
                   '|(m([a-f0-9]{6})))'
    MCU_TABLE_ROW_PATTERN = '^\|(((\s+)?Desktop(\s+)?)|((\s+)?SOC(\s+)?)|((\s+)?Mobile(\s+)?)' \
                            '|((\s+)?Server(\s+)?))\|(\s+)?(((m|M|mu)[A-Fa-f0-9]+)?((m|M|mu)' \
                            '\\_[A-Fa-f0-9]+\\_[A-Fa-f0-9]+)?((m|M|mu)\\_[0-9]+\\_[0-9]+\\_' \
                            '[A-Fa-f0-9]+)?)(\s+)?\|(\s+)?([A-Za-z]+.\s+(\()?[A-Za-z0-9-\/\(\).\s+]+)?([A-Za-z0-9,' \
                            '\s+-.\(\)\/]+)?(\s+)?\|(\s+([A-Z]{1}-[A-Z0-9]{1})?\s+?)\|(\s+)?[A-Fa-f0-9]+(\s+)?\|' \
                            '(\s+)?[A-Fa-f0-9]{8}\s+\|.*\|.*$'
    MCU_TIME_STAMP_FORMAT = '%Y%m%d'
    USER_NAME = '%USER_NAME%'
    START_COMMIT_HASH = '%START_COMMIT_HASH%'
    END_COMMIT_HASH = '%END_COMMIT_HASH%'
    START_COMMIT_TAG = '%START_COMMIT_TAG%'
    END_COMMIT_TAG = '%END_COMMIT_TAG%'
    MANIFEST_EDIT_TEMPLATE = '| Unannounced | N/A |'
    MAJOR_RELEASE_TO_CUSTOMMERS = ['Apple_only',
                                   'AWS_only',
                                   'CNL_U_GT0',
                                   'Dell_only',
                                   'Google_only',
                                   'HP_inc_only',
                                   'HPE_only',
                                   'Lakefield',
                                   'LCFC_only',
                                   'Lenovo_only',
                                   'Microsoft_only',
                                   'MSFT_OS_USE',
                                   'PRT_Chestnut_BDW_DE',
                                   'PRT_Chestnut_BDX',
                                   'PRT_Chestnut_HSX',
                                   'PRT0001',
                                   'PRT0002',
                                   'Samsung_only',
                                   'SKX_Amazon_only',
                                   'SKX_B1',
                                   'Supermicro_only',
                                   'LCFC_only',
                                   'AMI_only',
                                   'Insyde_only'
                                   ]

    README_MD_COLUMNS = ['CPU Segment',
                         'Microcode File Name',
                         'CPU Code Name',
                         'CPU Core Stepping',
                         'Platform ID',
                         'CPUID',
                         'CPU Public Spec Update',
                         'Intel Product Specs',
                         'CPU NDA Spec Update',
                         'Processor Model',
                         'Products']
