USE [YapoDB]
GO

/****** Object:  Table [dbo].[TerrenoSamples]    Script Date: 21-02-2022 14:35:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[TerrenoSamples](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[yapo_id] [int] NOT NULL,
	[price] [bigint] NOT NULL,
	[unit] [nvarchar](50) NOT NULL,
	[sample_date] [date] NOT NULL,
 CONSTRAINT [PK_TerrenoSamples] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[TerrenoSamples]  WITH CHECK ADD  CONSTRAINT [FK_TerrenoSamples_Terrenos] FOREIGN KEY([yapo_id])
REFERENCES [dbo].[Terrenos] ([yapo_id])
GO

ALTER TABLE [dbo].[TerrenoSamples] CHECK CONSTRAINT [FK_TerrenoSamples_Terrenos]
GO

