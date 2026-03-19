import uiScriptLocale

WINDOW_WIDTH = 470
WINDOW_HEIGHT = 420

window = {
	"name" : "DailyQuestWindow",

	"x" : SCREEN_WIDTH - WINDOW_WIDTH - 80,
	"y" : SCREEN_HEIGHT - WINDOW_HEIGHT - 120,

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
					"name" : "TopBar",
					"type" : "horizontalbar",

					"x" : 12,
					"y" : 34,
					"width" : WINDOW_WIDTH - 24,
				},
				{
					"name" : "QuestInfoText",
					"type" : "text",

					"x" : 18,
					"y" : 40,
					"text" : "Gunluk gorev verisi bekleniyor...",
				},
				{
					"name" : "QuestHelpText",
					"type" : "text",

					"x" : 18,
					"y" : 58,
					"text" : "Her gun yenilenir, gorevi bitirince odul otomatik gelir.",
					"r" : 0.75,
					"g" : 0.75,
					"b" : 0.75,
					"a" : 1.0,
				},
				{
					"name" : "MissionPanel",
					"type" : "bar",

					"x" : 16,
					"y" : 84,
					"width" : 212,
					"height" : 270,

					"color" : 0xAA000000,

					"children" :
					(
						{
							"name" : "MissionTitle",
							"type" : "text",

							"x" : 10,
							"y" : 10,
							"text" : "Guncel Gorev Durumu",
						},
						{
							"name" : "MissionDivider",
							"type" : "horizontalbar",

							"x" : 10,
							"y" : 30,
							"width" : 192,
						},
						{
							"name" : "MissionTargetLabel",
							"type" : "text",

							"x" : 10,
							"y" : 44,
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
							"y" : 62,
							"text" : "-",
							"r" : 0.67,
							"g" : 0.88,
							"b" : 1.0,
							"a" : 1.0,
						},
						{
							"name" : "MissionProgressLabel",
							"type" : "text",

							"x" : 10,
							"y" : 92,
							"text" : "Ilerleme",
							"r" : 0.75,
							"g" : 0.75,
							"b" : 0.75,
							"a" : 1.0,
						},
						{
							"name" : "MissionProgressGauge",
							"type" : "gauge",

							"x" : 10,
							"y" : 110,
							"width" : 190,
							"color" : "red",
						},
						{
							"name" : "MissionProgressValue",
							"type" : "text",

							"x" : 10,
							"y" : 126,
							"text" : "0 / 0",
						},
						{
							"name" : "MissionStateLabel",
							"type" : "text",

							"x" : 10,
							"y" : 158,
							"text" : "Durum",
							"r" : 0.75,
							"g" : 0.75,
							"b" : 0.75,
							"a" : 1.0,
						},
						{
							"name" : "MissionStateValue",
							"type" : "text",

							"x" : 10,
							"y" : 176,
							"text" : "-",
							"r" : 1.0,
							"g" : 0.90,
							"b" : 0.45,
							"a" : 1.0,
						},
						{
							"name" : "MissionResetText",
							"type" : "text",

							"x" : 10,
							"y" : 232,
							"text" : "Gunluk gorevler 24 saatte bir yenilenir.",
							"r" : 0.62,
							"g" : 0.62,
							"b" : 0.62,
							"a" : 1.0,
						},
					),
				},
				{
					"name" : "RewardPanel",
					"type" : "bar",

					"x" : 242,
					"y" : 84,
					"width" : 212,
					"height" : 270,

					"color" : 0xAA000000,

					"children" :
					(
						{
							"name" : "RewardTitle",
							"type" : "text",

							"x" : 10,
							"y" : 10,
							"text" : "Sabit Oduller",
						},
						{
							"name" : "RewardDivider",
							"type" : "horizontalbar",

							"x" : 10,
							"y" : 30,
							"width" : 192,
						},
						{
							"name" : "RewardSlot",
							"type" : "slot",

							"x" : 10,
							"y" : 48,
							"width" : 32,
							"height" : 32,

							"image" : "d:/ymir work/ui/public/Slot_Base.sub",

							"slot" :
							(
								{"index" : 0, "x" : 0, "y" : 0, "width" : 32, "height" : 32},
							),
						},
						{
							"name" : "RewardNameValue",
							"type" : "text",

							"x" : 50,
							"y" : 52,
							"text" : "Odul Yok",
						},
						{
							"name" : "RewardCountValue",
							"type" : "text",

							"x" : 50,
							"y" : 68,
							"text" : "x0",
							"r" : 0.67,
							"g" : 0.88,
							"b" : 1.0,
							"a" : 1.0,
						},
						{
							"name" : "RewardInfoText1",
							"type" : "text",

							"x" : 10,
							"y" : 114,
							"text" : "Gorevi tamamladiginda odul otomatik verilir.",
							"r" : 0.75,
							"g" : 0.75,
							"b" : 0.75,
							"a" : 1.0,
						},
						{
							"name" : "RewardInfoText2",
							"type" : "text",

							"x" : 10,
							"y" : 132,
							"text" : "Envanter doluysa odul bir sonraki oldurmede",
							"r" : 0.75,
							"g" : 0.75,
							"b" : 0.75,
							"a" : 1.0,
						},
						{
							"name" : "RewardInfoText3",
							"type" : "text",

							"x" : 10,
							"y" : 148,
							"text" : "tekrar kontrol edilir.",
							"r" : 0.75,
							"g" : 0.75,
							"b" : 0.75,
							"a" : 1.0,
						},
					),
				},
				{
					"name" : "OpenQuestButton",
					"type" : "button",

					"x" : 16,
					"y" : 364,

					"text" : "Kapat",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "RefreshButton",
					"type" : "button",

					"x" : 242,
					"y" : 364,

					"text" : "Yenile",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}
