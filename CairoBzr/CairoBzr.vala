/* This is a part of the external demo applet for Cairo-Dock

Copyright : (C) 2010-2011 by SQP
E-mail : 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
http://www.gnu.org/licenses/licenses.html#GPL */

/// See README.txt for informations on this plug-in


using GLib;
using CairoDock.Applet;

const uint CAIROBZR_ICON_STRING_LENGTH = 4;


/// Must match with the config options "tester left click" and "tester middle click".
const string[] CAIROBZR_CLICK_TESTER = {
	"NONE",
	"CairoBzr.SHOW_VERSIONS",
	"CairoBzr.DOWNLOAD_ALL",
	"CairoBzr.BUILD_ALL",
	"CairoBzr.UPDATE_ALL"
};


/// Must match with the config options "dev left click" and "dev middle click".
const string[] CAIROBZR_CLICK_DEV = {
	"NONE",
	"CairoBzr.SHOW_DIFF",
	"CairoBzr.SHOW_VERSIONS",
	"CairoBzr.TOGGLE_TARGET",
	"CairoBzr.TOGGLE_USER_MODE",
	"CairoBzr.TOGGLE_RELOAD_ACTION",
	"CairoBzr.SET_PLUGIN_NAME",
	"CairoBzr.GENERATE_REPORT", // TODO
	"CairoBzr.BUILD_TARGET",
	"CairoBzr.BUILD_ONE",
	"CairoBzr.BUILD_CORE",
	"CairoBzr.BUILD_PLUG_INS",
	"CairoBzr.BUILD_ALL",
	"CairoBzr.DOWNLOAD_CORE",
	"CairoBzr.DOWNLOAD_PLUGINS",
	"CairoBzr.DOWNLOAD_ALL",
	"CairoBzr.UPDATE_ALL"
};


/// Must match with the config option "dev mouse wheel".
const string[] CAIROBZR_WHEEL_DEV = {
	"NONE",
	"CairoBzr.TOGGLE_TARGET"
};


/// Actions available in developer menu.
const string[] CAIROBZR_MENU_DEV = {
	"CairoBzr.TOGGLE_TARGET",
	"CairoBzr.SET_PLUGIN_NAME",
	"NONE",
	"CairoBzr.SHOW_DIFF",
	"CairoBzr.SHOW_VERSIONS",
	"NONE",
	"CairoBzr.BUILD_ONE",
	"CairoBzr.BUILD_CORE",
	"CairoBzr.BUILD_PLUG_INS",
	"NONE",
	"CairoBzr.DOWNLOAD_CORE",
	"CairoBzr.DOWNLOAD_PLUGINS",
	"CairoBzr.DOWNLOAD_ALL",
	"NONE",
	"CairoBzr.UPDATE_ALL",
	"NONE",
	"CairoBzr.TOGGLE_RELOAD_ACTION",
	"CairoBzr.TOGGLE_USER_MODE"
};


/// Actions available in tester menu.
const string[] CAIROBZR_MENU_TESTER = {
	"CairoBzr.SHOW_VERSIONS",
	"NONE",
	"CairoBzr.UPDATE_ALL",
	"NONE",
	"CairoBzr.DOWNLOAD_ALL",
	"CairoBzr.BUILD_ALL",
	"NONE",
	"CairoBzr.TOGGLE_USER_MODE"
};



public struct CairoBzrConfig {
	protected bool bDevMode; /// false = tester / true = developer
	protected bool bTarget; /// false = core / true = plug-in(s)
	protected bool bReload; /// true if the reload action should be triggered after build
	protected int iTesterActionLeftClick;
	protected int iTesterActionMiddleClick;
	protected int iDevActionLeftClick;
	protected int iDevActionMiddleClick;
	protected int iDevActionMouseWheel;
//~ 	private int iActionOnDragAndDrop;
	protected string sBuildScriptMain;
	protected string sBuildScriptPlugIn;
	protected string sDiffCommand;

	protected string sFolderCore;
	protected string sFolderPlugIns;
	protected string sBuildPlugInName;
}



