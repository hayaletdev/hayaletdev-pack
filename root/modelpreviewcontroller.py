import app
import nonplayer
import player

try:
	import renderTarget
except:
	try:
		import rendertarget as renderTarget
	except:
		renderTarget = None

try:
	import mountpreviewmap
except:
	mountpreviewmap = None


class ModelPreviewController(object):
	"""
	Reusable model preview helper for custom UI windows.
	
	Usage:
		ctrl = ModelPreviewController()
		ctrl.show_player(playerRace, armor_vnum)
		ctrl.close()
	"""

	def __init__(self, render_index=0):
		self.render_index = render_index
		self._last_signature = None

	def set_index(self, render_index):
		self.render_index = render_index
		self._last_signature = None

	def close(self):
		if not renderTarget:
			return
		renderTarget.SetVisibility(self.render_index, False)
		self._last_signature = None

	def show_player(self, race_vnum, armor_vnum=0, weapon_vnum=0, hair_vnum=0, acce_vnum=0, force=False):
		if not renderTarget:
			return False
		if race_vnum < 0:
			return False

		signature = ("player", int(race_vnum), int(armor_vnum), int(weapon_vnum), int(hair_vnum), int(acce_vnum))
		if not force and self._last_signature == signature:
			return True

		renderTarget.SetVisibility(self.render_index, True)
		renderTarget.SelectModel(self.render_index, int(race_vnum))

		if armor_vnum > 0:
			renderTarget.SetArmor(self.render_index, int(armor_vnum))
		if weapon_vnum > 0:
			renderTarget.SetWeapon(self.render_index, int(weapon_vnum))
		if hair_vnum > 0:
			renderTarget.SetHair(self.render_index, int(hair_vnum))
		if acce_vnum > 0:
			renderTarget.SetAcce(self.render_index, int(acce_vnum))

		renderTarget.SetEffect(self.render_index)
		self._last_signature = signature
		return True

	def show_monster(self, model_vnum, force=False):
		if not renderTarget:
			return False
		if not self._is_valid_monster(model_vnum):
			return False

		signature = ("monster", int(model_vnum))
		if not force and self._last_signature == signature:
			return True

		renderTarget.SetVisibility(self.render_index, True)
		renderTarget.SelectModel(self.render_index, int(model_vnum))
		renderTarget.SetEffect(self.render_index)
		self._last_signature = signature
		return True

	def resolve_mount_model(self, item_vnum, affect_list=None, value_list=None):
		# 1) Runtime affect payload (APPLY_MOUNT) when available.
		if affect_list:
			for affect_type, affect_value in affect_list:
				try:
					affect_value = int(affect_value)
				except:
					continue
				if affect_value > 0 and 20000 <= affect_value < 40000:
					return affect_value

		# 2) Static map from item proto.
		try:
			item_vnum = int(item_vnum)
		except:
			item_vnum = 0

		if item_vnum > 0 and mountpreviewmap and hasattr(mountpreviewmap, "MOUNT_ITEM_TO_MODEL"):
			model = mountpreviewmap.MOUNT_ITEM_TO_MODEL.get(item_vnum, 0)
			if model > 0:
				return model

		# 3) Last fallback from values.
		if value_list:
			for value in value_list:
				try:
					ivalue = int(value)
				except:
					continue
				if 20000 <= ivalue < 40000:
					return ivalue

		return 0

	def resolve_pet_model(self, value_list):
		if not value_list:
			return 0

		for value in value_list:
			try:
				ivalue = int(value)
			except:
				continue

			if 10000 <= ivalue < 1000000 and self._is_valid_monster(ivalue):
				return ivalue

		return 0

	def _is_valid_monster(self, vnum):
		try:
			vnum = int(vnum)
		except:
			return False

		if vnum <= 0:
			return False

		try:
			name = nonplayer.GetMonsterName(vnum)
			return bool(name)
		except:
			return False


def default_tooltip_index():
	if hasattr(app, "RENDER_TARGET_INDEX_TOOLTIP_PREVIEW"):
		return app.RENDER_TARGET_INDEX_TOOLTIP_PREVIEW
	if hasattr(app, "RENDER_TARGET_INDEX_MYSHOPDECO"):
		return app.RENDER_TARGET_INDEX_MYSHOPDECO
	if hasattr(app, "RENDER_TARGET_INDEX_ILLUSTRATED"):
		return app.RENDER_TARGET_INDEX_ILLUSTRATED
	return 0


def default_shared_window_index():
	# Shared windows should avoid tooltip index to prevent UI collisions.
	if hasattr(app, "RENDER_TARGET_INDEX_MYSHOPDECO"):
		return app.RENDER_TARGET_INDEX_MYSHOPDECO
	if hasattr(app, "RENDER_TARGET_INDEX_ILLUSTRATED"):
		return app.RENDER_TARGET_INDEX_ILLUSTRATED
	if hasattr(app, "RENDER_TARGET_INDEX_TOOLTIP_PREVIEW"):
		return app.RENDER_TARGET_INDEX_TOOLTIP_PREVIEW
	return 0


def make_tooltip_controller():
	return ModelPreviewController(default_tooltip_index())
