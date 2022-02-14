USE [PersonDatabase]
go

drop table if exists [dbo].[Demographics];
go

CREATE TABLE [dbo].[Demographics]
(
	[IdKey] int identity(1,1)  not null,
	[ProviderGroup]	varchar(100) not null,
	[DateOnFile] date not null,
	[Id] int not null,
	[FirstName] nvarchar(100)  not null, 
	[MiddleName] nchar(100) null, 
	[LastName] nvarchar(100) null, 
	[DOB] date  not null,
	[Sex] char(1)  not null,
	[FavoriteColor]	nvarchar(100)  not null,
	CONSTRAINT [pk_dbo_Demographics_IdKey] PRIMARY KEY CLUSTERED ([IdKey])
)  

-- Index the secondary key
CREATE NONCLUSTERED INDEX [ix_dbo_Demographics_Id] on [dbo].[Demographics] ([Id])



drop table if exists [dbo].[Quarters];
go

CREATE TABLE [dbo].[Quarters]
(
	[IdKey]		 int identity(1,1)  not null,
	[DateOnFile] date null, -- NOT NULL
	[Id]		 int not null,
	[Quarter]    varchar(100)  not null, -- NOT NULL
	[Attributed] varchar(100) not null, 
	[Risk]		 float not null, 

	CONSTRAINT [pk_dbo_Quarters_IdKey] PRIMARY KEY CLUSTERED ([IdKey])
)  

-- Index the secondary key
CREATE NONCLUSTERED INDEX [ix_dbo_Quarters_Id] on [dbo].[Quarters] ([Id])




