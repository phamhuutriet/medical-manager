from ..core.enums import *


def is_valid_template_column_type(template_column: dict):
    template_column_types = {member.value for member in TemplateColumnType}
    return all(column_type in template_column_types for column_type in template_column.values())