USE [YapoDB]
GO

/****** Object:  Table [dbo].[AutoSamples]    Script Date: 21-02-2022 14:35:14 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[AutoSamples](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[yapo_id] [int] NOT NULL,
	[price] [bigint] NOT NULL,
	[sample_date] [date] NOT NULL,
 CONSTRAINT [PK_AutoSamples] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[AutoSamples]  WITH CHECK ADD  CONSTRAINT [FK_AutoSamples_Autos] FOREIGN KEY([yapo_id])
REFERENCES [dbo].[Autos] ([yapo_id])
GO

ALTER TABLE [dbo].[AutoSamples] CHECK CONSTRAINT [FK_AutoSamples_Autos]
GO

