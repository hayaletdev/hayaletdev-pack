import app
import player
import dbg

# Compatibility wrapper for RenderTarget-style scripts.
# Index 0 -> Illustration (player preview), Index 1 -> MyShopDeco (mob/object preview).

def _is_myshop_index(index):
	return hasattr(app, "RENDER_TARGET_INDEX_MYSHOPDECO") and index == app.RENDER_TARGET_INDEX_MYSHOPDECO


def SetBackground(index, path):
	return


def SetVisibility(index, isVisible):
	if _is_myshop_index(index):
		if hasattr(player, "MyShopDecoShow"):
			player.MyShopDecoShow(bool(isVisible))
	else:
		player.IllustrationShow(bool(isVisible))


def SelectModel(index, vnum):
	if _is_myshop_index(index):
		if hasattr(player, "SelectShopModel"):
			player.SelectShopModel(vnum)
		else:
			dbg.TraceError("RenderTarget SelectShopModel missing: %d" % vnum)
		return

	if not player.IllustrationSelectModel(vnum):
		dbg.TraceError("RenderTarget SelectModel failed: %d" % vnum)
		return

	# Reset all wearable layers so previous preview state does not leak.
	player.IllustrationChangeArmor(0)
	player.IllustrationChangeWeapon(0)
	player.IllustrationChangeHair(0)
	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		player.IllustrationChangeAcce(0)


def SetHair(index, vnum):
	if not _is_myshop_index(index):
		player.IllustrationChangeHair(vnum)


def SetArmor(index, vnum):
	if not _is_myshop_index(index):
		player.IllustrationChangeArmor(vnum)


def SetWeapon(index, vnum):
	if not _is_myshop_index(index):
		player.IllustrationChangeWeapon(vnum)


def SetAcce(index, vnum):
	if not _is_myshop_index(index) and app.ENABLE_ACCE_COSTUME_SYSTEM:
		player.IllustrationChangeAcce(vnum)


def SetEffect(index):
	if _is_myshop_index(index):
		if hasattr(player, "MyShopDecoChangeEffect"):
			player.MyShopDecoChangeEffect()
	else:
		player.IllustrationChangeEffect()
