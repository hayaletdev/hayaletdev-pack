import uiScriptLocale

window = {
	"name" : "DailyQuestWindow",

	"x" : SCREEN_WIDTH - 420,
	"y" : SCREEN_HEIGHT - 520,

	"style" : ("movable", "float",),

	"width" : 360,
	"height" : 430,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 360,
			"height" : 430,
			"title" : uiScriptLocale.QUEST_UI_TEXT_DAILY,

			"children" :
			(
				{
					"name" : "QuestInfoText",
					"type" : "text",

					"x" : 18,
					"y" : 40,

					"text" : "Active Daily Quests: 0",
				},
				{
					"name" : "QuestHelpText",
					"type" : "text",

					"x" : 18,
					"y" : 60,

					"text" : "Select a quest and click Open Quest.",
					"r" : 0.75,
					"g" : 0.75,
					"b" : 0.75,
					"a" : 1.0,
				},
			),
		},

		{
			"name" : "ScrollBar",
			"type" : "scrollbar",

			"x" : 328,
			"y" : 95,
			"size" : 245,
		},

		{
			"name" : "OpenQuestButton",
			"type" : "button",

			"x" : 18,
			"y" : 395,

			"text" : "Open Quest",

			"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
		},
		{
			"name" : "RefreshButton",
			"type" : "button",

			"x" : 200,
			"y" : 395,

			"text" : "Refresh",

			"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
		},
	),
}
