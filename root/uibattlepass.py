import app
import item
import net
import nonplayer
import ui

try:
	import modelpreviewcontroller
except:
	modelpreviewcontroller = None


class BattlePassWindow(ui.ScriptWindow):
	MAX_TASK_LINES = 7
	CATEGORY_PVM = 0
	CATEGORY_GENERAL = 1

	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0
		self.itemToolTip = None

		self.board = None
		self.leftPanel = None
		self.previewPanel = None
		self.seasonText = None
		self.levelText = None
		self.pointText = None
		self.statusText = None
		self.categoryText = None
		self.detailTitleText = None
		self.detailProgressText = None
		self.bonusLine1 = None
		self.bonusLine2 = None
		self.bonusLine3 = None
		self.claimButton = None
		self.tabPvmButton = None
		self.tabGeneralButton = None
		self.tabHintText = None
		self.rewardSlot = None
		self.rewardNameText = None
		self.rewardCountText = None

		self.modelPreview = None
		self.modelPreviewController = None
		self.modelPreviewIndex = 0

		self.taskRows = []
		self.taskData = {}

		self.seasonId = 0
		self.isActive = 0
		self.completedCount = 0
		self.totalCount = 0
		self.currentCategory = self.CATEGORY_PVM
		self.selectedTaskId = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded:
			return

		self.isLoaded = 1
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/battlepasswindow.py")

		self.board = self.GetChild("board")
		self.leftPanel = self.GetChild("LeftPanel")
		self.previewPanel = self.GetChild("PreviewPanel")
		self.seasonText = self.GetChild("SeasonText")
		self.levelText = self.GetChild("LevelText")
		self.pointText = self.GetChild("PointText")
		self.statusText = self.GetChild("StatusText")
		self.categoryText = self.GetChild("CategoryText")
		self.detailTitleText = self.GetChild("DetailTitleText")
		self.detailProgressText = self.GetChild("DetailProgressText")
		self.bonusLine1 = self.GetChild("BonusLine1")
		self.bonusLine2 = self.GetChild("BonusLine2")
		self.bonusLine3 = self.GetChild("BonusLine3")
		self.claimButton = self.GetChild("ClaimButton")
		self.tabPvmButton = self.GetChild("TabPvmButton")
		self.tabGeneralButton = self.GetChild("TabGeneralButton")
		self.tabHintText = self.GetChild("TabHintText")
		self.rewardSlot = self.GetChild("RewardSlot")
		self.rewardNameText = self.GetChild("RewardNameText")
		self.rewardCountText = self.GetChild("RewardCountText")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.claimButton.SetEvent(ui.__mem_func__(self.__OnClickClaim))
		self.tabPvmButton.SetEvent(ui.__mem_func__(self.__OnClickTabPvm))
		self.tabGeneralButton.SetEvent(ui.__mem_func__(self.__OnClickTabGeneral))
		self.tabPvmButton.SetText("PvM")
		self.tabGeneralButton.SetText("Genel")

		if self.rewardSlot:
			self.rewardSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInRewardSlot))
			self.rewardSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutRewardSlot))

		self.__CreateTaskRows()
		self.__CreateModelPreview()
		self.SetCenterPosition()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.__CloseModelPreview()
		self.interface = None
		self.itemToolTip = None
		self.taskRows = []
		self.taskData = {}

	def SetItemToolTip(self, tooltip):
		self.itemToolTip = tooltip

	def Open(self):
		self.Show()
		self.SetTop()
		self.RefreshData()

	def Close(self):
		self.__OnOverOutRewardSlot()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __GetModelPreviewIndex(self):
		if modelpreviewcontroller and hasattr(modelpreviewcontroller, "default_shared_window_index"):
			return modelpreviewcontroller.default_shared_window_index()
		if hasattr(app, "RENDER_TARGET_INDEX_MYSHOPDECO"):
			return app.RENDER_TARGET_INDEX_MYSHOPDECO
		return 0

	def __CreateModelPreview(self):
		if not self.previewPanel or not modelpreviewcontroller:
			return

		self.modelPreviewIndex = self.__GetModelPreviewIndex()
		self.modelPreviewController = modelpreviewcontroller.ModelPreviewController(self.modelPreviewIndex)
		self.modelPreview = ui.RenderTarget()
		self.modelPreview.SetParent(self.previewPanel)
		self.modelPreview.SetPosition(8, 28)
		self.modelPreview.SetSize(116, 234)
		self.modelPreview.SetRenderTarget(self.modelPreviewIndex)
		self.modelPreview.Show()

	def __CloseModelPreview(self):
		if self.modelPreviewController:
			self.modelPreviewController.close()

	def __RefreshModelPreview(self, task):
		if not self.modelPreviewController:
			return
		if not task:
			self.modelPreviewController.close()
			return

		target_vnum = int(task.get("target_vnum", 0))
		if target_vnum > 0:
			if not self.modelPreviewController.show_monster(target_vnum):
				self.modelPreviewController.close()
		else:
			self.modelPreviewController.close()

	def __CreateTaskRows(self):
		if not self.leftPanel:
			return

		self.taskRows = []
		for i in xrange(self.MAX_TASK_LINES):
			row_y = 8 + (i * 46)

			row_bar = ui.Bar()
			row_bar.SetParent(self.leftPanel)
			row_bar.SetPosition(6, row_y)
			row_bar.SetSize(328, 42)
			row_bar.SetColor(0x55000000)
			row_bar.Show()

			name_line = ui.TextLine()
			name_line.SetParent(row_bar)
			name_line.SetPosition(8, 4)
			name_line.SetText("-")
			name_line.Show()

			gauge = ui.Gauge()
			gauge.SetParent(row_bar)
			gauge.SetPosition(8, 20)
			gauge.MakeGauge(162, "red")
			gauge.SetPercentage(0, 1)
			gauge.Show()

			progress_line = ui.TextLine()
			progress_line.SetParent(row_bar)
			progress_line.SetPosition(174, 20)
			progress_line.SetText("0/0")
			progress_line.Show()

			reward_line = ui.TextLine()
			reward_line.SetParent(row_bar)
			reward_line.SetPosition(214, 20)
			reward_line.SetText("Odul:-")
			reward_line.Show()

			select_button = ui.Button()
			select_button.SetParent(row_bar)
			select_button.SetPosition(284, 10)
			select_button.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
			select_button.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
			select_button.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
			select_button.SetText("Sec")
			select_button.Show()

			self.taskRows.append({
				"bar": row_bar,
				"name": name_line,
				"gauge": gauge,
				"progress": progress_line,
				"reward": reward_line,
				"button": select_button,
				"task_id": 0,
			})

	def SetBattlePassState(self, season_id, active, level, points, points_per_level, premium_active):
		self.seasonId = int(season_id)
		self.isActive = int(active)
		self.completedCount = int(level)
		self.totalCount = int(points)
		if self.IsShow():
			self.RefreshData()

	def SetTaskData(self, task_id, category_id, task_type, target_vnum, progress, points, target_count):
		task_id = int(task_id)
		if not self.taskData.has_key(task_id):
			self.taskData[task_id] = {}

		task = self.taskData[task_id]
		task["task_id"] = task_id
		task["category_id"] = int(category_id)
		task["task_type"] = int(task_type)
		task["target_vnum"] = int(target_vnum)
		task["progress"] = max(0, int(progress))
		task["target_count"] = max(0, int(target_count))
		if not task.has_key("completed"):
			task["completed"] = 0
		if not task.has_key("reward_vnum"):
			task["reward_vnum"] = 0
		if not task.has_key("reward_count"):
			task["reward_count"] = 0
		if not task.has_key("reward_claimed"):
			task["reward_claimed"] = 0

		if self.selectedTaskId <= 0:
			self.selectedTaskId = task_id
		if self.IsShow():
			self.RefreshData()

	def SetTaskState(self, task_id, completed):
		task_id = int(task_id)
		if not self.taskData.has_key(task_id):
			self.taskData[task_id] = {"task_id": task_id}
		self.taskData[task_id]["completed"] = int(completed)
		if self.IsShow():
			self.RefreshData()

	def SetTaskReward(self, task_id, reward_vnum, reward_count, claimed):
		task_id = int(task_id)
		if not self.taskData.has_key(task_id):
			self.taskData[task_id] = {"task_id": task_id}
		task = self.taskData[task_id]
		task["reward_vnum"] = int(reward_vnum)
		task["reward_count"] = int(reward_count)
		task["reward_claimed"] = int(claimed)
		if self.IsShow():
			self.RefreshData()

	def SetRewardData(self, level, free_vnum, free_count, premium_vnum, premium_count, free_claimed, premium_claimed):
		return

	def __GetTaskName(self, task):
		target_vnum = int(task.get("target_vnum", 0))
		if target_vnum <= 0:
			return "Gorev #%d" % int(task.get("task_id", 0))
		mob_name = ""
		try:
			mob_name = nonplayer.GetMonsterName(target_vnum)
		except:
			mob_name = ""
		if not mob_name:
			return "VNUM %d" % target_vnum
		return mob_name

	def __GetItemName(self, item_vnum):
		if item_vnum <= 0:
			return "-"
		try:
			item.SelectItem(item_vnum)
			name = item.GetItemName()
		except:
			name = ""
		if not name:
			return "VNUM %d" % item_vnum
		return name

	def __GetFilteredTaskIds(self):
		result = []
		for task_id in self.taskData.keys():
			if int(self.taskData[task_id].get("category_id", 0)) == self.currentCategory:
				result.append(task_id)
		result.sort()
		return result

	def __EnsureSelectedTask(self):
		filtered = self.__GetFilteredTaskIds()
		if len(filtered) <= 0:
			self.selectedTaskId = 0
			return
		if self.selectedTaskId > 0 and self.selectedTaskId in filtered:
			return

		for task_id in filtered:
			if int(self.taskData[task_id].get("reward_claimed", 0)) == 0:
				self.selectedTaskId = task_id
				return
		self.selectedTaskId = filtered[0]

	def __SelectTask(self, task_id):
		self.selectedTaskId = int(task_id)
		self.RefreshData()

	def __OnClickTabPvm(self):
		self.currentCategory = self.CATEGORY_PVM
		self.selectedTaskId = 0
		self.RefreshData()

	def __OnClickTabGeneral(self):
		self.currentCategory = self.CATEGORY_GENERAL
		self.selectedTaskId = 0
		self.RefreshData()

	def __OnClickClaim(self):
		self.__EnsureSelectedTask()
		if self.selectedTaskId <= 0:
			return
		net.SendCommandPacket("/battlepass_claim %d 0" % self.selectedTaskId)

	def RefreshData(self):
		self.__EnsureSelectedTask()

		self.seasonText.SetText("Sezon: %d" % self.seasonId)
		self.levelText.SetText("Tamamlanan: %d" % self.completedCount)
		self.pointText.SetText("Toplam Gorev: %d" % self.totalCount)
		if self.isActive > 0:
			self.statusText.SetText("Durum: Devam Ediyor")
		else:
			self.statusText.SetText("Durum: Pasif")
		if self.currentCategory == self.CATEGORY_PVM:
			self.categoryText.SetText("Kategori: PVM Gorevleri")
		else:
			self.categoryText.SetText("Kategori: Genel Gorevler")
		self.tabHintText.SetText("Sol alttan sekme degistir")

		filtered = self.__GetFilteredTaskIds()
		for i in xrange(self.MAX_TASK_LINES):
			row = self.taskRows[i]
			row["task_id"] = 0
			if i >= len(filtered):
				row["name"].SetText("-")
				row["gauge"].SetPercentage(0, 1)
				row["progress"].SetText("0/0")
				row["reward"].SetText("Odul:-")
				row["bar"].SetColor(0x55000000)
				row["button"].Hide()
				continue

			task_id = filtered[i]
			task = self.taskData[task_id]
			progress = int(task.get("progress", 0))
			target_count = max(1, int(task.get("target_count", 0)))
			reward_vnum = int(task.get("reward_vnum", 0))
			reward_count = int(task.get("reward_count", 0))
			reward_claimed = int(task.get("reward_claimed", 0))

			row["task_id"] = task_id
			row["name"].SetText(self.__GetTaskName(task))
			row["gauge"].SetPercentage(progress, target_count)
			row["progress"].SetText("%d/%d" % (progress, target_count))
			if reward_claimed == 1:
				row["reward"].SetText("Odul: Alindi")
			else:
				row["reward"].SetText("%s x%d" % (self.__GetItemName(reward_vnum), reward_count))

			if task_id == self.selectedTaskId:
				row["bar"].SetColor(0x99301010)
			else:
				row["bar"].SetColor(0x55000000)

			row["button"].Show()
			row["button"].SetEvent(lambda arg_task_id=task_id: self.__SelectTask(arg_task_id))

		selected = None
		if self.selectedTaskId > 0 and self.taskData.has_key(self.selectedTaskId):
			selected = self.taskData[self.selectedTaskId]

		if not selected:
			self.detailTitleText.SetText("Gorev Detayi")
			self.detailProgressText.SetText("Ilerleme: 0/0")
			self.bonusLine1.SetText("-")
			self.bonusLine2.SetText("-")
			self.bonusLine3.SetText("-")
			self.rewardNameText.SetText("Odul: -")
			self.rewardCountText.SetText("x0")
			self.__RefreshRewardSlot(0, 0)
			self.__RefreshModelPreview(None)
			self.claimButton.Disable()
			return

		progress = int(selected.get("progress", 0))
		target_count = max(1, int(selected.get("target_count", 0)))
		reward_vnum = int(selected.get("reward_vnum", 0))
		reward_count = int(selected.get("reward_count", 0))
		reward_claimed = int(selected.get("reward_claimed", 0))

		self.detailTitleText.SetText(self.__GetTaskName(selected))
		self.detailProgressText.SetText("Ilerleme: %d/%d" % (progress, target_count))
		if progress >= target_count:
			self.bonusLine1.SetText("- Durum: Tamamlandi")
		else:
			self.bonusLine1.SetText("- Durum: Devam Ediyor")
		if reward_claimed == 1:
			self.bonusLine2.SetText("- Odul Durumu: Alindi")
		else:
			self.bonusLine2.SetText("- Odul Durumu: Bekliyor")
		self.bonusLine3.SetText("- Gorev ID: %d" % int(selected.get("task_id", 0)))

		self.rewardNameText.SetText("Odul: %s" % self.__GetItemName(reward_vnum))
		self.rewardCountText.SetText("x%d" % reward_count)
		self.__RefreshRewardSlot(reward_vnum, reward_count)
		self.__RefreshModelPreview(selected)

		if progress >= target_count and reward_claimed == 0:
			self.claimButton.Enable()
		else:
			self.claimButton.Disable()

	def __RefreshRewardSlot(self, reward_vnum, reward_count):
		if not self.rewardSlot:
			return
		self.rewardSlot.ClearSlot(0)
		if reward_vnum > 0 and reward_count > 0:
			self.rewardSlot.SetItemSlot(0, reward_vnum, reward_count)
		self.rewardSlot.RefreshSlot()

	def __OnOverInRewardSlot(self, slot_index):
		if slot_index != 0:
			return
		if not self.itemToolTip and self.interface:
			try:
				self.itemToolTip = self.interface.tooltipItem
			except:
				self.itemToolTip = None
		if not self.itemToolTip:
			return

		if self.selectedTaskId <= 0 or not self.taskData.has_key(self.selectedTaskId):
			return
		reward_vnum = int(self.taskData[self.selectedTaskId].get("reward_vnum", 0))
		if reward_vnum <= 0:
			return

		import player
		metin_slot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attr_slot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		self.itemToolTip.ClearToolTip()
		self.itemToolTip.AddItemData(reward_vnum, metin_slot, attr_slot)

	def __OnOverOutRewardSlot(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()
