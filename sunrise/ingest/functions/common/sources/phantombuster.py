from common.utils.source import PhantomBusterSource
from configs.phantom_buster import PhantomsAgent, PhantomStorageFolder


LINKEDIN_FOLLOWERS_SOURCE = PhantomBusterSource(
    name="linkedin_followers",
    agent=PhantomsAgent.LINKEDIN_FOLLOWERS.value,
    storage=PhantomStorageFolder.LINKEDIN_FOLLOWERS.value,
)


SALES_NAVIGATOR_SOURCE = PhantomBusterSource(
    name="sales_navigator",
    agent=PhantomsAgent.SALES_NAVIGATOR.value,
    storage=PhantomStorageFolder.SALES_NAVIGATOR.value,
)

COMPANY_FOLLOWERS_SOURCE = PhantomBusterSource(
    name="linkedin_company_followers",
    agent=PhantomsAgent.LINKEDIN_COMPANY_FOLLOWERS.value,
    storage=PhantomStorageFolder.LINKEDIN_COMPANY_FOLLOWERS.value,
)
