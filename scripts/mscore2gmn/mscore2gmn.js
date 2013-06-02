//=============================================================================
//MuseScore
//Linux Music Score Editor
//$Id:$

//Test plugin

//Copyright (C)2008 Werner Schweer and others

//This program is free software; you can redistribute it and/or modify
//it under the terms of the GNU General Public License version 2.

//This program is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.

//You should have received a copy of the GNU General Public License
//along with this program; if not, write to the Free Software
//Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
//=============================================================================

//This is ECMAScript code (ECMA-262 aka "Java Script")

var noteNames = new Array("f", "c", "g", "d", "a", "e", "b");

function tpc2gmn(tpc) {
	var result = "";
	if (tpc < 6) result += noteNames[tpc + 1] + "&&";
	else if (tpc < 13) result += noteNames[tpc - 6] + "&";
	else if (tpc < 20) result += noteNames[tpc - 13];
	else if (tpc < 27) result += noteNames[tpc - 20] + "#";
	else result += noteNames[tpc - 27] + "##";

	return result;
}

function index2octave(index) {
	return (Math.floor(index / 12) - 4);
}

function num2measure(num) {
	result = "/";
	switch (num) {
	case 30:
		result += "64";
		break;
	case 45:
		result += "64.";
		break;
	case 60:
		result += "32";
		break;
	case 90:
		result += "32.";
		break;
	case 96:
		result += "20";
		break;
	case 105:
		result += "32..";
		break;
	case 120:
		result += "16";
		break;
	case 160:
		result += "12";
		break;
	case 180:
		result += "16.";
		break;
	case 192:
		result += "10";
		break;
	case 210:
		result += "16..";
		break;
	case 225:
		result += "16...";
		break;
	case 240:
		result += "8";
		break;
	case 320:
		result += "6";
		break;
	case 360:
		result += "8.";
		break;
	case 384:
		result += "5";
		break;
	case 420:
		result += "8..";
		break;
	case 450:
		result += "8...";
		break;
	case 480:
		result += "4";
		break;
	case 720:
		result += "4.";
		break;
	case 840:
		result += "4..";
		break;
	case 900:
		result += "4...";
		break;
	case 960:
		result += "2";
		break;
	case 1440:
		result += "2.";
		break;
	case 1680:
		result += "2..";
		break;
	case 1800:
		result += "2...";
		break;
	case 1920:
		result += "1";
		break;
	case 2880:
		result += "1.";
		break;
	default:
	{
		if (num % 1920 == 0) result = "*" + num / 1920 + "/1";
		else if (num % 960 == 0) result = "*" + num / 960 + "/2";
		else if (num % 480 == 0) result = "*" + num / 480 + "/4";
		else if (num % 240 == 0) result = "*" + num / 240 + "/8";
		else if (num % 120 == 0) result = "*" + num / 120 + "/16";
		else if (num % 60 == 0) result = "*" + num / 60 + "/32";
		else result = "!!!" + num + "!!!";

		break;
	}
	}
	return result;
}

//---------------------------------------------------------
//init
//this function will be called on startup of mscore
//---------------------------------------------------------

function init() {
	print("test script init");
}

//-------------------------------------------------------------------
//run
//this function will be called when activating the
//plugin menu entry

//global Variables:
//pluginPath - contains the plugin path; file separator is "/"
//-------------------------------------------------------------------

//Setup some global variables
var pluginName = "mscore2gmn";

function run() {
	var dirString = QFileDialog.getExistingDirectory(this, pluginName + ": Select Folder", "", 0);
	if (!dirString) {
		QMessageBox.warning(this, pluginName, qsTr("No folder selected"));
		return;
	}

	var traverse = false;
	var origDir = new QDir(dirString);
	var scoreList = work(dirString, traverse, origDir);
	if (scoreList == "") scoreList = qsTr("\n\nAll files are up to date\n");
	else scoreList = qsTr("\n\nFile(s) exported:\n\n%1").arg(scoreList);
	QMessageBox.information(this, pluginName, dirString + scoreList);
}

