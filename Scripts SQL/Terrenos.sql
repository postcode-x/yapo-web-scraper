USE [YapoDB]
GO

/****** Object:  Table [dbo].[Terrenos]    Script Date: 21-02-2022 14:35:28 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Terrenos](
	[yapo_id] [int] NOT NULL,
	[href] [nvarchar](512) NULL,
	[title] [nvarchar](512) NULL,
	[measurements] [bigint] NULL,
	[unit] [nvarchar](16) NULL,
	[region] [nvarchar](50) NULL,
	[commune] [nvarchar](50) NULL,
 CONSTRAINT [PK_Terrenos] PRIMARY KEY CLUSTERED 
(
	[yapo_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

