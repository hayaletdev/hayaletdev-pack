import ui


class DailyQuestItem(ui.ListBoxEx.Item):
	def __init__(self, title_text, progress_text, detail_text, is_completed):
		ui.ListBoxEx.Item.__init__(self)

		self.titleText = self.__CreateTextLine(8, 2, title_text)
		self.progressText = self.__CreateTextLine(8, 18, progress_text, 0.82, 0.82, 0.82)
		self.detailText = self.__CreateTextLine(8, 32, detail_text, 0.67, 0.88, 1.0)

		if is_completed:
			self.titleText.SetFontColor(0.5, 1.0, 0.5)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

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

		self.hasData = 0
		self.targetMobVnum = 0
		self.targetCount = 0
		self.progressCount = 0
		self.rewardVnum = 0
		self.rewardCount = 0
		self.isClaimed = 0

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
		self.openQuestButton.SetEvent(ui.__mem_func__(self.Close))
		self.openQuestButton.SetText("Kapat")
		self.refreshButton.SetEvent(ui.__mem_func__(self.RefreshQuestList))

		self.questListBox = ui.ListBoxEx()
		self.questListBox.SetParent(self)
		self.questListBox.SetPosition(self.LIST_X, self.LIST_Y)
		self.questListBox.SetItemSize(self.LIST_ITEM_WIDTH, self.LIST_ITEM_HEIGHT)
		self.questListBox.SetItemStep(self.LIST_ITEM_STEP)
		self.questListBox.SetViewItemCount(self.LIST_VIEW_COUNT)
		self.questListBox.SetScrollBar(self.scrollBar)
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
		return

	def OnQuestDelete(self, quest_type, quest_index):
		return

	def SetDailyQuestData(self, mob_vnum, target_count, progress_count, reward_vnum, reward_count, is_claimed):
		self.hasData = 1
		self.targetMobVnum = int(mob_vnum)
		self.targetCount = max(0, int(target_count))
		self.progressCount = max(0, int(progress_count))
		self.rewardVnum = int(reward_vnum)
		self.rewardCount = max(1, int(reward_count))
		self.isClaimed = int(is_claimed)

		if self.progressCount > self.targetCount:
			self.progressCount = self.targetCount

		if self.IsShow():
			self.RefreshQuestList()

	def RefreshQuestList(self):
		if not self.questListBox:
			return

		self.questListBox.RemoveAllItems()

		if not self.hasData:
			self.infoText.SetText("Active Daily Quests: 0")
			self.helpText.SetText("Gunluk gorev verisi bekleniyor...")
			return

		state_text = "Devam ediyor"
		if self.isClaimed == 1:
			state_text = "Odul verildi"
		elif self.progressCount >= self.targetCount:
			state_text = "Tamamlandi"

		item = DailyQuestItem(
			"Hedef Canavar VNUM: %d" % self.targetMobVnum,
			"Ilerleme: %d / %d" % (self.progressCount, self.targetCount),
			"Odul: %d x%d | Durum: %s" % (self.rewardVnum, self.rewardCount, state_text),
			self.isClaimed == 1
		)
		self.questListBox.AppendItem(item)

		self.infoText.SetText("Active Daily Quests: 1")
		self.helpText.SetText("Hedefi tamamla. Odul otomatik verilir.")
