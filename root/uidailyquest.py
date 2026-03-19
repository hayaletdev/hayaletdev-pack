import item
import nonplayer
import player
import ui


class DailyQuestWindow(ui.ScriptWindow):
	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0
		self.itemToolTip = None

		self.board = None
		self.infoText = None
		self.helpText = None
		self.openQuestButton = None
		self.randomRewardButton = None

		self.targetValueText = None
		self.progressGauge = None
		self.progressValueText = None
		self.remainValueText = None
		self.stateValueText = None

		self.rewardSlot = None
		self.rewardNameText = None
		self.rewardCountText = None

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
		self.infoText = self.GetChild("QuestInfoText")
		self.helpText = self.GetChild("QuestHelpText")
		self.openQuestButton = self.GetChild("OpenQuestButton")
		self.randomRewardButton = self.GetChild("RandomRewardButton")

		self.targetValueText = self.GetChild("MissionTargetValue")
		self.progressGauge = self.GetChild("MissionProgressGauge")
		self.progressValueText = self.GetChild("MissionProgressValue")
		self.remainValueText = self.GetChild("MissionRemainValue")
		self.stateValueText = self.GetChild("MissionStateValue")

		self.rewardSlot = self.GetChild("RewardSlot")
		self.rewardNameText = self.GetChild("RewardNameValue")
		self.rewardCountText = self.GetChild("RewardCountValue")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.openQuestButton.SetEvent(ui.__mem_func__(self.Close))
		self.randomRewardButton.SetEvent(ui.__mem_func__(self.RefreshQuestList))

		if self.rewardSlot:
			self.rewardSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInRewardSlot))
			self.rewardSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutRewardSlot))

		self.SetCenterPosition()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()

		self.interface = None
		self.itemToolTip = None

		self.board = None
		self.infoText = None
		self.helpText = None
		self.openQuestButton = None
		self.randomRewardButton = None

		self.targetValueText = None
		self.progressGauge = None
		self.progressValueText = None
		self.remainValueText = None
		self.stateValueText = None

		self.rewardSlot = None
		self.rewardNameText = None
		self.rewardCountText = None

	def SetItemToolTip(self, tooltip):
		self.itemToolTip = tooltip

	def Open(self):
		self.RefreshQuestList()
		self.Show()
		self.SetTop()

	def Close(self):
		self.__OnOverOutRewardSlot()
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
		if not self.infoText:
			return

		if not self.hasData:
			self.infoText.SetText("Active Daily Quests: 0")
			self.helpText.SetText("Gunluk gorev verisi bekleniyor...")
			self.targetValueText.SetText("-")
			self.progressGauge.SetPercentage(0, 1)
			self.progressValueText.SetText("0 / 0")
			self.remainValueText.SetText("Kalan: 0")
			self.stateValueText.SetText("-")
			self.rewardNameText.SetText("Odul Yok")
			self.rewardCountText.SetText("x0")
			self.__RefreshRewardSlot(0, 0)
			return

		self.infoText.SetText("Active Daily Quests: 1")
		self.helpText.SetText("Gorev tamamlaninca odul otomatik teslim edilir.")

		self.targetValueText.SetText(self.__GetTargetNameText(self.targetMobVnum))
		self.progressGauge.SetPercentage(self.progressCount, max(1, self.targetCount))
		self.progressValueText.SetText("%d / %d" % (self.progressCount, self.targetCount))
		self.remainValueText.SetText("Kalan: %d" % max(0, self.targetCount - self.progressCount))

		state_text = "Devam ediyor"
		state_color = (1.0, 0.90, 0.45)
		if self.isClaimed == 1:
			state_text = "Odul verildi"
			state_color = (0.55, 1.0, 0.55)
		elif self.progressCount >= self.targetCount:
			state_text = "Tamamlandi"
			state_color = (0.67, 0.88, 1.0)

		self.stateValueText.SetText(state_text)
		self.stateValueText.SetFontColor(state_color[0], state_color[1], state_color[2])

		self.rewardNameText.SetText(self.__GetRewardNameText(self.rewardVnum))
		self.rewardCountText.SetText("x%d" % self.rewardCount)
		self.__RefreshRewardSlot(self.rewardVnum, self.rewardCount)

	def __RefreshRewardSlot(self, reward_vnum, reward_count):
		if not self.rewardSlot:
			return

		for slot_index in xrange(9):
			self.rewardSlot.ClearSlot(slot_index)

		if reward_vnum > 0 and reward_count > 0:
			self.rewardSlot.SetItemSlot(0, reward_vnum, reward_count)
		self.rewardSlot.RefreshSlot()

	def __GetTargetNameText(self, mob_vnum):
		if mob_vnum <= 0:
			return "Hedef: -"

		try:
			mob_name = nonplayer.GetMonsterName(mob_vnum)
		except:
			mob_name = ""

		if not mob_name:
			return "Hedef VNUM: %d" % mob_vnum

		return "Hedef: %s (%d)" % (mob_name, mob_vnum)

	def __GetRewardNameText(self, reward_vnum):
		if reward_vnum <= 0:
			return "Odul Yok"

		try:
			item.SelectItem(reward_vnum)
			reward_name = item.GetItemName()
		except:
			reward_name = ""

		if not reward_name:
			return "Item VNUM: %d" % reward_vnum

		return reward_name

	def __OnOverInRewardSlot(self, slot_index):
		if not self.itemToolTip and self.interface:
			try:
				self.itemToolTip = self.interface.tooltipItem
			except:
				self.itemToolTip = None

		if not self.itemToolTip:
			return

		if self.rewardVnum <= 0:
			return
		if slot_index != 0:
			return

		metin_slot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attr_slot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.itemToolTip.ClearToolTip()
		self.itemToolTip.AddItemData(self.rewardVnum, metin_slot, attr_slot)

	def __OnOverOutRewardSlot(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()
