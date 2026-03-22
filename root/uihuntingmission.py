import item
import net
import nonplayer
import player
import ui
import app

try:
	import modelpreviewcontroller
except:
	modelpreviewcontroller = None


class HuntingMissionWindow(ui.ScriptWindow):
	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0
		self.itemToolTip = None

		self.board = None
		self.infoText = None
		self.helpText = None
		self.missionHintText = None
		self.claimButton = None
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
		self.rewardSlotItems = {}
		self.previewPanel = None
		self.modelPreview = None
		self.modelPreviewController = None
		self.modelPreviewIndex = 0

		self.hasData = 0
		self.missionIndex = 0
		self.requiredLevel = 0
		self.targetMobVnum = 0
		self.targetCount = 0
		self.progressCount = 0
		self.rewardVnum = 0
		self.rewardCount = 0
		self.canClaim = 0
		self.fixedRewardPayload = "0"
		self.randomRewardPayload = "0"
		self.fixedRewards = []
		self.randomRewards = []
		self.isClaimPending = 0

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
		self.missionHintText = self.GetChild("MissionHintText")
		self.claimButton = self.GetChild("ClaimButton")
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
		try:
			self.previewPanel = self.GetChild("PreviewPanel")
		except:
			self.previewPanel = None

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.claimButton.SetEvent(ui.__mem_func__(self.ClaimReward))
		self.closeButton.SetEvent(ui.__mem_func__(self.Close))

		if self.rewardSlot:
			self.rewardSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInRewardSlot))
			self.rewardSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutRewardSlot))

		self.__CreateModelPreview()
		self.SetCenterPosition()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()

		self.interface = None
		self.itemToolTip = None

		self.board = None
		self.infoText = None
		self.helpText = None
		self.missionHintText = None
		self.claimButton = None
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
		self.rewardSlotItems = {}
		self.__CloseModelPreview()
		self.previewPanel = None
		self.modelPreview = None
		self.modelPreviewController = None

	def SetItemToolTip(self, tooltip):
		self.itemToolTip = tooltip

	def Open(self):
		self.RefreshMissionData()
		self.Show()
		self.SetTop()

	def Close(self):
		self.__OnOverOutRewardSlot()
		self.__CloseModelPreview()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def ClaimReward(self):
		if self.isClaimPending:
			return
		if not self.hasData:
			return

		player_level = player.GetStatus(player.LEVEL)
		can_claim_now = 0
		if self.targetCount > 0 and self.progressCount >= self.targetCount and player_level >= self.requiredLevel:
			can_claim_now = 1

		if can_claim_now != 1:
			return

		self.isClaimPending = 1
		if self.claimButton:
			self.claimButton.Disable()
		net.SendCommandPacket("/hunting_mission_claim")

	def SetHuntingMissionData(self, mission_index, required_level, mob_vnum, target_count, progress_count, reward_vnum, reward_count, can_claim, fixed_payload=None, random_payload=None):
		self.hasData = 1
		self.missionIndex = max(0, int(mission_index))
		self.requiredLevel = max(0, int(required_level))
		self.targetMobVnum = int(mob_vnum)
		self.targetCount = max(0, int(target_count))
		self.progressCount = max(0, int(progress_count))
		self.rewardVnum = int(reward_vnum)
		self.rewardCount = max(0, int(reward_count))
		self.canClaim = int(can_claim)
		self.isClaimPending = 0
		if fixed_payload is not None:
			self.fixedRewardPayload = self.__NormalizeRewardPayload(fixed_payload)
		if random_payload is not None:
			self.randomRewardPayload = self.__NormalizeRewardPayload(random_payload)
		if self.missionIndex <= 0:
			self.fixedRewardPayload = "0"
			self.randomRewardPayload = "0"

		self.fixedRewards = self.__ParseRewardPayload(self.fixedRewardPayload)
		self.randomRewards = self.__ParseRewardPayload(self.randomRewardPayload)

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
			if self.missionHintText:
				self.missionHintText.SetText("Hedef tamamlaninca Odulu Al butonunu kullan.")
			self.rewardNameText.SetText("Odul Yok")
			self.rewardCountText.SetText("x0")
			self.__RefreshRewardSlot([])
			if self.claimButton:
				self.claimButton.Disable()
			self.__RefreshModelPreview()
			return

		player_level = player.GetStatus(player.LEVEL)

		self.infoText.SetText("Aktif Av Gorevi: 1")
		self.helpText.SetText("Hedef tamamlaninca Odulu Al ile odulu alip siradaki goreve gec.")

		self.indexValueText.SetText("%d" % self.missionIndex)
		self.requiredLevelValueText.SetText("%d" % self.requiredLevel)
		self.targetValueText.SetText(self.__GetTargetNameText(self.targetMobVnum))
		self.progressGauge.SetPercentage(self.progressCount, max(1, self.targetCount))
		self.progressValueText.SetText("%d / %d" % (self.progressCount, self.targetCount))
		self.remainValueText.SetText("Kalan: %d" % max(0, self.targetCount - self.progressCount))

		local_can_claim = 0
		if self.targetCount > 0 and self.progressCount >= self.targetCount and player_level >= self.requiredLevel:
			local_can_claim = 1

		state_text = "In Progress"
		state_color = (1.0, 0.90, 0.45)

		if self.targetCount <= 0 or self.missionIndex <= 0:
			state_text = "Completed"
			state_color = (0.55, 1.0, 0.55)
		elif player_level < self.requiredLevel:
			state_text = "Locked"
			state_color = (1.0, 0.55, 0.55)
		elif self.canClaim == 1 or local_can_claim == 1:
			state_text = "Claim Reward"
			state_color = (0.67, 0.88, 1.0)

		self.stateValueText.SetText(state_text)
		self.stateValueText.SetFontColor(state_color[0], state_color[1], state_color[2])
		if self.claimButton:
			if local_can_claim == 1 and self.isClaimPending == 0:
				self.claimButton.Enable()
			else:
				self.claimButton.Disable()

		guaranteed_rewards = self.__MergeRewardList([(self.rewardVnum, self.rewardCount)] + self.fixedRewards)
		random_rewards = self.__MergeRewardList(self.randomRewards)
		display_rewards = []

		for reward_info in guaranteed_rewards:
			display_rewards.append((reward_info[0], reward_info[1], 0))
		for reward_info in random_rewards:
			display_rewards.append((reward_info[0], reward_info[1], 1))

		if len(guaranteed_rewards) <= 0 and len(random_rewards) <= 0:
			self.rewardNameText.SetText("Odul Yok")
			self.rewardCountText.SetText("x0")
		elif len(random_rewards) <= 0:
			if len(guaranteed_rewards) == 1:
				self.rewardNameText.SetText(self.__GetRewardNameText(guaranteed_rewards[0][0]))
				self.rewardCountText.SetText("x%d" % max(0, guaranteed_rewards[0][1]))
			else:
				self.rewardNameText.SetText("Sabit Oduller")
				self.rewardCountText.SetText("%d kalem odul" % len(guaranteed_rewards))
		else:
			self.rewardNameText.SetText("Sabit + Random Havuz")
			preview_count = min(9, len(display_rewards))
			if len(display_rewards) > preview_count:
				self.rewardCountText.SetText("Sabit:%d Random:%d den 1 (Onizleme %d/%d)" % (len(guaranteed_rewards), len(random_rewards), preview_count, len(display_rewards)))
			else:
				self.rewardCountText.SetText("Sabit:%d Random:%d den 1" % (len(guaranteed_rewards), len(random_rewards)))

		if self.missionHintText:
			if len(random_rewards) > 0:
				self.missionHintText.SetText("Not: Random havuzdan sadece 1 odul verilir.")
			else:
				self.missionHintText.SetText("Hedef tamamlaninca Odulu Al butonunu kullan.")

		self.__RefreshRewardSlot(display_rewards)
		self.__RefreshModelPreview()

	def __GetModelPreviewIndex(self):
		if modelpreviewcontroller and hasattr(modelpreviewcontroller, "default_shared_window_index"):
			return modelpreviewcontroller.default_shared_window_index()
		if hasattr(app, "RENDER_TARGET_INDEX_MYSHOPDECO"):
			return app.RENDER_TARGET_INDEX_MYSHOPDECO
		return 0

	def __CreateModelPreview(self):
		if not self.previewPanel:
			return
		if not modelpreviewcontroller:
			return

		self.modelPreviewIndex = self.__GetModelPreviewIndex()
		self.modelPreviewController = modelpreviewcontroller.ModelPreviewController(self.modelPreviewIndex)

		self.modelPreview = ui.RenderTarget()
		self.modelPreview.SetParent(self.previewPanel)
		self.modelPreview.SetPosition(126, 32)
		self.modelPreview.SetSize(96, 92)
		self.modelPreview.SetRenderTarget(self.modelPreviewIndex)
		self.modelPreview.Show()

	def __CloseModelPreview(self):
		if self.modelPreviewController:
			self.modelPreviewController.close()

	def __RefreshModelPreview(self):
		if not self.modelPreviewController:
			return

		if self.hasData and self.targetMobVnum > 0:
			if not self.modelPreviewController.show_monster(self.targetMobVnum):
				self.modelPreviewController.close()
		else:
			self.modelPreviewController.close()

	def __RefreshRewardSlot(self, reward_list):
		if not self.rewardSlot:
			return

		self.rewardSlotItems = {}

		for slot_index in xrange(9):
			self.rewardSlot.ClearSlot(slot_index)

		slot_count = min(9, len(reward_list))
		for slot_index in xrange(slot_count):
			reward_info = reward_list[slot_index]
			reward_vnum = reward_info[0]
			reward_count = reward_info[1]
			if reward_vnum <= 0 or reward_count <= 0:
				continue
			self.rewardSlot.SetItemSlot(slot_index, reward_vnum, reward_count)
			self.rewardSlotItems[slot_index] = reward_info

		self.rewardSlot.RefreshSlot()

	def __NormalizeRewardPayload(self, payload):
		normalized = str(payload).strip()
		if not normalized:
			return "0"
		return normalized

	def __ParseRewardPayload(self, payload):
		reward_list = []
		if not payload or payload == "0":
			return reward_list

		for token in payload.split(","):
			token = token.strip()
			if not token:
				continue

			parts = token.split(":")
			if len(parts) != 2:
				continue

			try:
				reward_vnum = int(parts[0])
				reward_count = int(parts[1])
			except:
				continue

			if reward_vnum <= 0 or reward_count <= 0:
				continue

			reward_list.append((reward_vnum, reward_count))

		return reward_list

	def __MergeRewardList(self, reward_list):
		merged = []
		for reward_info in reward_list:
			reward_vnum = int(reward_info[0])
			reward_count = int(reward_info[1])
			if reward_vnum <= 0 or reward_count <= 0:
				continue

			is_updated = 0
			for idx in xrange(len(merged)):
				if merged[idx][0] == reward_vnum:
					merged[idx] = (merged[idx][0], merged[idx][1] + reward_count)
					is_updated = 1
					break

			if not is_updated:
				merged.append((reward_vnum, reward_count))

		return merged

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

		if not self.rewardSlotItems.has_key(slot_index):
			return

		reward_vnum = self.rewardSlotItems[slot_index][0]
		if reward_vnum <= 0:
			return

		metin_slot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attr_slot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.itemToolTip.ClearToolTip()
		self.itemToolTip.AddItemData(reward_vnum, metin_slot, attr_slot)

	def __OnOverOutRewardSlot(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()
