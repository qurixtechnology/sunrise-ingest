create table person (
 id uniqueIdentifier default (newId()) primary key,
 firstName varchar(128) not null,
 lastName varchar(128) not null)
