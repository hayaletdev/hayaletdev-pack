import net
import nonplayer
import app
import ui

try:
	import modelpreviewcontroller
except:
	modelpreviewcontroller = None


class BattlePassWindow(ui.ScriptWindow):
	MAX_TASK_LINES = 8

	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0

		self.board = None
		self.leftPanel = None
		self.previewPanel = None
		self.seasonText = None
		self.levelText = None
		self.pointText = None
		self.statusText = None
		self.detailTitleText = None
		self.detailProgressText = None
		self.bonusLine1 = None
		self.bonusLine2 = None
		self.bonusLine3 = None
		self.freeClaimButton = None
		self.premiumClaimButton = None

		self.modelPreview = None
		self.modelPreviewController = None
		self.modelPreviewIndex = 0

		self.taskRows = []
		self.taskData = {}
		self.rewardData = {}

		self.seasonId = 0
		self.isActive = 0
		self.level = 0
		self.points = 0
		self.pointsPerLevel = 100
		self.premiumActive = 0
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
		self.detailTitleText = self.GetChild("DetailTitleText")
		self.detailProgressText = self.GetChild("DetailProgressText")
		self.bonusLine1 = self.GetChild("BonusLine1")
		self.bonusLine2 = self.GetChild("BonusLine2")
		self.bonusLine3 = self.GetChild("BonusLine3")
		self.freeClaimButton = self.GetChild("FreeClaimButton")
		self.premiumClaimButton = self.GetChild("PremiumClaimButton")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.freeClaimButton.SetEvent(ui.__mem_func__(self.__OnClickFreeClaim))
		self.premiumClaimButton.SetEvent(ui.__mem_func__(self.__OnClickPremiumClaim))

		self.__CreateTaskRows()
		self.__CreateModelPreview()

		self.SetCenterPosition()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.__CloseModelPreview()

		self.interface = None
		self.board = None
		self.leftPanel = None
		self.previewPanel = None
		self.seasonText = None
		self.levelText = None
		self.pointText = None
		self.statusText = None
		self.detailTitleText = None
		self.detailProgressText = None
		self.bonusLine1 = None
		self.bonusLine2 = None
		self.bonusLine3 = None
		self.freeClaimButton = None
		self.premiumClaimButton = None
		self.modelPreview = None
		self.modelPreviewController = None
		self.taskRows = []
		self.taskData = {}
		self.rewardData = {}

	def SetItemToolTip(self, tooltip):
		return

	def Open(self):
		self.Show()
		self.SetTop()
		self.RefreshData()

	def Close(self):
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
		if not self.previewPanel:
			return
		if not modelpreviewcontroller:
			return

		self.modelPreviewIndex = self.__GetModelPreviewIndex()
		self.modelPreviewController = modelpreviewcontroller.ModelPreviewController(self.modelPreviewIndex)

		self.modelPreview = ui.RenderTarget()
		self.modelPreview.SetParent(self.previewPanel)
		self.modelPreview.SetPosition(8, 26)
		self.modelPreview.SetSize(120, 320)
		self.modelPreview.SetRenderTarget(self.modelPreviewIndex)
		self.modelPreview.Show()

	def __CloseModelPreview(self):
		if self.modelPreviewController:
			self.modelPreviewController.close()

	def __RefreshModelPreview(self):
		if not self.modelPreviewController:
			return

		task = self.__GetSelectedTask()
		if not task:
			self.modelPreviewController.close()
			return

		target_vnum = task.get("target_vnum", 0)
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
			row_y = 10 + (i * 44)

			row_bar = ui.Bar()
			row_bar.SetParent(self.leftPanel)
			row_bar.SetPosition(8, row_y)
			row_bar.SetSize(322, 40)
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
			gauge.MakeGauge(200, "red")
			gauge.SetPercentage(0, 1)
			gauge.Show()

			progress_line = ui.TextLine()
			progress_line.SetParent(row_bar)
			progress_line.SetPosition(214, 20)
			progress_line.SetText("0/0")
			progress_line.Show()

			slots_line = ui.TextLine()
			slots_line.SetParent(row_bar)
			slots_line.SetPosition(268, 12)
			slots_line.SetText("[ ] [ ] [ ]")
			slots_line.Show()

			self.taskRows.append({
				"bar": row_bar,
				"name": name_line,
				"gauge": gauge,
				"progress": progress_line,
				"slots": slots_line,
			})

	def SetBattlePassState(self, season_id, active, level, points, points_per_level, premium_active):
		self.seasonId = int(season_id)
		self.isActive = int(active)
		self.level = int(level)
		self.points = int(points)
		self.pointsPerLevel = max(1, int(points_per_level))
		self.premiumActive = int(premium_active)
		if self.IsShow():
			self.RefreshData()

	def SetTaskData(self, task_id, category_id, task_type, target_vnum, progress, points, target_count):
		task_id = int(task_id)
		self.taskData[task_id] = {
			"task_id": task_id,
			"category_id": int(category_id),
			"task_type": int(task_type),
			"target_vnum": int(target_vnum),
			"progress": max(0, int(progress)),
			"points": max(0, int(points)),
			"target_count": max(0, int(target_count)),
			"completed": 0,
		}

		if self.selectedTaskId <= 0:
			self.selectedTaskId = task_id

		if self.IsShow():
			self.RefreshData()

	def SetTaskState(self, task_id, completed):
		task_id = int(task_id)
		if not self.taskData.has_key(task_id):
			self.taskData[task_id] = {
				"task_id": task_id,
				"category_id": 0,
				"task_type": 0,
				"target_vnum": 0,
				"progress": 0,
				"points": 0,
				"target_count": 0,
				"completed": int(completed),
			}
		else:
			self.taskData[task_id]["completed"] = int(completed)

		if self.selectedTaskId <= 0:
			self.selectedTaskId = task_id

		if self.IsShow():
			self.RefreshData()

	def SetRewardData(self, level, free_vnum, free_count, premium_vnum, premium_count, free_claimed, premium_claimed):
		self.rewardData[int(level)] = {
			"level": int(level),
			"free_vnum": int(free_vnum),
			"free_count": int(free_count),
			"premium_vnum": int(premium_vnum),
			"premium_count": int(premium_count),
			"free_claimed": int(free_claimed),
			"premium_claimed": int(premium_claimed),
		}

	def __GetTaskName(self, task):
		target_vnum = task.get("target_vnum", 0)
		if target_vnum <= 0:
			return "Gorev"

		mob_name = ""
		try:
			mob_name = nonplayer.GetMonsterName(target_vnum)
		except:
			mob_name = ""

		if not mob_name:
			return "VNUM %d" % target_vnum

		return mob_name

	def __PickSelectedTask(self):
		if len(self.taskData) <= 0:
			self.selectedTaskId = 0
			return

		if self.selectedTaskId > 0 and self.taskData.has_key(self.selectedTaskId):
			return

		task_ids = self.taskData.keys()
		task_ids.sort()
		self.selectedTaskId = int(task_ids[0])

	def __GetSelectedTask(self):
		self.__PickSelectedTask()
		if self.selectedTaskId <= 0:
			return None
		if not self.taskData.has_key(self.selectedTaskId):
			return None
		return self.taskData[self.selectedTaskId]

	def RefreshData(self):
		self.__PickSelectedTask()

		if self.seasonText:
			self.seasonText.SetText("Sezon: %d" % self.seasonId)
		if self.levelText:
			self.levelText.SetText("Level: %d" % self.level)
		if self.pointText:
			self.pointText.SetText("Puan: %d/%d" % (self.points, self.pointsPerLevel))

		status_text = "Durum: Devam Ediyor"
		if self.isActive <= 0:
			status_text = "Durum: Pasif"
		if self.statusText:
			self.statusText.SetText(status_text)

		task_ids = self.taskData.keys()
		task_ids.sort()

		for i in xrange(self.MAX_TASK_LINES):
			row = self.taskRows[i]
			if i >= len(task_ids):
				row["name"].SetText("-")
				row["gauge"].SetPercentage(0, 1)
				row["progress"].SetText("0/0")
				row["slots"].SetText("[ ] [ ] [ ]")
				row["bar"].SetColor(0x55000000)
				continue

			task = self.taskData[task_ids[i]]
			task_name = self.__GetTaskName(task)
			progress = int(task.get("progress", 0))
			target_count = max(1, int(task.get("target_count", 0)))
			points = max(0, int(task.get("points", 0)))

			row["name"].SetText(task_name)
			row["gauge"].SetPercentage(progress, target_count)
			row["progress"].SetText("%d/%d" % (progress, target_count))
			row["slots"].SetText("+%d P" % points)

			if task_ids[i] == self.selectedTaskId:
				row["bar"].SetColor(0x88301010)
			else:
				row["bar"].SetColor(0x55000000)

		selected = self.__GetSelectedTask()
		if not selected:
			if self.detailTitleText:
				self.detailTitleText.SetText("Gorev Detayi")
			if self.detailProgressText:
				self.detailProgressText.SetText("Ilerleme: 0/0")
			if self.bonusLine1:
				self.bonusLine1.SetText("-")
			if self.bonusLine2:
				self.bonusLine2.SetText("-")
			if self.bonusLine3:
				self.bonusLine3.SetText("-")
			self.__RefreshModelPreview()
			return

		progress = int(selected.get("progress", 0))
		target_count = max(1, int(selected.get("target_count", 0)))
		points = max(0, int(selected.get("points", 0)))
		completed = int(selected.get("completed", 0))

		if self.detailTitleText:
			self.detailTitleText.SetText(self.__GetTaskName(selected))
		if self.detailProgressText:
			self.detailProgressText.SetText("Ilerleme: %d/%d" % (progress, target_count))

		if self.bonusLine1:
			if completed == 1:
				self.bonusLine1.SetText("- Durum: Tamamlandi")
			else:
				self.bonusLine1.SetText("- Durum: Devam Ediyor")
		if self.bonusLine2:
			self.bonusLine2.SetText("- Gorev Puani: +%d" % points)
		if self.bonusLine3:
			if self.premiumActive > 0:
				self.bonusLine3.SetText("- Premium Hat: Acik")
			else:
				self.bonusLine3.SetText("- Premium Hat: Kapali")

		self.__RefreshModelPreview()

	def __FindClaimLevel(self, premium_track):
		reward_levels = self.rewardData.keys()
		reward_levels.sort()
		for level in reward_levels:
			reward = self.rewardData[level]
			if level > self.level:
				continue
			if premium_track:
				if reward["premium_claimed"] == 0:
					return level
			else:
				if reward["free_claimed"] == 0:
					return level
		return max(1, self.level)

	def __OnClickFreeClaim(self):
		claim_level = self.__FindClaimLevel(False)
		net.SendCommandPacket("/battlepass_claim %d 0" % claim_level)

	def __OnClickPremiumClaim(self):
		claim_level = self.__FindClaimLevel(True)
		net.SendCommandPacket("/battlepass_claim %d 1" % claim_level)


