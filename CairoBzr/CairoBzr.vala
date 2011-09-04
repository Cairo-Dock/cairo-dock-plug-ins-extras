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

/// See README for informations on this plug-in


using GLib;
using CairoDock.Applet;
using Gee; // HashMap

const uint CAIROBZR_ICON_STRING_LENGTH = 4;


/// List of actions defined in this plug-in.
/// The config options "dev left click" and "dev middle click" must match with this list.
public enum CDCairoBzrAction {
	NONE,
	SHOW_DIFF,
	SHOW_VERSIONS,
	TOGGLE_TARGET,
	TOGGLE_USER_MODE,
	TOGGLE_RELOAD_ACTION,
	SET_PLUGIN_NAME,
	GENERATE_REPORT, // TODO
	BUILD_TARGET,
	BUILD_ONE,
	BUILD_CORE,
	BUILD_PLUG_INS,
	BUILD_ALL,
	DOWNLOAD_CORE,
	DOWNLOAD_PLUGINS,
	DOWNLOAD_ALL,
	UPDATE_ALL
}


/// Must match with the config options "tester left click" and "tester middle click".
const CDCairoBzrAction[] CAIROBZR_CLICK_TESTER = {
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.SHOW_VERSIONS,
	CDCairoBzrAction.DOWNLOAD_ALL,
	CDCairoBzrAction.BUILD_ALL,
	CDCairoBzrAction.UPDATE_ALL
};


/// Must match with the config option "dev mouse wheel".
const CDCairoBzrAction[] CAIROBZR_WHEEL_DEV = {
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.TOGGLE_TARGET
};


/// Actions available in developer menu.
const CDCairoBzrAction[] CAIROBZR_MENU_DEV = {
	CDCairoBzrAction.TOGGLE_TARGET,
	CDCairoBzrAction.SET_PLUGIN_NAME,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.SHOW_DIFF,
	CDCairoBzrAction.SHOW_VERSIONS,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.BUILD_ONE,
	CDCairoBzrAction.BUILD_CORE,
	CDCairoBzrAction.BUILD_PLUG_INS,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.DOWNLOAD_CORE,
	CDCairoBzrAction.DOWNLOAD_PLUGINS,
	CDCairoBzrAction.DOWNLOAD_ALL,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.UPDATE_ALL,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.TOGGLE_RELOAD_ACTION,
	CDCairoBzrAction.TOGGLE_USER_MODE
};


/// Actions available in tester menu.
const CDCairoBzrAction[] CAIROBZR_MENU_TESTER = {
	CDCairoBzrAction.SHOW_VERSIONS,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.UPDATE_ALL,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.DOWNLOAD_ALL,
	CDCairoBzrAction.BUILD_ALL,
	CDCairoBzrAction.NONE,
	CDCairoBzrAction.TOGGLE_USER_MODE
};



public struct CairoBzrConfig {
	protected bool bDevMode; /// false = tester / true = developer
	protected bool bTarget; /// false = core / true = plug-in(s)
	protected bool bReload; /// true if the reload action should be triggered after build
	protected CDCairoBzrAction iTesterActionLeftClick;
	protected CDCairoBzrAction iTesterActionMiddleClick;
	protected CDCairoBzrAction iDevActionLeftClick;
	protected CDCairoBzrAction iDevActionMiddleClick;
	protected CDCairoBzrAction iDevActionMouseWheel;
//~ 	private CDCairoBzrAction iActionOnDragAndDrop;
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
		action_add(CDCairoBzrAction.NONE, launch_none, "", "", 2);
		action_add(CDCairoBzrAction.SHOW_DIFF, launch_show_diff, "Show Diff", "gtk-justify-fill");
		action_add(CDCairoBzrAction.SHOW_VERSIONS, launch_show_versions, "Show Versions", "gtk-network", 0, true);
		action_add(CDCairoBzrAction.TOGGLE_TARGET, launch_toggle_target, "", "gtk-refresh");
		action_add(CDCairoBzrAction.TOGGLE_USER_MODE, launch_toggle_user_mode, "Use developer mode", "", 3);
		action_add(CDCairoBzrAction.TOGGLE_RELOAD_ACTION, launch_toggle_reload_action, "Reload after build", "", 3);
		action_add(CDCairoBzrAction.SET_PLUGIN_NAME, launch_set_plugin_name, "Set plug-in name", "gtk-refresh");
action_add(CDCairoBzrAction.GENERATE_REPORT, launch_none, "", "gtk-refresh");
		action_add(CDCairoBzrAction.BUILD_TARGET, launch_build_target, "", "gtk-media-play");
		action_add(CDCairoBzrAction.BUILD_ONE, launch_build_one_plugin, "", "gtk-media-play", 0, true);
		action_add(CDCairoBzrAction.BUILD_CORE, launch_build_core, "Build Core", "gtk-media-forward", 0, true);
		action_add(CDCairoBzrAction.BUILD_PLUG_INS, launch_build_plugins, "Build Plug-Ins", "gtk-media-next", 0, true);
		action_add(CDCairoBzrAction.BUILD_ALL, launch_build_all, "Build All", "gtk-media-next", 0, true);
		action_add(CDCairoBzrAction.DOWNLOAD_CORE, launch_download_core, "Download Core", "gtk-network", 0, true);
		action_add(CDCairoBzrAction.DOWNLOAD_PLUGINS, launch_download_plugins, "Download Plug-Ins", "gtk-network", 0, true);
		action_add(CDCairoBzrAction.DOWNLOAD_ALL, launch_download_all, "Download All", "gtk-network", 0, true);
		action_add(CDCairoBzrAction.UPDATE_ALL, launch_update_all, "Update All", "gtk-network", 0, true);

