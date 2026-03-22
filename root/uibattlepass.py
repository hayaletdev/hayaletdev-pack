import net
import ui


class BattlePassWindow(ui.ScriptWindow):
	MAX_TASK_LINES = 8
	MAX_REWARD_LINES = 8

	def __init__(self, interface):
		ui.ScriptWindow.__init__(self)

		self.interface = interface
		self.isLoaded = 0

		self.board = None
		self.stateText = None
		self.taskLines = []
		self.rewardLines = []
		self.claimFreeButton = None
		self.claimPremiumButton = None

		self.seasonId = 0
		self.isActive = 0
		self.level = 0
		self.points = 0
		self.pointsPerLevel = 0
		self.premiumActive = 0
		self.taskData = {}
		self.rewardData = {}

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		if self.isLoaded:
			return

		self.isLoaded = 1
		self.SetSize(440, 460)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")

		self.board = ui.BoardWithTitleBar()
		self.board.SetParent(self)
		self.board.SetSize(440, 460)
		self.board.SetPosition(0, 0)
		self.board.SetTitleName("Battle Pass")
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.board.Show()

		self.stateText = ui.TextLine()
		self.stateText.SetParent(self.board)
		self.stateText.SetPosition(16, 34)
		self.stateText.SetText("Battle pass verisi bekleniyor...")
		self.stateText.Show()

		taskTitle = ui.TextLine()
		taskTitle.SetParent(self.board)
		taskTitle.SetPosition(16, 64)
		taskTitle.SetText("Gorevler")
		taskTitle.Show()

		rewardTitle = ui.TextLine()
		rewardTitle.SetParent(self.board)
		rewardTitle.SetPosition(16, 242)
		rewardTitle.SetText("Oduller")
		rewardTitle.Show()

		for i in xrange(self.MAX_TASK_LINES):
			line = ui.TextLine()
			line.SetParent(self.board)
			line.SetPosition(16, 88 + (i * 18))
			line.SetText("-")
			line.Show()
			self.taskLines.append(line)

		for i in xrange(self.MAX_REWARD_LINES):
			line = ui.TextLine()
			line.SetParent(self.board)
			line.SetPosition(16, 266 + (i * 18))
			line.SetText("-")
			line.Show()
			self.rewardLines.append(line)

		self.claimFreeButton = ui.Button()
		self.claimFreeButton.SetParent(self.board)
		self.claimFreeButton.SetPosition(16, 418)
		self.claimFreeButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.claimFreeButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.claimFreeButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.claimFreeButton.SetText("Free Claim")
		self.claimFreeButton.SetEvent(ui.__mem_func__(self.__OnClickFreeClaim))
		self.claimFreeButton.Show()

		self.claimPremiumButton = ui.Button()
		self.claimPremiumButton.SetParent(self.board)
		self.claimPremiumButton.SetPosition(224, 418)
		self.claimPremiumButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.claimPremiumButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.claimPremiumButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.claimPremiumButton.SetText("Premium Claim")
		self.claimPremiumButton.SetEvent(ui.__mem_func__(self.__OnClickPremiumClaim))
		self.claimPremiumButton.Show()

		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.board = None
		self.stateText = None
		self.taskLines = []
		self.rewardLines = []
		self.taskData = {}
		self.rewardData = {}
		self.claimFreeButton = None
		self.claimPremiumButton = None
		self.interface = None

	def SetItemToolTip(self, tooltip):
		return

	def Open(self):
		self.RefreshData()
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetBattlePassState(self, season_id, active, level, points, points_per_level, premium_active):
		self.seasonId = int(season_id)
		self.isActive = int(active)
		self.level = int(level)
		self.points = int(points)
		self.pointsPerLevel = int(points_per_level)
		self.premiumActive = int(premium_active)

		if self.IsShow():
			self.RefreshData()

	def SetTaskData(self, task_id, category_id, task_type, target_vnum, progress, points, target_count):
		self.taskData[int(task_id)] = {
			"task_id": int(task_id),
			"category_id": int(category_id),
			"task_type": int(task_type),
			"target_vnum": int(target_vnum),
			"progress": int(progress),
			"points": int(points),
			"target_count": int(target_count),
			"completed": 0,
		}

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

		if self.IsShow():
			self.RefreshData()

	def RefreshData(self):
		if self.stateText:
			active_text = "Aktif" if self.isActive else "Pasif"
			premium_text = "Acik" if self.premiumActive else "Kapali"
			self.stateText.SetText("Sezon:%d | Durum:%s | Level:%d | Puan:%d/%d | Premium:%s" % (
				self.seasonId,
				active_text,
				self.level,
				self.points,
				max(1, self.pointsPerLevel),
				premium_text,
			))

		task_ids = self.taskData.keys()
		task_ids.sort()
		for i in xrange(self.MAX_TASK_LINES):
			if i < len(task_ids):
				task = self.taskData[task_ids[i]]
				completed_mark = "OK" if task["completed"] else ".."
				self.taskLines[i].SetText("[%s] Gorev %d | Vnum:%d | %d/%d | +%d" % (
					completed_mark,
					task["task_id"],
					task["target_vnum"],
					task["progress"],
					task["target_count"],
					task["points"],
				))
			else:
				self.taskLines[i].SetText("-")

		reward_levels = self.rewardData.keys()
		reward_levels.sort()
		for i in xrange(self.MAX_REWARD_LINES):
			if i < len(reward_levels):
				reward = self.rewardData[reward_levels[i]]
				free_mark = "OK" if reward["free_claimed"] else ".."
				premium_mark = "OK" if reward["premium_claimed"] else ".."
				self.rewardLines[i].SetText("Lv.%d | F(%s): %d x%d | P(%s): %d x%d" % (
					reward["level"],
					free_mark,
					reward["free_vnum"],
					reward["free_count"],
					premium_mark,
					reward["premium_vnum"],
					reward["premium_count"],
				))
			else:
				self.rewardLines[i].SetText("-")

	def __OnClickFreeClaim(self):
		claim_level = max(1, self.level)
		net.SendCommandPacket("/battlepass_claim %d 0" % claim_level)

	def __OnClickPremiumClaim(self):
		claim_level = max(1, self.level)
		net.SendCommandPacket("/battlepass_claim %d 1" % claim_level)