public class CairoBzr : CDAppletVala {
	public CairoBzr (string[] argv) { base(argv); }


	/***  ACTIONS DEFINITION  ***/

	private void actions_load () {
		actions_init ();
		action_add("CairoBzr.SHOW_DIFF", launch_show_diff, "Show Diff", "gtk-justify-fill");
		action_add("CairoBzr.SHOW_VERSIONS", launch_show_versions, "Show Versions", "gtk-network", 0, true);
		action_add("CairoBzr.TOGGLE_TARGET", launch_toggle_target, "", "gtk-refresh");
		action_add("CairoBzr.TOGGLE_USER_MODE", launch_toggle_user_mode, "Use developer mode", "", 3);
		action_add("CairoBzr.TOGGLE_RELOAD_ACTION", launch_toggle_reload_action, "Reload after build", "", 3);
		action_add("CairoBzr.SET_PLUGIN_NAME", launch_set_plugin_name, "Set plug-in name", "gtk-refresh");
action_add("CairoBzr.GENERATE_REPORT", action_none, "", "gtk-refresh");
		action_add("CairoBzr.BUILD_TARGET", launch_build_target, "", "gtk-media-play");
		action_add("CairoBzr.BUILD_ONE", launch_build_one_plugin, "", "gtk-media-play", 0, true);
		action_add("CairoBzr.BUILD_CORE", launch_build_core, "Build Core", "gtk-media-forward", 0, true);
		action_add("CairoBzr.BUILD_PLUG_INS", launch_build_plugins, "Build Plug-Ins", "gtk-media-next", 0, true);
		action_add("CairoBzr.BUILD_ALL", launch_build_all, "Build All", "gtk-media-next", 0, true);
		action_add("CairoBzr.DOWNLOAD_CORE", launch_download_core, "Download Core", "gtk-network", 0, true);
		action_add("CairoBzr.DOWNLOAD_PLUGINS", launch_download_plugins, "Download Plug-Ins", "gtk-network", 0, true);
		action_add("CairoBzr.DOWNLOAD_ALL", launch_download_all, "Download All", "gtk-network", 0, true);
		action_add("CairoBzr.UPDATE_ALL", launch_update_all, "Update All", "gtk-execute", 0, true);

		this.action_get ("CairoBzr.TOGGLE_USER_MODE").set_checkbox_reference (&this.config.bDevMode);
		this.action_get ("CairoBzr.TOGGLE_RELOAD_ACTION").set_checkbox_reference (&this.config.bReload);
	}



	/***  BASIC ACTIONS CALLS  ***/

	private void launch_show_diff () {
		string[] argv = { this.config.sDiffCommand, "." };
		this.spawn_async (this.config.bTarget ? this.config.sFolderPlugIns : this.config.sFolderCore, argv);
	}


	private void launch_toggle_target () {
		this.config.bTarget = this.config.bTarget == true ? false : true;
		set_target ();
	}


	private void launch_toggle_user_mode () {
		this.config.bDevMode = this.config.bDevMode == true ? false : true;
		set_icon_info ();
	}


	private void launch_toggle_reload_action () {
		this.config.bReload = this.config.bReload == true ? false : true;
	}


	private void launch_set_plugin_name () {
		var dialog_attributes = new HashTable<string,Variant>(str_hash, str_equal);
		dialog_attributes.insert ("icon", "stock_properties");
		dialog_attributes.insert ("message", "Set build plugin name");
		dialog_attributes.insert ("buttons", "ok;cancel");
		var widget_attributes = new HashTable<string,Variant>(str_hash, str_equal);
		widget_attributes.insert ("widget-type", "text-entry");
		widget_attributes.insert ("editable", true);
		try { this.icon.PopupDialog (dialog_attributes, widget_attributes); }
		catch (Error e) {}
	}


	public void launch_build_target () {
		action_launch (this.config.bTarget ? "CairoBzr.BUILD_ONE" : "CairoBzr.BUILD_CORE");
	}



