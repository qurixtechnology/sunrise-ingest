-- Creates the login AbolrousHazem with password '340$Uuxwp7Mcxo7Khy'.
CREATE LOGIN SUNRISE_SQL_INGEST_MANAGER
    WITH PASSWORD = 'qurixingestManager22!';
GO
-- Creates a database user for the login created above.
USE DEV_SUNRISE_DB;
CREATE USER SUNRISE_SQL_INGEST_MANAGER FOR LOGIN SUNRISE_SQL_INGEST_MANAGER with default_schema = SOURCE;
ALTER ROLE db_owner add member unittest;
GO
