USE [YapoDB]
GO

/****** Object:  Table [dbo].[Autos]    Script Date: 21-02-2022 14:35:07 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Autos](
	[yapo_id] [int] NOT NULL,
	[href] [nvarchar](512) NULL,
	[brand] [nvarchar](512) NULL,
	[year] [bigint] NULL,
	[km] [bigint] NULL,
	[tx] [nvarchar](50) NULL,
 CONSTRAINT [PK_Autos] PRIMARY KEY CLUSTERED 
(
	[yapo_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