	/***  THREADED ACTIONS CALLS  ***/

	private void launch_show_versions () {
		string sLogCore = compile_bzr_log (this.config.sFolderCore, "lp:cairo-dock-core");
		string sLogPlugIns = compile_bzr_log (this.config.sFolderPlugIns, "lp:cairo-dock-plug-ins");
		string sMessage = "<b><u>Core</u></b> : %s\n<b><u>Plug-ins</u></b> : %s".printf (sLogCore, sLogPlugIns);
		var dialog_attributes = popup_dialog_attribute ("cairo-dock", sMessage, "cancel", true);
		try { this.icon.PopupDialog (dialog_attributes, popup_widget_attribute_empty ()); }
		catch (Error e) {}
		set_emblem_none ();
	}


	public void launch_build_one_plugin () {
		if (!(this.config.sFolderPlugIns.length > 0)) return;
		string sCompileDirectory = this.config.sFolderPlugIns + "/build/" + this.config.sBuildPlugInName;
		string sError;
		print("[CairoBzr] Build plugin : %s\n", this.config.sBuildPlugInName);
		string[] argv = { directory_scripts () + this.config.sBuildScriptPlugIn };

		if (this.config.bReload)
			try {
				var regex = new Regex ("-");
				argv += regex.replace (this.config.sBuildPlugInName, -1, 0, " ");
			} catch (RegexError e) {}
//~ 		this.spawn_async(sCompileDirectory, argv);
		this.spawn_sync(sCompileDirectory, argv, null, out sError);
		if (sError.length > 0)
			print(sError + "\n");
		set_emblem_none ();
	}


	public void launch_build_core ()    {
		build_main (this.config.sFolderCore, this.config.bReload);
		set_emblem_none ();
	}


	public void launch_build_plugins ()    {
		build_main (this.config.sFolderPlugIns, this.config.bReload);
		set_emblem_none ();
	}


	public void launch_build_all () {
		if (build_main (this.config.sFolderCore, false))
			build_main (this.config.sFolderPlugIns, !this.config.bDevMode || this.config.bReload);
		set_emblem_none ();
	}


	public void launch_download_core () {
		download_main (this.config.sFolderCore);
		set_emblem_none ();
	}


	public void launch_download_plugins () {
		download_main (this.config.sFolderPlugIns);
		set_emblem_none ();
	}


	public void launch_download_all () {
		if (download_main (this.config.sFolderCore))
			download_main (this.config.sFolderPlugIns);
		set_emblem_none ();
	}


	public void launch_update_all () {
		if (download_main (this.config.sFolderCore) && download_main (this.config.sFolderPlugIns) && build_main (this.config.sFolderCore, false))
			build_main (this.config.sFolderPlugIns, !this.config.bDevMode || this.config.bReload);
		set_emblem_none ();
	}



	/***  PRIVATE METHODS  ***/

	private string directory_scripts () {
		return this.sAppletDirectory + "/scripts/";
	}


	private void set_target (string sText = "") {
		if (sText.length > 0)
			this.config.sBuildPlugInName = sText;
		string sName = this.config.bTarget ? this.config.sBuildPlugInName : "core";
		this.action_get ("CairoBzr.TOGGLE_TARGET").set_label ("Target : " + sName);
		this.action_get ("CairoBzr.BUILD_TARGET").set_label ("Build " + sName);
		this.action_get ("CairoBzr.BUILD_ONE").set_label ("Build " + this.config.sBuildPlugInName);
		set_icon_info ();
	}


	private void set_icon_info () {
		string sTextInfo = "";
		if (this.config.bDevMode) {
			if (this.config.bTarget)
				sTextInfo = this.config.sBuildPlugInName.length <= CAIROBZR_ICON_STRING_LENGTH ? this.config.sBuildPlugInName : this.config.sBuildPlugInName.substring (0, CAIROBZR_ICON_STRING_LENGTH);
			else
				sTextInfo = "Core";
		}
		try { this.icon.SetQuickInfo(sTextInfo); }
		catch (Error e) {}
	}


