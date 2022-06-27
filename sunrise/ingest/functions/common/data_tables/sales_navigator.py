from common.utils.datatable import DataColumn, DataTable


STAGE_SALES_NAVIGATOR = DataTable(
    schema="[SOURCE]",
    name="SALES_NAVIGATOR",
    columns=[
        DataColumn(
            name="PROFILE_LINK",
            source_name="profileUrl",
            type="VARCHAR(250)",
        ),
        DataColumn(
            name="FULL_NAME",
            source_name="fullName",
            type="VARCHAR(250)",
        ),
        DataColumn(
            name="FIRST_NAME",
            source_name="firstName",
            type="VARCHAR(100)",
        ),
        DataColumn(
            name="LAST_NAME",
            source_name="lastName",
            type="VARCHAR(100)",
        ),
        DataColumn(
            name="IMG_URL",
            source_name="imgUrl",
            type="VARCHAR(MAX)",
        ),
        DataColumn(
            name="DEGREE",
            source_name="degree",
            type="INT",
        ),
        DataColumn(
            name="TITLE",
            source_name="title",
            type="VARCHAR(150)",
        ),
        DataColumn(
            name="COMPANY_NAME",
            source_name="companyName",
            type="VARCHAR(200)",
        ),
        DataColumn(
            name="COMPANY_URL",
            source_name="companyUrl",
            type="VARCHAR(200)",
        ),
        DataColumn(
            name="REGULAR_COMPANY_URL",
            source_name="regularCompanyUrl",
            type="VARCHAR(MAX)",
        ),
        DataColumn(
            name="[LOCATION]",
            source_name="location",
            type="VARCHAR(100)",
        ),
        DataColumn(
            name="NOTE",
            source_name="note",
            type="VARCHAR(100)",
        ),
        DataColumn(
            name="DATE_ADDED",
            source_name="dateAdded",
            type="DATETIME",
        ),
        DataColumn(
            name="VM_ID",
            source_name="vmid",
            type="VARCHAR(100)",
        ),
        DataColumn(
            name="LINKEDIN_PROFILE_URL",
            source_name="linkedInProfileUrl",
            type="VARCHAR(200)",
        ),
        DataColumn(
            name="[NAME]",
            source_name="[name]",
            type="VARCHAR(100)",
        ),
        DataColumn(
            name="LINKEDIN_QUERY",
            source_name="query",
            type="VARCHAR(200)",
        ),
        DataColumn(
            name="INTERNAL_LINKEDIN_TS",
            source_name="timestamp",
            type="DATETIME",
        ),
        DataColumn(
            name="INSERTION_TS",
            type="DATETIME",
            imported=False,
            default_value="GETDATE()",
        ),
    ],
)

ROW_STAGE_SALES_NAVIGATOR = STAGE_SALES_NAVIGATOR.row_dataclass
