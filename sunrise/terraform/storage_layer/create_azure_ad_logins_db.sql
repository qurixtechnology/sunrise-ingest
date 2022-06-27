-- Create Azure AD users: needed after deployment with Terraform
CREATE USER [fernando.zepeda@qurix.tech] FROM EXTERNAL PROVIDER;

-- Grant roles
ALTER ROLE db_datareader ADD MEMBER [fernando.zepeda@qurix.tech]; 
ALTER ROLE db_datawriter ADD MEMBER [fernando.zepeda@qurix.tech]; 
ALTER ROLE db_ddladmin ADD MEMBER [fernando.zepeda@qurix.tech]; 

--Grant Database Permissions
GRANT VIEW DATABASE STATE TO [fernando.zepeda@qurix.tech]

-- Add Server Role to admin
ALTER SERVER ROLE [sysadmin] ADD MEMBER [konkevych@qurix.tech];