	public void set_icon () {
		try { this.icon.SetIcon (this.sAppletDirectory + "/icon"); }
		catch (Error e) {}
	}


	private bool build_main (string sDirectory, bool bCanReload = true) {
		if (!(sDirectory.length > 0)) return false;
		int iExitStatus;
		string sError;
		string[] argv = { directory_scripts () + this.config.sBuildScriptMain };
		if (bCanReload)
			argv += "-r";
		print("[CairoBzr] Build main : %s\n", sDirectory);
		this.spawn_sync(sDirectory, argv, null, out sError, out iExitStatus);
		if (sError.length > 0)
			print (sError + "\n");
		return iExitStatus > 0 ? false : true;
	}


	private bool download_main (string sDirectory) {
		if (!(sDirectory.length > 0)) return false;
		int iExitStatus;
		string sError, sOutout;
		string[] argv = { "/usr/bin/bzr", "pull" };
		print("[CairoBzr] Download main : %s\n", sDirectory);
		this.spawn_sync(sDirectory, argv, out sOutout, out sError, out iExitStatus);
		if (sOutout.length > 0)
			print (sOutout + "\n");
		if (sError.length > 0)
			print(sError + "\n");
		return iExitStatus > 0 ? false : true;
	}


	private string compile_bzr_log (string sDirectory, string sBranch){
		if (!(sDirectory.length > 0)) return "";
		int iLocalVersion = 0, iDistVersion = 0;
		
		int iExitStatus;
		string sOutput;
		string[] argv = { "/usr/bin/bzr", "revno" };
		this.spawn_sync (sDirectory, argv, out sOutput, null, out iExitStatus);
		if (iExitStatus == 0) {
			iLocalVersion = int.parse (sOutput);
			argv += sBranch;
			this.spawn_sync (sDirectory, argv, out sOutput, null, out iExitStatus);
			if (iExitStatus == 0) {
				iDistVersion = int.parse (sOutput);
				int iDelta = iDistVersion - iLocalVersion;
				if (iDelta > 0) {
					argv[1] = "log";
					argv += "-l%d".printf (iDelta);
					argv += "--short";
					string sLog;
					this.spawn_sync (sDirectory, argv, out sLog);
					if (sLog.length > 0) {
						try {
							var regex = new Regex ("\n\n");
							sLog = regex.replace (sLog, -1, 0, "\n");
						} catch (RegexError e) {}
						sLog = "\n" + sLog;
					}
					return "<b>%d / %d</b>%s".printf (iLocalVersion, iDistVersion, sLog);
				}
				return "Up-to-date (%d)".printf (iLocalVersion);
			}
		}
		return "Unable to fetch versions";
	}



	/***  MAIN ICON CALLBACKS  ***/

	public override void on_click (int iState) {
		action_launch (this.config.bDevMode ? CAIROBZR_CLICK_DEV[this.config.iDevActionLeftClick] : CAIROBZR_CLICK_TESTER[this.config.iTesterActionLeftClick]);
	}
	
	public override void on_middle_click () {
		action_launch (this.config.bDevMode ? CAIROBZR_CLICK_DEV[this.config.iDevActionMiddleClick] : CAIROBZR_CLICK_TESTER[this.config.iTesterActionMiddleClick]);
	}

	public override void on_scroll (bool bScrollUp) { 
		if (this.config.bDevMode)
			action_launch (CAIROBZR_WHEEL_DEV[this.config.iDevActionMouseWheel]);
	}

	public override void on_menu_select (int iNumEntry) {
		action_launch (this.config.bDevMode ? CAIROBZR_MENU_DEV[iNumEntry] : CAIROBZR_MENU_TESTER[iNumEntry]);
		}

	public override void on_build_menu () {
		build_menu ( this.config.bDevMode ? (string[]) CAIROBZR_MENU_DEV : (string[]) CAIROBZR_MENU_TESTER );
	}

	public override void on_answer_dialog (int iButton, Variant answer) {
		set_target ((string) answer);
	}


