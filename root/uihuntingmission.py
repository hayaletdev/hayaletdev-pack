import item
import nonplayer
import player
import ui


class HuntingMissionWindow(ui.ScriptWindow):
	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0
		self.itemToolTip = None

		self.board = None
		self.infoText = None
		self.helpText = None
		self.refreshButton = None
		self.closeButton = None

		self.indexValueText = None
		self.requiredLevelValueText = None
		self.targetValueText = None
		self.progressGauge = None
		self.progressValueText = None
		self.remainValueText = None
		self.stateValueText = None

		self.rewardSlot = None
		self.rewardNameText = None
		self.rewardCountText = None

		self.hasData = 0
		self.missionIndex = 0
		self.requiredLevel = 0
		self.targetMobVnum = 0
		self.targetCount = 0
		self.progressCount = 0
		self.rewardVnum = 0
		self.rewardCount = 0
		self.canClaim = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/huntingmissionwindow.py")

		self.board = self.GetChild("board")
		self.infoText = self.GetChild("QuestInfoText")
		self.helpText = self.GetChild("QuestHelpText")
		self.refreshButton = self.GetChild("RefreshButton")
		self.closeButton = self.GetChild("CloseButton")

		self.indexValueText = self.GetChild("MissionIndexValue")
		self.requiredLevelValueText = self.GetChild("MissionRequiredLevelValue")
		self.targetValueText = self.GetChild("MissionTargetValue")
		self.progressGauge = self.GetChild("MissionProgressGauge")
		self.progressValueText = self.GetChild("MissionProgressValue")
		self.remainValueText = self.GetChild("MissionRemainValue")
		self.stateValueText = self.GetChild("MissionStateValue")

		self.rewardSlot = self.GetChild("RewardSlot")
		self.rewardNameText = self.GetChild("RewardNameValue")
		self.rewardCountText = self.GetChild("RewardCountValue")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.refreshButton.SetEvent(ui.__mem_func__(self.RefreshMissionData))
		self.closeButton.SetEvent(ui.__mem_func__(self.Close))

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
		self.refreshButton = None
		self.closeButton = None

		self.indexValueText = None
		self.requiredLevelValueText = None
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
		self.RefreshMissionData()
		self.Show()
		self.SetTop()

	def Close(self):
		self.__OnOverOutRewardSlot()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetHuntingMissionData(self, mission_index, required_level, mob_vnum, target_count, progress_count, reward_vnum, reward_count, can_claim):
		self.hasData = 1
		self.missionIndex = max(0, int(mission_index))
		self.requiredLevel = max(0, int(required_level))
		self.targetMobVnum = int(mob_vnum)
		self.targetCount = max(0, int(target_count))
		self.progressCount = max(0, int(progress_count))
		self.rewardVnum = int(reward_vnum)
		self.rewardCount = max(0, int(reward_count))
		self.canClaim = int(can_claim)

		if self.targetCount > 0 and self.progressCount > self.targetCount:
			self.progressCount = self.targetCount

		if self.IsShow():
			self.RefreshMissionData()

	def RefreshMissionData(self):
		if not self.infoText:
			return

		if not self.hasData:
			self.infoText.SetText("Aktif Av Gorevi: 0")
			self.helpText.SetText("Sunucudan gorev verisi bekleniyor...")
			self.indexValueText.SetText("-")
			self.requiredLevelValueText.SetText("-")
			self.targetValueText.SetText("-")
			self.progressGauge.SetPercentage(0, 1)
			self.progressValueText.SetText("0 / 0")
			self.remainValueText.SetText("Kalan: 0")
			self.stateValueText.SetText("-")
			self.rewardNameText.SetText("Odul Yok")
			self.rewardCountText.SetText("x0")
			self.__RefreshRewardSlot(0, 0)
			return

		player_level = player.GetStatus(player.LEVEL)

		self.infoText.SetText("Aktif Av Gorevi: 1")
		self.helpText.SetText("Hedef tamamlaninca odul verilir, sonra siradaki gorev acilir.")

		self.indexValueText.SetText("%d" % self.missionIndex)
		self.requiredLevelValueText.SetText("%d" % self.requiredLevel)
		self.targetValueText.SetText(self.__GetTargetNameText(self.targetMobVnum))
		self.progressGauge.SetPercentage(self.progressCount, max(1, self.targetCount))
		self.progressValueText.SetText("%d / %d" % (self.progressCount, self.targetCount))
		self.remainValueText.SetText("Kalan: %d" % max(0, self.targetCount - self.progressCount))

		state_text = "In Progress"
		state_color = (1.0, 0.90, 0.45)

		if self.targetCount <= 0 or self.missionIndex <= 0:
			state_text = "Completed"
			state_color = (0.55, 1.0, 0.55)
		elif player_level < self.requiredLevel:
			state_text = "Locked"
			state_color = (1.0, 0.55, 0.55)
		elif self.canClaim == 1:
			state_text = "Claim Reward"
			state_color = (0.67, 0.88, 1.0)

		self.stateValueText.SetText(state_text)
		self.stateValueText.SetFontColor(state_color[0], state_color[1], state_color[2])

		self.rewardNameText.SetText(self.__GetRewardNameText(self.rewardVnum))
		self.rewardCountText.SetText("x%d" % max(0, self.rewardCount))
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
			return "-"

		try:
			mob_name = nonplayer.GetMonsterName(mob_vnum)
		except:
			mob_name = ""

		if not mob_name:
			return "VNUM: %d" % mob_vnum

		return "%s (%d)" % (mob_name, mob_vnum)

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