		this.action_get (CDCairoBzrAction.TOGGLE_USER_MODE).set_checkbox_reference (&this.config.bDevMode);
		this.action_get (CDCairoBzrAction.TOGGLE_RELOAD_ACTION).set_checkbox_reference (&this.config.bReload);
	}



	/***  BASIC ACTIONS CALLS  ***/

	public void launch_none () {}

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
		action_launch (this.config.bTarget ? CDCairoBzrAction.BUILD_ONE : CDCairoBzrAction.BUILD_CORE);
	}



	/***  THREADED ACTIONS CALLS  ***/

	private void launch_show_versions () {
		string sLogCore = compile_bzr_log (this.config.sFolderCore, "lp:cairo-dock-core");
		string sLogPlugIns = compile_bzr_log (this.config.sFolderPlugIns, "lp:cairo-dock-plug-ins");
		try { this.icon.ShowDialog("Core : %s\nPlug-ins : %s".printf(sLogCore, sLogPlugIns), 60); }
		catch (Error e) {}
		set_emblem_none ();
	}


	public void launch_build_one_plugin () {
		string sCompileDirectory = this.config.sFolderPlugIns + "/build/" + this.config.sBuildPlugInName;
		string sError;
		print("[CairoBzr] Build plugin : %s\n", this.config.sBuildPlugInName);
		string[] argv = { directory_scripts () + this.config.sBuildScriptPlugIn };
		if (this.config.bReload)
			argv += this.config.sBuildPlugInName;
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
		this.action_get (CDCairoBzrAction.TOGGLE_TARGET).set_label ("Target : " + sName);
		this.action_get (CDCairoBzrAction.BUILD_TARGET).set_label ("Build " + sName);
		this.action_get (CDCairoBzrAction.BUILD_ONE).set_label ("Build " + this.config.sBuildPlugInName);
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
			print(sError + "\n");
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
			print(sOutout + "\n");
		if (sError.length > 0)
			print(sError + "\n");
		return iExitStatus > 0 ? false : true;
	}


	private string compile_bzr_log (string sDirectory, string sBranch){
		if (!(sDirectory.length > 0)) return "";
		int iLocalVersion = 0, iDistVersion = 0;
		string sLog = "";
		
		int iExitStatus;
		string sOutput;
		string[] argv = { "/usr/bin/bzr", "revno" };
		this.spawn_sync (sDirectory, argv, out sOutput, null, out iExitStatus);
		if (iExitStatus == 0) {
			iLocalVersion = int.parse(sOutput);
			argv += sBranch;
			this.spawn_sync (sDirectory, argv, out sOutput, null, out iExitStatus);
			if (iExitStatus == 0) {
				iDistVersion = int.parse(sOutput);
				int iDelta = iDistVersion - iLocalVersion;
				if (iDelta > 0) {
					argv[1] = "log";
					argv += "-l%d".printf(iDelta);
					argv += "--line";
					this.spawn_sync (sDirectory, argv, out sLog, null, null);
					if (sLog.length > 0) sLog = "\n" + sLog;
				}
			}
		}
		return "%d / %d%s\n".printf (iLocalVersion, iDistVersion, sLog);
	}



	/***  MAIN ICON CALLBACKS  ***/

	public override void on_click (int iState) {
		action_launch (this.config.bDevMode ? this.config.iDevActionLeftClick : CAIROBZR_CLICK_TESTER[this.config.iTesterActionLeftClick]);
	}
	
	public override void on_middle_click () {
		action_launch (this.config.bDevMode ? this.config.iDevActionMiddleClick : CAIROBZR_CLICK_TESTER[this.config.iTesterActionMiddleClick]);
	}

	public override void on_scroll (bool bScrollUp) { 
		if (this.config.bDevMode)
			action_launch (CAIROBZR_WHEEL_DEV[this.config.iDevActionMouseWheel]);
	}

	public override void on_menu_select (int iNumEntry) {
		action_launch (this.config.bDevMode ? CAIROBZR_MENU_DEV[iNumEntry] : CAIROBZR_MENU_TESTER[iNumEntry]);
		}

	public override void on_build_menu () {
		build_menu ( this.config.bDevMode ? (CDCairoBzrAction[]) CAIROBZR_MENU_DEV : (CDCairoBzrAction[]) CAIROBZR_MENU_TESTER );
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
			this.config.iTesterActionLeftClick = (CDCairoBzrAction) keyfile.get_integer("Configuration", "tester left click");
			this.config.iTesterActionMiddleClick = (CDCairoBzrAction) keyfile.get_integer("Configuration", "tester middle click");
			this.config.iDevActionLeftClick = (CDCairoBzrAction) keyfile.get_integer("Developer", "dev left click");
			this.config.iDevActionMiddleClick = (CDCairoBzrAction) keyfile.get_integer("Developer", "dev middle click");
			this.config.iDevActionMouseWheel = (CDCairoBzrAction) keyfile.get_integer("Developer", "dev mouse wheel");
		}
		catch (Error e) {
			print ("[CairoBzr] Error when trying to load configuration data : %s\n", e.message);
		}
	}


	public override void begin () {
		Process.spawn_command_line_sync ("pwd", out this.sAppletDirectory); // SpawnError
		this.sAppletDirectory = this.sAppletDirectory.substring (0, this.sAppletDirectory.length - 1);
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
	protected HashMap<CDCairoBzrAction, CairoAction> lActions;
	protected string sAppletDirectory;


	public CDAppletVala (string[] argv) { base(argv); }


	protected void actions_init () {
		this.lActions = new HashMap<CDCairoBzrAction, CairoAction> ();
	}

	protected void action_add (CDCairoBzrAction iAction, DelegateType pFunction, string sName, string sIcon, int iIconType = 0, bool bUseThread = false) {
		this.lActions[iAction] = new CairoAction (pFunction, sName, sIcon, iIconType, bUseThread);
	}


	public CairoAction action_get (CDCairoBzrAction iAction) {
		return this.lActions[iAction];
	}


	public void action_launch (CDCairoBzrAction iAction) {
		var pAction = action_get (iAction);
		var pFunction = pAction.function ();
		if (pAction.use_thread ()) {
      set_emblem_busy ();
			try { Thread.create<void> ((ThreadFunc) pFunction, false); }
			catch (ThreadError e) {}
		}
		else
			pFunction ();
	}


	public void set_emblem_busy () {
		try { this.icon.SetEmblem (this.sAppletDirectory + "/icons/emblem-important.svg", 3); }
		catch (Error e) {}
	}

	public void set_emblem_none () {
		try { this.icon.SetEmblem ("", 3); }
		catch (Error e) {}
	}


	protected void build_menu (CDCairoBzrAction[] pMenu) {
		HashTable<string,Variant>[] pItems = {};
		CDCairoBzrAction iActionType;
		CairoAction pAction;
		HashTable<string,Variant?>  pItem;
		for (int a = 0; a < pMenu.length; a++) {
			iActionType = pMenu[a];
			pAction = action_get (iActionType);
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
	private DelegateType pFunction;
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


//~ 	public string label ()          { return this.sLabel; }
//~ 	public string icon ()           { return this.sIcon; }
	public DelegateType function () { return this.pFunction; }
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

