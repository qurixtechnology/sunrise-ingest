/*
    Name: Sales Navigator
    Description: Sink table for ingestion of sales information
    Source: Linkedin via Phantom Buster
*/
CREATE TABLE [SOURCE].[SALES_NAVIGATOR] (
    PROFILE_LINK VARCHAR(250), -- unique?
    FULL_NAME VARCHAR(250),
    FIRST_NAME VARCHAR(100),
    LAST_NAME VARCHAR(100),
    IMG_URL VARCHAR(100),
    DEGREE INT,
    TITLE VARCHAR(100),
    COMPANY_NAME VARCHAR(200),
    COMPANY_URL VARCHAR(200),
    REGULAR_COMPANY_URL VARCHAR(MAX),
    [LOCATION] VARCHAR(200),
    NOTE VARCHAR(MAX),
    DATE_ADDED DATETIME,
    VM_ID VARCHAR(100),
    LINKEDIN_PROFILE_URL VARCHAR(200),
    [NAME] VARCHAR(200),
    LINKEDIN_QUERY VARCHAR(MAX),
    INTERNAL_LINKEDIN_TS DATETIME,
    EXTRACTION_TS DATETIME,
    INSERTION_TS DATETIME DEFAULT GETDATE()
);
/*
"profileUrl": "https://www.linkedin.com/sales/people/ACwAAApjCN0BWfHC6NGC6AVQuC1sBdltcZw0ydA,NAME_SEARCH,x6ZR",
        "fullName": "Niki Slawinski",
        "firstName": "Niki",
        "lastName": "Slawinski",
        "imgUrl": "https://media-exp1.licdn.com/dms/image/C5603AQG_ZDGsVlyV6g/profile-displayphoto-shrink_800_800/0/1593128100374?e=1638403200&v=beta&t=0grV81Wj3c3NIfG_nrcetdPvG62Q9awPx7KnOs7RU_w",
        "degree": 1,
        "title": "Senior Brand Consultant | Project Direction",
        "companyName": "DIE NEUE VERNUNFT GmbH",
        "companyUrl": "https://www.linkedin.com/sales/company/13039779",
        "regularCompanyUrl": "https://www.linkedin.com/company/13039779",
        "location": "Hamburg, Hamburg, Deutschland",
        "note": "",
        "dateAdded": "2021-08-15T10:54:47.007Z",
        "vmid": "ACwAAApjCN0BWfHC6NGC6AVQuC1sBdltcZw0ydA",
        "linkedInProfileUrl": "https://www.linkedin.com/in/ACwAAApjCN0BWfHC6NGC6AVQuC1sBdltcZw0ydA/",
        "name": "Niki Slawinski",
        "query": "https://www.linkedin.com/sales/lists/people/6832625598850969600?sortCriteria=OUTREACH_ACTIVITY&sortOrder=DESCENDING",
        "timestamp": "2021-10-02T10:16:54.996Z"
*/