function work(dirString, traverse, origDir) {
	var dir = new QDir(dirString);
	var dirIt = new QDirIterator(dir);
	var scoreList = "";

	while (dirIt.hasNext()) {
		var file = dirIt.next();
		if (dirIt.fileInfo().isDir()) {
			if (file.match("\./..$") || file.match("\./.$")) continue;
			if (traverse) scoreList += work(file, traverse, origDir);
		} else {
			if (file.match("\." + ".mscz" + "$")) {
				scoreList += process_one(file, origDir);
			}
		}
	}

	return scoreList;
}

function timesigtype2gmn(type) {
	var denominator = type % 64
	var numerator = (type-denominator) / 64;

	return (numerator + "/" + denominator);
}

function process_one(file, origDir) {
	var outputFileName = file.replace(".mscz", ".gmn");
	var outputFile = new QFile(outputFileName, 3);
	if (outputFile.open(QIODevice.WriteOnly)) {
		print("Datei geöffnet");
		var score = new Score();
		if (score.load(file)) {
			var ts = new QTextStream(outputFile);

			var composerGmn = "\\composer<\"" + score.composer + "\">";
			var titleGmn = "\\title<\"" + score.title + "\">";
			var meterGmn = "\\meter<\"" + timesigtype2gmn(score.timesig.type) + "\">";
			var keyGmn = "\\key<" + score.keysig + ">";

			var cursor = new Cursor(score);

			ts.writeString("{\n");
			for (var iStaff = 0; iStaff < score.staves; iStaff++) {

				ts.writeString("[");

				if (iStaff == 0) {
					ts.writeString(composerGmn);
					ts.writeString(titleGmn);                	
				}
				
				ts.writeString(meterGmn);
				ts.writeString(keyGmn);

				cursor.staff = iStaff;
				cursor.voice = 0;

				cursor.rewind(); // set cursor to first chord/rest
				var tickLenOld = 0; // set starting length unrealistic
				var octaveOld = -100; // set starting octave unrealistic
				while (!cursor.eos()) {
					var tick = cursor.tick();
					if (cursor.isChord()) {
						var chord = cursor.chord();
						var tickLen = chord.tickLen;
						var noteStrings = new Array();

						if (chord.topNote().tied == 1) {
							do {
								do {
									cursor.next();
								} while (cursor.isChord() == false);
								chord = cursor.chord();
								tickLen += chord.tickLen;
							} while (chord.topNote().tied != 2);
						}

						for (var iNote = 0; iNote < chord.notes; iNote++) {
							var note = chord.note(iNote);
							var localString = "";
							localString += tpc2gmn(note.tpc);
							var octave = index2octave(note.pitch);
							if (octave != octaveOld) {
								localString += octave;
								octaveOld = octave;
							}

							if (tickLen != tickLenOld) {
								localString += num2measure(tickLen);
								tickLenOld = tickLen
							}

							noteStrings.push(localString);
						}

						if (noteStrings.length > 1) ts.writeString("{" + noteStrings.join(",") + "} ");
						else ts.writeString(noteStrings.toString() + " ");

					} else if (cursor.isRest()) {
						var rest = cursor.rest();
						var tickLen = rest.tickLen;
						ts.writeString("_" + num2measure(tickLen) + " ");

					}
					cursor.next();
				}
				if (iStaff < score.staves-1) {
					ts.writeString("], \n");
				} else {
					ts.writeString("]\n");
				}
			}
			ts.writeString("}");
			ts.flush();
			outputFile.close();
			print("Datei geschlossen")
		}
		score.close();
	} else {
		print("Dateifehler!");
	}
	return file;
}

//---------------------------------------------------------
//menu:  defines were the function will be placed
//in the MuseScore menu structure
//---------------------------------------------------------

var mscorePlugin = {
		menu: 'Plugins.Guido Music Notation',
		init: init,
		run: run
};

mscorePlugin;