	/***  APPLET DEFINITION  ***/

	public override void get_config (GLib.KeyFile keyfile) {
		try {
			this.config.bDevMode = keyfile.get_boolean("Configuration", "user_mode");
			this.config.bTarget = keyfile.get_boolean("Developer", "build target");
			this.config.bReload = keyfile.get_boolean("Developer", "trigger reload");

			this.config.sBuildScriptMain = keyfile.get_string("Developer", "build script main");
			this.config.sBuildScriptPlugIn = keyfile.get_string("Developer", "build script plug-in");
			this.config.sFolderCore = keyfile.get_string("Configuration", "folder core");
			this.config.sFolderPlugIns = keyfile.get_string("Configuration", "folder plug-ins");
			this.config.sBuildPlugInName  = keyfile.get_string("Developer", "build plug-in name");
			this.config.sDiffCommand = keyfile.get_string("Developer", "diff gui");
			this.config.iTesterActionLeftClick = keyfile.get_integer("Configuration", "tester left click");
			this.config.iTesterActionMiddleClick = keyfile.get_integer("Configuration", "tester middle click");
			this.config.iDevActionLeftClick = keyfile.get_integer("Developer", "dev left click");
			this.config.iDevActionMiddleClick = keyfile.get_integer("Developer", "dev middle click");
			this.config.iDevActionMouseWheel = keyfile.get_integer("Developer", "dev mouse wheel");
		}
		catch (Error e) {
			print ("[CairoBzr] Error when trying to load configuration data : %s\n", e.message);
		}
	}


	public override void begin () {
		try {
			Process.spawn_command_line_sync ("pwd", out this.sAppletDirectory); // SpawnError
		}
		catch (Error e) {
			print ("[CairoBzr] Error when trying to check applet dir : %s\n", e.message);
		}
		this.sAppletDirectory = this.sAppletDirectory.substring (0, this.sAppletDirectory.length - 1);
		this.sEmblemBusy = "/icons/emblem-important.svg";
		reload ();
	}


	public override void reload () {
		actions_load ();
		set_target ();
	}

	public override void end () {
//~ 		print ("[CairoBzr] applet is stopped\n");
	}

} // End class : CairoBzr



public delegate void DelegateType();

public class CDAppletVala : CDApplet {
	// my config.
	protected CairoBzrConfig config;
	protected HashTable<string, CairoAction> tActions;
	protected string sAppletDirectory;
	protected string sEmblemBusy;


	public CDAppletVala (string[] argv) { base(argv); }


	protected void actions_init () {
		this.tActions = new HashTable<string, CairoAction> (str_hash, str_equal);
		action_add("NONE", action_none, "", "", 2);
	}

	protected void action_add (string sAction, DelegateType pFunction, string sName, string sIcon, int iIconType = 0, bool bUseThread = false) {
		this.tActions.insert (sAction, new CairoAction (pFunction, sName, sIcon, iIconType, bUseThread));
	}


	public CairoAction action_get (string sAction) {
		return this.tActions.lookup (sAction);
	}


	public void action_launch (string sAction) {
		var pAction = action_get (sAction);
		unowned DelegateType pFunction = pAction.function ();
		if (pAction.use_thread ()) {
      set_emblem_busy ();
			try { Thread.create<void> ((ThreadFunc) pFunction, false); }
			catch (ThreadError e) {}
		}
		else
			pFunction ();
	}


	public void action_none () {}


	public void set_emblem_busy () {
		try { this.icon.SetEmblem (this.sAppletDirectory + "/icons/emblem-important.svg", CDApplet.EmblemPosition.EMBLEM_TOP_RIGHT + CDApplet.EmblemModifier.EMBLEM_PERSISTENT); }
		catch (Error e) {}
	}

	public void set_emblem_none () {
		try { this.icon.SetEmblem ("", CDApplet.EmblemPosition.EMBLEM_TOP_RIGHT); }
		catch (Error e) {}
	}


