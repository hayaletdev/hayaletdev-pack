import uiScriptLocale

WINDOW_WIDTH = 286
WINDOW_HEIGHT = 500

window = {
	"name" : "DailyQuestWindow",

	"x" : SCREEN_WIDTH - WINDOW_WIDTH - 70,
	"y" : SCREEN_HEIGHT - WINDOW_HEIGHT - 90,

	"style" : ("movable", "float",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			"title" : uiScriptLocale.QUEST_UI_TEXT_DAILY,

			"children" :
			(
				{
					"name" : "QuestInfoText",
					"type" : "text",

					"x" : 16,
					"y" : 36,
					"text" : "Gunluk gorev verisi bekleniyor...",
				},
				{
					"name" : "QuestHelpText",
					"type" : "text",

					"x" : 16,
					"y" : 54,
					"text" : "Gorev tamamlaninca odul otomatik gelir.",
					"r" : 0.75,
					"g" : 0.75,
					"b" : 0.75,
					"a" : 1.0,
				},
				{
					"name" : "MainPanel",
					"type" : "bar",

					"x" : 16,
					"y" : 78,
					"width" : 252,
					"height" : 364,

					"color" : 0xAA000000,

					"children" :
					(
						{
							"name" : "PreviewPanel",
							"type" : "bar",

							"x" : 10,
							"y" : 10,
							"width" : 232,
							"height" : 118,

							"color" : 0x55000000,

							"children" :
							(
								{
									"name" : "PreviewTitle",
									"type" : "text",

									"x" : 10,
									"y" : 8,
									"text" : "Guncel Gorev Durumu",
								},
								{
									"name" : "PreviewDivider",
									"type" : "horizontalbar",

									"x" : 10,
									"y" : 26,
									"width" : 212,
								},
								{
									"name" : "MissionTargetLabel",
									"type" : "text",

									"x" : 10,
									"y" : 42,
									"text" : "Hedef",
									"r" : 0.75,
									"g" : 0.75,
									"b" : 0.75,
									"a" : 1.0,
								},
								{
									"name" : "MissionTargetValue",
									"type" : "text",

									"x" : 10,
									"y" : 60,
									"text" : "-",
									"r" : 0.67,
									"g" : 0.88,
									"b" : 1.0,
									"a" : 1.0,
								},
								{
									"name" : "MissionStateLabel",
									"type" : "text",

									"x" : 10,
									"y" : 84,
									"text" : "Durum",
									"r" : 0.75,
									"g" : 0.75,
									"b" : 0.75,
									"a" : 1.0,
								},
								{
									"name" : "MissionStateValue",
									"type" : "text",

									"x" : 58,
									"y" : 84,
									"text" : "-",
									"r" : 1.0,
									"g" : 0.90,
									"b" : 0.45,
									"a" : 1.0,
								},
							),
						},
						{
							"name" : "MissionProgressLabel",
							"type" : "text",

							"x" : 12,
							"y" : 136,
							"text" : "Ilerleme",
							"r" : 0.75,
							"g" : 0.75,
							"b" : 0.75,
							"a" : 1.0,
						},
						{
							"name" : "MissionProgressGauge",
							"type" : "gauge",

							"x" : 12,
							"y" : 154,
							"width" : 228,
							"color" : "red",
						},
						{
							"name" : "MissionProgressValue",
							"type" : "text",

							"x" : 12,
							"y" : 172,
							"text" : "0 / 0",
						},
						{
							"name" : "MissionRemainValue",
							"type" : "text",

							"x" : 12,
							"y" : 190,
							"text" : "Kalan: 0",
							"r" : 0.67,
							"g" : 0.88,
							"b" : 1.0,
							"a" : 1.0,
						},
						{
							"name" : "RewardTitle",
							"type" : "text",

							"x" : 12,
							"y" : 226,
							"text" : "Sabit Oduller",
						},
						{
							"name" : "RewardDivider",
							"type" : "horizontalbar",

							"x" : 12,
							"y" : 244,
							"width" : 228,
						},
						{
							"name" : "RewardSlot",
							"type" : "slot",

							"x" : 12,
							"y" : 258,
							"width" : 96,
							"height" : 96,

							"image" : "d:/ymir work/ui/public/Slot_Base.sub",

							"slot" :
							(
								{"index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32},
								{"index" : 1, "x" : 32, "y" : 0, "width" : 32, "height" : 32},
								{"index" : 2, "x" : 64, "y" : 0, "width" : 32, "height" : 32},
								{"index" : 3, "x" : 0, "y" : 32, "width" : 32, "height" : 32},
								{"index" : 4, "x" : 32, "y" : 32, "width" : 32, "height" : 32},
								{"index" : 5, "x" : 64, "y" : 32, "width" : 32, "height" : 32},
								{"index" : 6, "x" : 0, "y" : 64, "width" : 32, "height" : 32},
								{"index" : 7, "x" : 32, "y" : 64, "width" : 32, "height" : 32},
								{"index" : 8, "x" : 64, "y" : 64, "width" : 32, "height" : 32},
							),
						},
						{
							"name" : "RewardNameValue",
							"type" : "text",

							"x" : 118,
							"y" : 264,
							"text" : "Odul Yok",
						},
						{
							"name" : "RewardCountValue",
							"type" : "text",

							"x" : 118,
							"y" : 282,
							"text" : "x0",
							"r" : 0.67,
							"g" : 0.88,
							"b" : 1.0,
							"a" : 1.0,
						},
						{
							"name" : "MissionResetText",
							"type" : "text",

							"x" : 12,
							"y" : 332,
							"text" : "Gunluk gorev, 24 saatte bir yenilenir.",
							"r" : 0.62,
							"g" : 0.62,
							"b" : 0.62,
							"a" : 1.0,
						},
					),
				},
				{
					"name" : "RandomRewardButton",
					"type" : "button",

					"x" : 16,
					"y" : 452,

					"text" : "Odul Listesi",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "OpenQuestButton",
					"type" : "button",

					"x" : 144,
					"y" : 452,

					"text" : "Kapat",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}
