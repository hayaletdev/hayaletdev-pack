import app
import event
import localeInfo
import quest
import ui


class DailyQuestItem(ui.ListBoxEx.Item):
	def __init__(self, quest_index, quest_name, progress_text, remain_text, is_confirmed):
		ui.ListBoxEx.Item.__init__(self)

		self.quest_index = quest_index
		self.quest_name = quest_name
		self.progress_text = progress_text
		self.remain_text = remain_text
		self.is_confirmed = is_confirmed

		self.titleText = self.__CreateTextLine(8, 2, quest_name)
		self.progressText = self.__CreateTextLine(8, 18, progress_text, 0.82, 0.82, 0.82)
		self.remainText = self.__CreateTextLine(8, 32, remain_text, 0.67, 0.88, 1.0)

		if not is_confirmed:
			self.titleText.SetFontColor(1.0, 0.9, 0.45)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, width, height)

	def GetQuestIndex(self):
		return self.quest_index

	def __CreateTextLine(self, x, y, text, r = 1.0, g = 1.0, b = 1.0):
		text_line = ui.TextLine()
		text_line.SetParent(self)
		text_line.SetPosition(x, y)
		text_line.SetText(text)
		text_line.SetFontColor(r, g, b)
		text_line.Show()
		return text_line


class DailyQuestWindow(ui.ScriptWindow):
	LIST_X = 18
	LIST_Y = 95
	LIST_ITEM_WIDTH = 300
	LIST_ITEM_HEIGHT = 46
	LIST_ITEM_STEP = 48
	LIST_VIEW_COUNT = 5

	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0

		self.board = None
		self.scrollBar = None
		self.infoText = None
		self.helpText = None
		self.openQuestButton = None
		self.refreshButton = None
		self.questListBox = None

		self.selectedQuestIndex = 0
		self.lastUpdateTime = 0
		self.dailyQuestDict = {}

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/dailyquestwindow.py")

		self.board = self.GetChild("board")
		self.scrollBar = self.GetChild("ScrollBar")
		self.infoText = self.GetChild("QuestInfoText")
		self.helpText = self.GetChild("QuestHelpText")
		self.openQuestButton = self.GetChild("OpenQuestButton")
		self.refreshButton = self.GetChild("RefreshButton")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.openQuestButton.SetEvent(ui.__mem_func__(self.__OpenSelectedQuest))
		self.refreshButton.SetEvent(ui.__mem_func__(self.RefreshQuestList))

		self.questListBox = ui.ListBoxEx()
		self.questListBox.SetParent(self)
		self.questListBox.SetPosition(self.LIST_X, self.LIST_Y)
		self.questListBox.SetItemSize(self.LIST_ITEM_WIDTH, self.LIST_ITEM_HEIGHT)
		self.questListBox.SetItemStep(self.LIST_ITEM_STEP)
		self.questListBox.SetViewItemCount(self.LIST_VIEW_COUNT)
		self.questListBox.SetScrollBar(self.scrollBar)
		self.questListBox.SetSelectEvent(ui.__mem_func__(self.__OnSelectQuest))
		self.questListBox.Show()

		self.SetCenterPosition()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.board = None
		self.scrollBar = None
		self.infoText = None
		self.helpText = None
		self.openQuestButton = None
		self.refreshButton = None
		self.questListBox = None
		self.dailyQuestDict = {}
		self.interface = None

	def Open(self):
		self.RefreshQuestList()
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnQuestRefresh(self, quest_type, quest_index):
		if quest_type != quest.QUEST_TYPE_DAILY:
			return

		self.__SyncQuestData(quest_index)
		if self.IsShow():
			self.RefreshQuestList()

	def OnQuestDelete(self, quest_type, quest_index):
		if quest_type != quest.QUEST_TYPE_DAILY:
			return

		if quest_index in self.dailyQuestDict:
			del self.dailyQuestDict[quest_index]

		if self.selectedQuestIndex == quest_index:
			self.selectedQuestIndex = 0

		if self.IsShow():
			self.RefreshQuestList()

	def OnUpdate(self):
		if not self.IsShow():
			return

		current_time = app.GetGlobalTimeStamp()
		if current_time == self.lastUpdateTime:
			return

		self.lastUpdateTime = current_time
		self.RefreshQuestList()

	def RefreshQuestList(self):
		if not self.questListBox:
			return

		active_daily_quest_index_list = self.__CollectActiveDailyQuestIndices()
		for quest_index in active_daily_quest_index_list:
			self.__SyncQuestData(quest_index)

		for quest_index in self.dailyQuestDict.keys():
			if not quest_index in active_daily_quest_index_list:
				del self.dailyQuestDict[quest_index]

		self.questListBox.RemoveAllItems()

		sorted_entries = self.dailyQuestDict.items()
		sorted_entries.sort(key = lambda entry: entry[0])

		current_selected_index = self.selectedQuestIndex
		self.selectedQuestIndex = 0
		for quest_index, data in sorted_entries:
			progress_text = self.__FormatCounterText(data["counter_name"], data["counter_value"])
			remain_text = self.__FormatRemainText(data["clock_name"], data["clock_time"])

			item = DailyQuestItem(
				quest_index,
				data["name"],
				progress_text,
				remain_text,
				data["is_confirmed"]
			)
			self.questListBox.AppendItem(item)

			if current_selected_index == quest_index:
				self.questListBox.SelectItem(item)
				self.selectedQuestIndex = quest_index

		quest_count = len(sorted_entries)
		self.infoText.SetText("Active Daily Quests: %d" % quest_count)

		if quest_count == 0:
			self.helpText.SetText("No active daily quest. Re-login or wait for reset.")
		else:
			self.helpText.SetText("Select a quest and click Open Quest.")

	def __OnSelectQuest(self, item):
		if not item:
			self.selectedQuestIndex = 0
			return

		self.selectedQuestIndex = item.GetQuestIndex()

	def __OpenSelectedQuest(self):
		if self.selectedQuestIndex <= 0:
			return

		event.QuestButtonClick(-2147483648 + self.selectedQuestIndex)

	def __CollectActiveDailyQuestIndices(self):
		quest_index_list = []

		try:
			quest_count = quest.GetQuestCount()
		except:
			return quest_index_list

		for slot_index in xrange(quest_count):
			try:
				quest_index = quest.GetQuestIndex(slot_index)
			except:
				quest_index = slot_index

			if quest_index <= 0:
				continue

			try:
				quest_data = quest.GetQuestData(quest_index)
				if len(quest_data) >= 6 and quest_data[0] != quest.QUEST_TYPE_DAILY:
					continue
			except:
				continue

			quest_index_list.append(quest_index)

		return quest_index_list

	def __SyncQuestData(self, quest_index):
		try:
			quest_data = quest.GetQuestData(quest_index)

			if len(quest_data) >= 6:
				(quest_type, is_confirmed, quest_name, quest_icon, counter_name, counter_value) = quest_data
				if quest_type != quest.QUEST_TYPE_DAILY:
					if quest_index in self.dailyQuestDict:
						del self.dailyQuestDict[quest_index]
					return
			else:
				(quest_name, quest_icon, counter_name, counter_value) = quest_data
				is_confirmed = 1

			clock_name = ""
			clock_time = 0
			try:
				(clock_name, clock_time) = quest.GetQuestLastTime(quest_index)
			except:
				pass

			self.dailyQuestDict[quest_index] = {
				"name" : quest_name,
				"is_confirmed" : is_confirmed,
				"counter_name" : counter_name,
				"counter_value" : counter_value,
				"clock_name" : clock_name,
				"clock_time" : clock_time,
			}
		except:
			if quest_index in self.dailyQuestDict:
				del self.dailyQuestDict[quest_index]

	def __FormatCounterText(self, counter_name, counter_value):
		if len(counter_name) <= 0:
			return "Progress: -"
		return "%s: %d" % (counter_name, counter_value)

	def __FormatRemainText(self, clock_name, clock_time):
		if len(clock_name) <= 0:
			return localeInfo.QUEST_UNLIMITED_TIME

		if clock_time <= 0:
			return "%s: %s" % (clock_name, localeInfo.QUEST_TIMEOVER)

		return "%s: %s" % (clock_name, localeInfo.SecondToColonTypeHMS(clock_time))