	protected void build_menu (string[] pMenu) {
		HashTable<string,Variant>[] pItems = {};
		string sActionType;
		CairoAction pAction;
		HashTable<string,Variant?>  pItem;
		for (int a = 0; a < pMenu.length; a++) {
			sActionType = pMenu[a];
			pAction = action_get (sActionType);
			switch (pAction.iIconType) {
				case 2: /// Separator
					pItem = pAction.menu_separator ();
					break;
				case 3: /// Checkbox
					pItem = pAction.menu_checkbox (a);
					break;
				default: /// Icon
					pItem = pAction.menu_icon (a);
					break;
			}
			pItems += pItem;
		}
		try { this.icon.AddMenuItems(pItems); }
		catch (Error e) {}
	}


	protected HashTable<string,Variant> popup_dialog_attribute (string sIcon, string sMessage = "", string sButtons = "ok;cancel", bool bUseMarkup = false) {
		var dialog_attributes = new HashTable<string,Variant>(str_hash, str_equal);
		dialog_attributes.insert ("icon", sIcon);
		dialog_attributes.insert ("message", sMessage);
		dialog_attributes.insert ("buttons", sButtons);
		dialog_attributes.insert ("use-markup", bUseMarkup);
		return dialog_attributes;
	}


	protected HashTable<string,Variant> popup_widget_attribute_empty () {
		return new HashTable<string,Variant>(str_hash, str_equal);
	}


	protected void spawn_async (string sDirectory, string[] argv) {
		Pid child_pid;
		try {
			Process.spawn_async (sDirectory, argv, null, 0, null, out child_pid);
		}
		catch (Error e) {
			print ("Could not launch command : %s : %s\n", argv[0], e.message);
		}
	}


	protected void spawn_sync (string sDirectory, string[] argv, out string? sOutput, out string? sError = null, out int? iExitStatus = null) {
		try {
			Process.spawn_sync (sDirectory, argv, null, SpawnFlags.LEAVE_DESCRIPTORS_OPEN + SpawnFlags.CHILD_INHERITS_STDIN, null, out sOutput, out sError, out iExitStatus);
		}
		catch (Error e) {
			print ("Could not launch command : %s : %s\n", argv[0], e.message);
		}
	}

} // End class : CDAppletVala



public class CairoAction {
	private string sIcon;
	private string sLabel;
	private unowned DelegateType pFunction;
	public int iIconType;
	private bool bUseThread;
	private bool* bChecked;

	public CairoAction (DelegateType pFunction, string sLabel = "", string sIcon = "", int iIconType = 0, bool bUseThread = false) {
		this.pFunction = pFunction;
		this.set_label (sLabel);
		this.sIcon = sIcon;
		this.iIconType = iIconType;
		this.bUseThread = bUseThread;
	}


	public HashTable<string,Variant?> menu_separator () {
		var pItem = new HashTable<string,Variant?>(str_hash, str_equal);
		pItem.insert("type", 2);
		return pItem;
	}


	public HashTable<string,Variant?> menu_icon (int iId) {
		var pItem = new HashTable<string,Variant?>(str_hash, str_equal);
		pItem.insert("label", this.sLabel);
		pItem.insert("icon", this.sIcon);
		pItem.insert("id", iId);
		return pItem;
	}


	public HashTable<string,Variant?> menu_checkbox (int iId) {
		var pItem = new HashTable<string,Variant?>(str_hash, str_equal);
		pItem.insert("type", 3);
		pItem.insert("label", this.sLabel);
		pItem.insert("state", *this.bChecked);
		pItem.insert("id", iId);
		return pItem;
	}


	public unowned DelegateType function () { return this.pFunction; }
	public bool use_thread ()       { return this.bUseThread; }

	public void set_label (string sLabel)               { this.sLabel = sLabel; }
	public void set_checkbox_reference (bool* bPointer) { this.bChecked = bPointer; }
	
} // End class : CairoAction



	/***  MAIN  ***/

static int main (string[] argv) {	
	var myApplet = new CairoBzr (argv);
	myApplet.run();
	return 0;
}

