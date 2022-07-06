from common.utils.datatable import DataColumn, DataTable

STAGE_LINKEDIN_FOLLOWERS = DataTable(
    schema="[SOURCE]",
    name="LINKEDIN_FOLLOWERS",
    columns=[
        DataColumn(
            name="PROFILE_LINK",
            source_name="profileLink",
            type="VARCHAR(250)",
            slowly_changing_dimension=True,
        ),
        DataColumn(
            name="FIRST_NAME",
            source_name="firstName",
            type="NVARCHAR(100)",
            slowly_changing_dimension=True,
        ),
        DataColumn(
            name="LAST_NAME",
            source_name="lastName",
            type="NVARCHAR(100)",
            slowly_changing_dimension=True,
        ),
        DataColumn(
            name="OCCUPATION",
            source_name="occupation",
            type="NVARCHAR(MAX)",
        ),
        DataColumn(
            name="FOLLOWERS",
            source_name="followers",
            type="INT",
        ),
        DataColumn(
            name="EXTRACTION_TS",
            type="DATETIME",
            imported=False,
        ),
        DataColumn(
            name="INSERTION_TS",
            type="DATETIME",
            imported=False,
            default_value="GETDATE()",
        ),
    ],
)

ROW_STAGE_LINKEDIN_FOLLOWERS = STAGE_LINKEDIN_FOLLOWERS.row_dataclass
