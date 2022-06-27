/*
    Name: Linkedin Followers
    Description: Sink table for ingestion of Linkedin followers
    Source: Linkedin via Phantom Buster
*/
CREATE TABLE [SOURCE].[LINKEDIN_FOLLOWERS] (
    PROFILE_LINK VARCHAR(250),
    FIRST_NAME VARCHAR(100),
    LAST_NAME VARCHAR(100),
    OCCUPATION VARCHAR(250),
    FOLLOWERS INT,
    EXTRACTION_TS DATETIME,
    INSERTION_TS DATETIME DEFAULT GETDATE()
);