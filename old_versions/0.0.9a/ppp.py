import os
import sys
import configparser
import time
import select
import platform

if os.name == 'nt':  # Windows
    import msvcrt
else:  # Linux und MacOS
    import termios
    import tty

# Global variables
# Colors (to esc.py)
cBlack = 0
cRed = 1
cGreen = 2
cYellow = 3
cBlue = 4
cMagenta = 5
cCyan = 6
cWhite = 7
cbBlack = 8
cbRed = 9
cbGreen = 10
cbYellow = 11
cbBlue = 12
cbMagenta = 13
cbCyan = 14
cbWhite = 15
cBg = 0
cFg = 7

# App
appName = "Powerful Pee & Potence"
appVersion = "0.0.9a"
appAuthor = "github.com/PitWD"
appCopyright = "(c) GPL by"
appDate = "06.05.2025"

# OS
iOS = 0  # iOS special (a-shell)

# Trigger time for ScreenSaver WatchDog
TriggerTime = time.time() 

# Load Values from INI (quick 'n' dirty, slow, case sensitive but type-safe)
def LoadSettings(TrainType = 'Default'):

    global iOS

    # if INIs missing
    NoSettings = False
    NoLanguage = False

    # Define the path to Settings.ini
    config_file_path = os.path.join(os.path.dirname(__file__), 'Settings.ini')

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    # Check if file was read successfully
    if not config.read(config_file_path, encoding='utf-8'):
        NoSettings = True

    # Values from Settings.ini
    iniVal = {
        'Version': config.get('Global', 'Version') if config.has_option('Global', 'Version') else '1.0.0',
        'Debug': config.get('Global', 'Debug') if config.has_option('Global', 'Debug') else '0',
        'StartDelay': config.get('Global', 'StartDelay') if config.has_option('Global', 'StartDelay') else '1',
        'timeBlink': config.get(TrainType, 'Blink') if config.has_option(TrainType, 'Blink') else '60',
        'timeButterfly': config.get(TrainType, 'Butterfly') if config.has_option(TrainType, 'Butterfly') else '10',
        'time10': config.get(TrainType, '10Percent') if config.has_option(TrainType, '10Percent') else '10',
        'time50': config.get(TrainType, '50Percent') if config.has_option(TrainType, '50Percent') else '10',
        'time80': config.get(TrainType, '80Percent') if config.has_option(TrainType, '80Percent') else '10',
        'startSequence': config.get(TrainType, 'Start') if config.has_option(TrainType, 'Start') else 'Bu_Bl',
        'startRepeat': config.get(TrainType, 'RepeatStart') if config.has_option(TrainType, 'RepeatStart') else '2',
        'mainSequence': config.get(TrainType, 'Main') if config.has_option(TrainType, 'Main') else 'Bu_10_50_80_Bu_10_50_80_Bu_Bl',
        'mainRepeat': config.get(TrainType, 'RepeatMain') if config.has_option(TrainType, 'RepeatMain') else '6',
        'endSequence': config.get(TrainType, 'End') if config.has_option(TrainType, 'End') else 'Bu',
        'endRepeat': config.get(TrainType, 'RepeatEnd') if config.has_option(TrainType, 'RepeatEnd') else '1',
        'Language': config.get('Global', 'Language') if config.has_option('Global', 'Language') else '"EN"',
        'Automatic': config.get('Global', 'Automatic') if config.has_option('Global', 'Automatic') else '1',
        'timeAutoDelay': config.get('Global', 'AutoDelayTime') if config.has_option('Global', 'AutoDelayTime') else '3',
        'DoubleHeight': config.get('Global', 'DoubleHeight') if config.has_option('Global', 'DoubleHeight') else '0',
        'SimDoubleHeight': config.get('Global', 'SimDoubleHeight') if config.has_option('Global', 'SimDoubleHeight') else '0',
        'DoubleWidth': config.get('Global', 'DoubleWidth') if config.has_option('Global', 'DoubleWidth') else '0',
        'SimDoubleWidth': config.get('Global', 'SimDoubleWidth') if config.has_option('Global', 'SimDoubleWidth') else '0',
        'Bold': config.get('Global', 'Bold') if config.has_option('Global', 'Bold') else '0',
        'Italic': config.get('Global', 'Italic') if config.has_option('Global', 'Italic') else '0',
        'Underline': config.get('Global', 'Underline') if config.has_option('Global', 'Underline') else '0',
        'iOS': config.get('Global', 'iOS') if config.has_option('Global', 'iOS') else '0',
        'Android': config.get('Global', 'Android') if config.has_option('Global', 'Android') else '0',
        'TriggerScreenSaver': config.get('Global', 'TriggerScreenSaver') if config.has_option('Global', 'TriggerScreenSaver') else '0',
        'TriggerScrTime': config.get('Global', 'TriggerScrTime') if config.has_option('Global', 'TriggerScrTime') else '60',
        'TriggerScrText_X': config.get('Global', 'TriggerScrText_X') if config.has_option('Global', 'TriggerScrText_X') else 'xscreensaver-command -deactivate > /dev/null 2>&1',
        'TriggerScrText_Mac': config.get('Global', 'TriggerScrText_Mac') if config.has_option('Global', 'TriggerScrText_Mac') else 'caffeinate -u -t 90',
        'TriggerScrText_Win': config.get('Global', 'TriggerScrText_Win') if config.has_option('Global', 'TriggerScrText_Win') else '''powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('+')"''',
        'TriggerScrText_Other': config.get('Global', 'TriggerScrText_Other') if config.has_option('Global', 'TriggerScrText_Other') else '',
    }

    # Save default values to Settings.ini
    if NoSettings:
        # Save default values to Settings.ini
        with open(config_file_path, 'w') as configfile:
            config.add_section('Global')
            config.set('Global', 'Version', iniVal['version'])
            config.set('Global', 'Debug', iniVal['debug'])
            config.set('Global', 'StartDelay', iniVal['StartDelay'])
            config.set('Global', 'Language', iniVal['Language'])
            config.set('Global', 'Automatic', iniVal['Automatic'])
            config.set('Global', 'AutoDelayTime', iniVal['timeAutoDelay'])
            config.set('Global', 'DoubleHeight', iniVal['DoubleHeight'])
            config.set('Global', 'SimDoubleHeight', iniVal['SimDoubleHeight'])
            config.set('Global', 'DoubleWidth', iniVal['DoubleWidth'])
            config.set('Global', 'SimDoubleWidth', iniVal['SimDoubleWidth'])
            config.set('Global', 'Bold', iniVal['Bold'])
            config.set('Global', 'Italic', iniVal['Italic'])
            config.set('Global', 'Underline', iniVal['Underline'])
            config.set('Global', 'iOS', iniVal['iOS'])
            config.set('Global', 'Android', iniVal['Android'])
            config.set('Global', 'TriggerScreenSaver', iniVal['TriggerScreenSaver'])
            config.set('Global', 'TriggerScrTime', iniVal['TriggerScrTime'])
            config.set('Global', 'TriggerScrText_X', iniVal['TriggerScrText_X'])
            config.set('Global', 'TriggerScrText_Mac', iniVal['TriggerScrText_Mac'])
            config.set('Global', 'TriggerScrText_Win', iniVal['TriggerScrText_Win'])
            config.set('Global', 'TriggerScrText_Other', iniVal['TriggerScrText_Other'])
            config.add_section(TrainType)
            config.set(TrainType, 'Blink', iniVal['timeBlink'])
            config.set(TrainType, 'Butterfly', iniVal['timeButterfly'])
            config.set(TrainType, '10Percent', iniVal['time10'])
            config.set(TrainType, '50Percent', iniVal['time50'])
            config.set(TrainType, '80Percent', iniVal['time80'])
            config.set(TrainType, 'Start', iniVal['startSequence'])
            config.set(TrainType, 'RepeatStart', iniVal['startRepeat'])
            config.set(TrainType, 'Main', iniVal['mainSequence'])
            config.set(TrainType, 'RepeatMain', iniVal['mainRepeat'])
            config.set(TrainType, 'End', iniVal['endSequence'])
            config.set(TrainType, 'RepeatEnd', iniVal['endRepeat'])
            config.write(configfile)

    # Define the path to Language.ini
    config_file_path = os.path.join(os.path.dirname(__file__), 'Language.ini')

    # Read the configuration file
    # Check if file was read successfully
    if not config.read(config_file_path, encoding='utf-8'):
        NoLanguage = True

    # Get Language
    iniVal['Language'] = iniVal['Language'].strip('"')
    LangShort = 'ActionShort' + iniVal['Language']
    LangLong = 'ActionLong' + iniVal['Language']
    LangProcedure = 'Procedures' + iniVal['Language']
    LangMessage = 'Messages' + iniVal['Language']

    # Values from Language.ini
    lang_values = {
        'strShortBlink': config.get(LangShort, 'Blink') if config.has_option(LangShort, 'Blink') else '"Blink"',
        'strShortButterfly': config.get(LangShort, 'Butterfly') if config.has_option(LangShort, 'Butterfly') else '"Butterfly / Windshield Wiper"',
        'strShort10': config.get(LangShort, '10Percent') if config.has_option(LangShort, '10Percent') else '"10%% Tension"',
        'strShort50': config.get(LangShort, '50Percent') if config.has_option(LangShort, '50Percent') else '"50%% Tension"',
        'strShort80': config.get(LangShort, '80Percent') if config.has_option(LangShort, '80Percent') else '"80%% Tension"',
        'strLongBlink': config.get(LangLong, 'Blink') if config.has_option(LangLong, 'Blink') else '"Tighten / Relax - As if you want to interrupt minimal urine flow."',
        'strLongButterfly': config.get(LangLong, 'Butterfly') if config.has_option(LangLong, 'Butterfly') else '"Relaxed left and right, or opening and closing the legs as if suppressing the urge to urinate."',
        'strLong10': config.get(LangLong, '10Percent') if config.has_option(LangLong, '10Percent') else '"Hold the tension like Blinking - As if you want to interrupt minimal urine flow."',
        'strLong50': config.get(LangLong, '50Percent') if config.has_option(LangLong, '50Percent') else '"Hold the tension like 50%% Tension - As if you want to interrupt medium urine flow."',
        'strLong80': config.get(LangLong, '80Percent') if config.has_option(LangLong, '80Percent') else '"Hold the tension like 80%% Tension - As if you want to interrupt strong urine flow. The anal sphincter is only activated here."',
        'strStart': config.get(LangProcedure, 'Start') if config.has_option(LangProcedure, 'Start') else '"Start procedure"',
        'strMain': config.get(LangProcedure, 'Main') if config.has_option(LangProcedure, 'Main') else '"Main procedure"',
        'strEnd': config.get(LangProcedure, 'End') if config.has_option(LangProcedure, 'End') else '"End procedure"',
        'msgEnter': config.get(LangMessage, 'PressEnter') if config.has_option(LangMessage, 'PressEnter') else '"Press Enter to continue..."',
        'msgEnterSpace': config.get(LangMessage, 'PressEnterSpace') if config.has_option(LangMessage, 'PressEnterSpace') else '"Press ENTER to cancel, SPACE to pause"',
        'msgSpaceEnter': config.get(LangMessage, 'iOSEnterSpace') if config.has_option(LangMessage, 'iOSEnterSpace') else '"Press SPACE + ENTER to cancel, ENTER to pause"',
        'msgStartDelay': config.get(LangMessage, 'StartDelay') if config.has_option(LangMessage, 'StartDelay') else '"Start delay"',
    }

    # Save default values to Language.ini
    if NoLanguage:
        # Save default values to Language.ini
        with open(config_file_path, 'w') as configfile:
            config.add_section(LangShort)
            config.set(LangShort, 'Blink', lang_values['strShortBlink'])
            config.set(LangShort, 'Butterfly', lang_values['strShortButterfly'])
            config.set(LangShort, '10Percent', lang_values['strShort10'])
            config.set(LangShort, '50Percent', lang_values['strShort50'])
            config.set(LangShort, '80Percent', lang_values['strShort80'])
            config.add_section(LangLong)
            config.set(LangLong, 'Blink', lang_values['strLongBlink'])
            config.set(LangLong, 'Butterfly', lang_values['strLongButterfly'])
            config.set(LangLong, '10Percent', lang_values['strLong10'])
            config.set(LangLong, '50Percent', lang_values['strLong50'])
            config.set(LangLong, '80Percent', lang_values['strLong80'])
            config.add_section(LangProcedure)
            config.set(LangProcedure, 'Start', lang_values['strStart'])
            config.set(LangProcedure, 'Main', lang_values['strMain'])
            config.set(LangProcedure, 'End', lang_values['strEnd'])
            config.add_section(LangMessage)
            config.set(LangMessage, 'PressEnter', lang_values['msgEnter'])
            config.set(LangMessage, 'PressEnterSpace', lang_values['msgEnterSpace'])
            config.set(LangMessage, 'iOSEnterSpace', lang_values['msgSpaceEnter'])
            config.set(LangMessage, 'StartDelay', lang_values['msgStartDelay'])
            config.write(configfile)
        # Restart App for right parsing %%
        os.execv(sys.executable, ['python3'] + sys.argv)

    # Combine iniVal and lang_values
    iniVal.update(lang_values)
    
    # Int values to integers
    iniVal['timeBlink'] = int(iniVal['timeBlink'])
    iniVal['timeButterfly'] = int(iniVal['timeButterfly'])
    iniVal['time10'] = int(iniVal['time10'])
    iniVal['time50'] = int(iniVal['time50'])
    iniVal['time80'] = int(iniVal['time80'])
    iniVal['startRepeat'] = int(iniVal['startRepeat'])
    iniVal['mainRepeat'] = int(iniVal['mainRepeat'])
    iniVal['endRepeat'] = int(iniVal['endRepeat'])
    iniVal['timeAutoDelay'] = int(iniVal['timeAutoDelay'])
    iniVal['TriggerScrTime'] = int(iniVal['TriggerScrTime'])
    iniVal['StartDelay'] = int(iniVal['StartDelay'])
    # Bool values to boolean
    iniVal['Automatic'] = bool(int(iniVal['Automatic']))
    iniVal['Debug'] = bool(int(iniVal['Debug']))
    iniVal['DoubleHeight'] = bool(int(iniVal['DoubleHeight']))
    iniVal['SimDoubleHeight'] = bool(int(iniVal['SimDoubleHeight']))
    iniVal['DoubleWidth'] = bool(int(iniVal['DoubleWidth']))
    iniVal['SimDoubleWidth'] = bool(int(iniVal['SimDoubleWidth']))
    iniVal['Bold'] = bool(int(iniVal['Bold']))
    iniVal['Italic'] = bool(int(iniVal['Italic']))
    iniVal['Underline'] = bool(int(iniVal['Underline']))
    iniVal['iOS'] = bool(int(iniVal['iOS']))
    iniVal['Android'] = bool(int(iniVal['Android']))
    iniVal['TriggerScreenSaver'] = bool(int(iniVal['TriggerScreenSaver']))
    # Strip leading and trailing '"' from strings
    iniVal['Version'] = iniVal['Version']. strip('"')
    iniVal['startSequence'] = iniVal['startSequence'].strip('"')
    iniVal['mainSequence'] = iniVal['mainSequence'].strip('"')
    iniVal['endSequence'] = iniVal['endSequence'].strip('"')
    iniVal['strShortBlink'] = iniVal['strShortBlink'].strip('"')
    iniVal['strShortButterfly'] = iniVal['strShortButterfly'].strip('"')
    iniVal['strShort10'] = iniVal['strShort10'].strip('"')
    iniVal['strShort50'] = iniVal['strShort50'].strip('"')
    iniVal['strShort80'] = iniVal['strShort80'].strip('"')
    iniVal['strLongBlink'] = iniVal['strLongBlink'].strip('"')
    iniVal['strLongButterfly'] = iniVal['strLongButterfly'].strip('"')
    iniVal['strLong10'] = iniVal['strLong10'].strip('"')
    iniVal['strLong50'] = iniVal['strLong50'].strip('"')
    iniVal['strLong80'] = iniVal['strLong80'].strip('"')
    iniVal['strStart'] = iniVal['strStart'].strip('"')
    iniVal['strMain'] = iniVal['strMain'].strip('"')
    iniVal['strEnd'] = iniVal['strEnd'].strip('"')
    iniVal['msgEnter'] = iniVal['msgEnter'].strip('"')
    iniVal['msgEnterSpace'] = iniVal['msgEnterSpace'].strip('"')
    iniVal['msgSpaceEnter'] = iniVal['msgSpaceEnter'].strip('"')
    iniVal['msgStartDelay'] = iniVal['msgStartDelay'].strip('"')
    iniVal['TriggerScrText_X'] = iniVal['TriggerScrText_X'].strip('"')
    iniVal['TriggerScrText_Mac'] = iniVal['TriggerScrText_Mac'].strip('"')
    iniVal['TriggerScrText_Win'] = iniVal['TriggerScrText_Win'].strip("'")  # Win string is encapsulated in single quotes
    iniVal['TriggerScrText_Other'] = iniVal['TriggerScrText_Other'].strip('"')

    # Make lists from sequences (" " and "_" are legal separators)
    iniVal['startSequence'] = iniVal['startSequence'].replace(' ', '_').split('_')
    iniVal['mainSequence'] = iniVal['mainSequence'].replace(' ', '_').split('_')
    iniVal['endSequence'] = iniVal['endSequence'].replace(' ', '_').split('_')

    if iniVal['iOS']:
        # iOS (a-shell) special - swap Enter and Space 
        iniVal['msgEnterSpace'] = iniVal['msgSpaceEnter']
        iOS = 1

    return iniVal


# Trigger the ScreenSaver WatchDog
def TriggerWatchDog():

    system = platform.system()

    if system == "Windows":
        # 'powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('+')"' Simulate Shift-KeyPress - Win10 or higher
        os.system(iniVal['TriggerScrText_Win'])

    elif system == "Darwin":
        # 'caffeinate -d -u -t 61 &'
        os.system(iniVal['TriggerScrText_Mac'])
    
    elif system == "Linux":
        # "xset s reset" X11 - no window-manager
        # "xdotool mousemove_relative 1 0 && xdotool mousemove_relative -- -1 0" probably works with all window-managers
        # "xscreensaver-command -deactivate > /dev/null 2>&1" may work with a lot window-managers
        os.system(iniVal['TriggerScrText_X'])
    
    else:
        # other OS
        os.system(iniVal['TriggerScrText_Other'])

def IsQuit(key):
    quitKeys = ['q', 'Q',
                'Ctrl-C',
                'Ctrl-Q',
                'Back'
                'Del',
                'Esc']
    if key in quitKeys:
        return True
    return False

# Convert esc-coded special keys to keyname (to esc.py)
def KeyToFunction(key):
    escKeys ={
        '\x1bOP': 'F1',
        '\x1bOQ': 'F2',
        '\x1bOR': 'F3',
        '\x1bOS': 'F4',
        '\x1b[15~': 'F5',
        '\x1b[17~': 'F6',
        '\x1b[18~': 'F7',
        '\x1b[19~': 'F8',
        '\x1b[20~': 'F9',
        '\x1b[21~': 'F10',
        '\x1b[23~': 'F11',
        '\x1b[24~': 'F12',
        '\x1b[1;2P': 'Shift-F1',
        '\x1b[1;2Q': 'Shift-F2',
        '\x1b[1;2R': 'Shift-F3',
        '\x1b[1;2S': 'Shift-F4',
        '\x1b[15;2~': 'Shift-F5',
        '\x1b[17;2~': 'Shift-F6',
        '\x1b[18;2~': 'Shift-F7',
        '\x1b[19;2~': 'Shift-F8',
        '\x1b[20;2~': 'Shift-F9',
        '\x1b[21;2~': 'Shift-F10',
        '\x1b[23;2~': 'Shift-F11',
        '\x1b[24;2~': 'Shift-F12',
        '\x1b[1;5P': 'Ctrl-F1',
        '\x1b[1;5Q': 'Ctrl-F2',
        '\x1b[1;5R': 'Ctrl-F3',
        '\x1b[1;5S': 'Ctrl-F4',
        '\x1b[15;5~': 'Ctrl-F5',
        '\x1b[17;5~': 'Ctrl-F6',
        '\x1b[18;5~': 'Ctrl-F7',
        '\x1b[19;5~': 'Ctrl-F8',
        '\x1b[20;5~': 'Ctrl-F9',
        '\x1b[21;5~': 'Ctrl-F10',
        '\x1b[23;5~': 'Ctrl-F11',
        '\x1b[24;5~': 'Ctrl-F12',
        '\x1b[1;6P': 'Ctrl-Shift-F1',
        '\x1b[1;6Q': 'Ctrl-Shift-F2',
        '\x1b[1;6R': 'Ctrl-Shift-F3',
        '\x1b[1;6S': 'Ctrl-Shift-F4',
        '\x1b[15;6~': 'Ctrl-Shift-F5',
        '\x1b[17;6~': 'Ctrl-Shift-F6',
        '\x1b[18;6~': 'Ctrl-Shift-F7',
        '\x1b[19;6~': 'Ctrl-Shift-F8',
        '\x1b[20;6~': 'Ctrl-Shift-F9',
        '\x1b[21;6~': 'Ctrl-Shift-F10',
        '\x1b[23;6~': 'Ctrl-Shift-F11',
        '\x1b[24;6~': 'Ctrl-Shift-F12',
        '\x1b[1;3P': 'Alt-F1',
        '\x1b[1;3Q': 'Alt-F2',
        '\x1b[1;3R': 'Alt-F3',
        '\x1b[1;3S': 'Alt-F4',
        '\x1b[15;3~': 'Alt-F5',
        '\x1b[17;3~': 'Alt-F6',
        '\x1b[18;3~': 'Alt-F7',
        '\x1b[19;3~': 'Alt-F8',
        '\x1b[20;3~': 'Alt-F9',
        '\x1b[21;3~': 'Alt-F10',
        '\x1b[23;3~': 'Alt-F11',
        '\x1b[24;3~': 'Alt-F12',
        '\x1b[1;4P': 'Alt-Shift-F1',
        '\x1b[1;4Q': 'Alt-Shift-F2',
        '\x1b[1;4R': 'Alt-Shift-F3',
        '\x1b[1;4S': 'Alt-Shift-F4',
        '\x1b[15;4~': 'Alt-Shift-F5',
        '\x1b[17;4~': 'Alt-Shift-F6',
        '\x1b[18;4~': 'Alt-Shift-F7',
        '\x1b[19;4~': 'Alt-Shift-F8',
        '\x1b[20;4~': 'Alt-Shift-F9',
        '\x1b[21;4~': 'Alt-Shift-F10',
        '\x1b[23;4~': 'Alt-Shift-F11',
        '\x1b[24;4~': 'Alt-Shift-F12',
        '\x1b[1;7P': 'Alt-Ctrl-F1',
        '\x1b[1;7Q': 'Alt-Ctrl-F2',
        '\x1b[1;7R': 'Alt-Ctrl-F3',
        '\x1b[1;7S': 'Alt-Ctrl-F4',
        '\x1b[15;7~': 'Alt-Ctrl-F5',
        '\x1b[17;7~': 'Alt-Ctrl-F6',
        '\x1b[18;7~': 'Alt-Ctrl-F7',
        '\x1b[19;7~': 'Alt-Ctrl-F8',
        '\x1b[20;7~': 'Alt-Ctrl-F9',
        '\x1b[21;7~': 'Alt-Ctrl-F10',
        '\x1b[23;7~': 'Alt-Ctrl-F11',
        '\x1b[24;7~': 'Alt-Ctrl-F12',
        '\x1b[A': 'Up',
        '\x1b[B': 'Down',
        '\x1b[C': 'Right',
        '\x1b[D': 'Left',
        '\x1b[E': 'Center',
        '\x1b[F': 'End',
        '\x1b[H': 'Home',
        '\x1b[Z': 'Shift-Tab',
        '\x1b[1;2A':'Shift-Up',
        '\x1b[1;2B':'Shift-Down',
        '\x1b[1;2C':'Shift-Right',
        '\x1b[1;2D':'Shift-Left',
        '\x1b[1;2E':'Shift-Center',
        '\x1b[1;2F':'Shift-End',
        '\x1b[1;2H':'Shift-Home',
        '\x1b[1;3A':'Alt-Up',
        '\x1b[1;3B':'Alt-Down',
        '\x1b[1;3C':'Alt-Right',
        '\x1b[1;3D':'Alt-Left',
        '\x1b[1;3E':'Alt-Center',
        '\x1b[1;3F':'Alt-End',
        '\x1b[1;3H':'Alt-Home',
        '\x1b[1;5A':'Ctrl-Up',
        '\x1b[1;5B':'Ctrl-Down',
        '\x1b[1;5C':'Ctrl-Right',
        '\x1b[1;5D':'Ctrl-Left',
        '\x1b[1;5E':'Ctrl-Center',
        '\x1b[1;5F':'Ctrl-End',
        '\x1b[1;5H':'Ctrl-Home',
        '\x7F': 'Back',
        '\x08': 'Back',
        '\x1b\x08': 'Alt-Back',
        '\x1b[3~': 'Del',
        '\x1b[2~': 'Ins',
        '\x1b[5~': 'PgUp',
        '\x1b[6~': 'PgDn',
        '\x09': 'Tab',
        '\x1b': 'Esc',
        '\x0A': 'Enter',
        '\x0D': 'Enter',
        '\x0D\x0A': 'Enter',
        '\x00': 'EOF',
        '\x01': 'Ctrl-A',
        '\x02': 'Ctrl-B',
        '\x03': 'Ctrl-C',
        '\x04': 'Ctrl-D',
        '\x05': 'Ctrl-E',
        '\x06': 'Ctrl-F',
        '\x07': 'Ctrl-G',
        # '\x08': 'Ctrl-H', Back
        # '\x09': 'Ctrl-I', Tab
        # '\x0A': 'Ctrl-J', Enter
        '\x0B': 'Ctrl-K',
        '\x0C': 'Ctrl-L',
        # '\x0D': 'Ctrl-M', Enter
        '\x0E': 'Ctrl-N',
        '\x0F': 'Ctrl-O',
        '\x10': 'Ctrl-P',
        '\x11': 'Ctrl-Q',
        '\x12': 'Ctrl-R',
        '\x13': 'Ctrl-S',
        '\x14': 'Ctrl-T',
        '\x15': 'Ctrl-U',
        '\x16': 'Ctrl-V',
        '\x17': 'Ctrl-W',
        '\x18': 'Ctrl-X',
        '\x19': 'Ctrl-Y',
        '\x1A': 'Ctrl-Z',
        '^A': 'Ctrl-A',
        '^B': 'Ctrl-B',
        '^C': 'Ctrl-C',
        '^D': 'Ctrl-D',
        '^E': 'Ctrl-E',
        '^F': 'Ctrl-F',
        '^G': 'Ctrl-G',
        '^H': 'Ctrl-H',
        '^I': 'Ctrl-I',
        '^J': 'Ctrl-J',
        '^K': 'Ctrl-K',
        '^L': 'Ctrl-L',
        '^M': 'Ctrl-M',
        '^N': 'Ctrl-N',
        '^O': 'Ctrl-O',
        '^P': 'Ctrl-P',
        '^Q': 'Ctrl-Q',
        '^R': 'Ctrl-R',
        '^S': 'Ctrl-S',
        '^T': 'Ctrl-T',
        '^U': 'Ctrl-U',
        '^V': 'Ctrl-V',
        '^W': 'Ctrl-W',
        '^X': 'Ctrl-X',
        '^Y': 'Ctrl-Y',
        '^Z': 'Ctrl-Z',
        '\x1b[2;2~': 'Shift-Ins',
        '\x1b[3;2~': 'Shift-Del',
        '\x1b[5;2~': 'Shift-PgUp',
        '\x1b[6;2~': 'Shift-PgDn',
        '\x1b[2;5~': 'Ctrl-Ins',
        '\x1b[3;5~': 'Ctrl-Del',
        '\x1b[5;5~': 'Ctrl-PgUp',
        '\x1b[6;5~': 'Ctrl-PgDn',
        '\x1b[2;3~': 'Alt-Ins',
        '\x1b[3;3~': 'Alt-Del',
        '\x1b[5;3~': 'Alt-PgUp',
        '\x1b[6;3~': 'Alt-PgDn',
        '\x1ba': 'Alt-a',
        '\x1bb': 'Alt-b',
        '\x1bc': 'Alt-c',
        '\x1bd': 'Alt-d',
        '\x1be': 'Alt-e',
        '\x1bf': 'Alt-f',
        '\x1bg': 'Alt-g',
        '\x1bh': 'Alt-h',
        '\x1bi': 'Alt-i',
        '\x1bj': 'Alt-j',
        '\x1bk': 'Alt-k',
        '\x1bl': 'Alt-l',
        '\x1bm': 'Alt-m',
        '\x1bn': 'Alt-n',
        '\x1bo': 'Alt-o',
        '\x1bp': 'Alt-p',
        '\x1bq': 'Alt-q',
        '\x1br': 'Alt-r',
        '\x1bs': 'Alt-s',
        '\x1bt': 'Alt-t',
        '\x1bu': 'Alt-u',
        '\x1bv': 'Alt-v',
        '\x1bw': 'Alt-w',
        '\x1bx': 'Alt-x',
        '\x1by': 'Alt-y',
        '\x1bz': 'Alt-z',
        '\x1bA': 'Shift-Alt-A',
        '\x1bB': 'Shift-Alt-B',
        '\x1bC': 'Shift-Alt-C',
        '\x1bD': 'Shift-Alt-D',
        '\x1bE': 'Shift-Alt-E',
        '\x1bF': 'Shift-Alt-F',
        '\x1bG': 'Shift-Alt-G',
        '\x1bH': 'Shift-Alt-H',
        '\x1bI': 'Shift-Alt-I',
        '\x1bJ': 'Shift-Alt-J',
        '\x1bK': 'Shift-Alt-K',
        '\x1bL': 'Shift-Alt-L',
        '\x1bM': 'Shift-Alt-M',
        '\x1bN': 'Shift-Alt-N',
        '\x1bO': 'Shift-Alt-O',
        '\x1bP': 'Shift-Alt-P',
        '\x1bQ': 'Shift-Alt-Q',
        '\x1bR': 'Shift-Alt-R',
        '\x1bS': 'Shift-Alt-S',
        '\x1bT': 'Shift-Alt-T',
        '\x1bU': 'Shift-Alt-U',
        '\x1bV': 'Shift-Alt-V',
        '\x1bW': 'Shift-Alt-W',
        '\x1bX': 'Shift-Alt-X',
        '\x1bY': 'Shift-Alt-Y',
        '\x1bZ': 'Shift-Alt-Z',
        '\x1b0': 'Alt-0',
        '\x1b1': 'Alt-1',
        '\x1b2': 'Alt-2',
        '\x1b3': 'Alt-3',
        '\x1b4': 'Alt-4',
        '\x1b5': 'Alt-5',
        '\x1b6': 'Alt-6',
        '\x1b7': 'Alt-7',
        '\x1b8': 'Alt-8',
        '\x1b9': 'Alt-9',
    }        
        
    if key in escKeys:
        #print({'key': key, 'value': escKeys[key]}, end='', flush=True)
        return escKeys[key]
    else:
        if key.startswith('\x1b'):
            #print({'ESC+(' + key[1:] + ' : ' + str(ord(key[1])) + ')'}, end='', flush=True)
            return 'ESC+(' + key[1:] + ' : ' + str(ord(key[1])) + ')'
        elif len(key):
            #if str(ord(key[0])) == '3':
                #return 'Ctrl-C'     # iOS (a-shell) special
            #print({key}, end='', flush=True)
            return key
        else:
            return 'NULL'

# Look for Keypress - returns key-name or key or "" (to esc.py)
def GetKeyPress():
    global iOS
    key= ''

    if os.name == 'nt':  # Windows - not working yet
        while True:
            if msvcrt.kbhit():
                c = msvcrt.getch().decode('utf-8')
                key += c
            else:
                if key:
                    key = KeyToFunction(key)
                    return key
                else:
                    return ''
                
    elif iOS:  
        # Even its working on all OS, it's very shitty cause of timing issues
        # additional not all hits are all time detected
        fd = sys.stdin.fileno()     
        if not iniVal['iOS']:
            tty.setraw(fd)
        while True:
            # Check if stdin has data to read
            if iniVal['iOS']:
                rlist, _, _ = select.select([sys.stdin], [], [], 0.33)
            else:
                rlist, _, _ = select.select([sys.stdin], [], [], 0.25)

            if rlist:
                c = sys.stdin.read(1)  # Lese 1 Zeichen
                key += c
            
            else:
                if not iniVal['iOS']:
                    os.system('stty sane')
                if key:
                    key = KeyToFunction(key)
                    if iniVal['iOS']:
                        # iOS special - swap Enter and Space (Enter for Pause / Space + Enter for Cancel)
                        if key == 'Enter':
                            key = ' '
                        elif key[0] == ' ':
                            key = 'Enter'
                    
                    return key
                else:
                    return ''

    else:  # Linux and macOS (after error a-shell under iOS)
        # idea from: https://stackoverflow.com/questions/71801157/detect-key-press-in-python-without-running-as-root-and-without-blockingioerror
        fd = sys.stdin.fileno()
        try:
            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)

            newattr[3] = newattr[3] & ~termios.ICANON 
            newattr[3] = newattr[3] & ~termios.ECHO
            newattr[6][termios.VMIN] = 0
            newattr[6][termios.VTIME] = 0
            termios.tcsetattr(fd, termios.TCSANOW, newattr)

            while True:
                try:
                    c = sys.stdin.read(1)
                    if c:
                        key += c
                    else:
                        key = KeyToFunction(key)
                        termios.tcsetattr(fd, termios.TCSANOW, oldterm)
                        return key
                except:
                    termios.tcsetattr(fd, termios.TCSANOW, oldterm)
                    return ''
                
        except:
            iOS = 1
            termios.tcsetattr(fd, termios.TCSANOW, oldterm)
            return GetKeyPress()
    

# Clear the console (to esc.py)
def escCLS():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux and MacOS
        os.system('clear')

# Set cursor position (to esc.py)
def escSetCursorPos(x, y):
    print(f'\033[{y};{x}H', end='', flush=True)

def escCursorDown(y = 1):
    print("\x1B[" + str(y) + "B", end="", flush=True)

def escCursorRight(x = 1):
    print("\x1B[" + str(x) + "C", end="", flush=True)

def escCursorLeft(x = 1):
    print("\x1B[" + str(x) + "D", end="", flush=True)

def escCursorUp(y = 1):
    print("\x1B[" + str(y) + "A", end="", flush=True)

def escCursorMoveX(x = 1):
    if x > 0:
        escCursorRight(x)
    elif x < 0:
        escCursorLeft(x * -1)

def escCursorMoveY(y = 1):
    if y > 0:
        escCursorUp(y)
    elif y < 0:
        escCursorDown(y * -1)

def escCursorMoveXY(x = 1, y = 1):
    escCursorMoveX(x)
    escCursorMoveY(y)

# Set cursor color - 16 Colors (to esc.py)
def escSetColor(fg, bg):
    print(f'\033[{30 + (fg % 8)}m\033[{40 + (bg % 8)}m', end='', flush=True)
    if fg >= 8:  # Bright foreground
        print('\033[1m', end='', flush=True)
    if bg >= 8:  # Bright background
        print('\033[5m', end='', flush=True)  # Optional: Blink for bright background

# Set cursor color - 255 Colors (to esc.py)
def escSet255Color(fg, bg):
    print(f'\033[38;5;{fg}m\033[48;5;{bg}m', end='', flush=True)

# Reset colors to terminal standard (to esc.py)
def escResetColor():
    print('\033[0m', end='', flush=True)

# Get Terminal Size (to esc.py)
def escGetTerminalSize():
    return os.get_terminal_size()

# Cursor On/Off
def escCursorVisible(state):
    if state:
        c = 'h'
    else:
        c = 'l'
    
    print(f'\033[?25{c}', end='', flush=True)
#Echo On/Off
def setEcho(state):
    # Set echo state
    if state:
        os.system('stty echo')
    else:
        os.system('stty -echo')

# Clear full line, y0 = current line
def escClrLine(y = 0, cnt = 1):
    if y:
        escSetCursorPos(1, y)
    for i in range(cnt):
        print('\033[2K', end='', flush=True)
        escCursorDown(1)
# Clear line from cursor to end of line, y0 = current line
def escClrLineEnd(x = 0, y = 0, cnt = 1):
    if y:
        escSetCursorPos(x, y)
    for i in range(cnt):
        print('\033[K', end='', flush=True)
        escCursorDown(1)
# Clear line from start of line to cursor, y0 = current line
def escClrLineStart(x = 0, y = 0, cnt = 1):
    if y:
        escSetCursorPos(x, y)
    for i in range(cnt):
        print('\033[1K', end='', flush=True)
        escCursorDown(1)
# Clear rectangle from x1,y1 to x2,y2
def escClrRect(x1, y1, x2, y2):
    
    global termSize

    # Sort x and y that x1,y1 is top left and x2,y2 is bottom right
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    # Take care that x & y are in range
    if x1 < 1 and x2 < 1:
        return
    elif x1 < 1:
        x1 = 1
    if x2 > termSize.columns and x1 > termSize.columns:
        return
    elif x2 > termSize.columns:
        x2 = termSize.columns
    if y1 < 1 and y2 < 1:
        return
    elif y1 < 1:
        y1 = 1
    if y2 > termSize.lines and y1 > termSize.lines:
        return
    elif y2 > termSize.lines:
        y2 = termSize.lines
    
    # Cnt of lines to clear
    cnt = y2 - y1 + 1
    
    # Check if x1 is 1 and / or x2 is termSize.columns
    if x1 == 1 and x2 == termSize.columns:
        # Clear full lines
        escClrLine(y1, cnt)
    elif x1 == 1:
        # Clear from cursor to start of line
        escClrLineStart(x2, y1, cnt)
    elif x2 == termSize.columns:
        # Clear from start of line to cursor
        escClrLineEnd(x1, y1, cnt)
    else:
        # Clear rectangle with spaces
        escSetCursorPos(x1, y1)
        for i in range(y1, y2 + 1):
            print(" " * cnt, end='', flush=True)
            escCursorDown(1)

# QuitApp
def QuitApp(cls = 1):
    # Reset terminal settings
    escResetColor()
    escResetStyle()
    escCursorVisible(1)
    setEcho(1)
    if cls:
        escCLS()
    sys.exit(0)

### Set cursor style ### (all 7 to esc.py)
def escSetStyle(style):
        print(f"\033[{style}m", end='', flush=True)
#Reset cursor style
def escResetStyle():
    escSetStyle(0)
# Set cursor bold
def escSetBold(state):
    escSetStyle(1 if state else 22)
# Set cursor faint
def escSetFaint(state):
    escSetStyle(2 if state else 22)
# Set cursor underline
def escSetUnderline(state):
    escSetStyle(4 if state else 24)
# Set cursor italic
def escSetItalic(state):
    escSetStyle(3 if state else 23)
# Set cursor inverted
def escSetInverted(state):
    escSetStyle(7 if state else 27)
### ###

### Set cursor height/width ### (all 5 to esc.py)
def escSetDoubleHW(state):
    print(f'\033#{state}', end='', flush=True)
# Reset cursor double height and width
def escResetDoubleHW():
    escSetDoubleHW(5)
# Set cursor double height - DECDHL top half
def escSetDoubleHeightTop():
    escSetDoubleHW(3)
# Set cursor double height - DECDHL bottom half
def escSetDoubleHeightBottom():
    escSetDoubleHW(4)
# Set cursor double width - DECDWL
def escSetDoubleWidth():
    escSetDoubleHW(6)
### ###

# Print at position
def PrintAtPos(text, x, y, clear = 0, right = 0, space = ' '):
    text = str(text)
    escSetCursorPos(x, y)
    if clear > 0:
        escResetDoubleHW()
        print(space * clear, end='', flush=True)
        if right > 0:
            # Right align the text (need improvement - real reverse print)
            x += clear - len(text)
        escSetCursorPos(x, y)
    print(text, end='', flush=True)

    return len(text)

# Builds centered text with leading and optional trailing spaces
def CenterText(text, width, justLeft = False, justCnt = False):
    text = str(text)
    lenText = len(text)
    if lenText >= width:
        return text
    spaces = (width - lenText) // 2
    if justCnt:
        return spaces
    text = ' ' * spaces + text
    if justLeft:
        return text

    return text + ' ' * (width - lenText - spaces)

# Multiple lines from too long text or text with linefeed's.
def TextToLines(text, width):
    # Replace linefeed placeholder '\n' with real linefeed's
    # Preserve existing linefeed's by a new line, independent of the width.
    # Still too width lines split on spaces. 
    text = str(text).replace('\\n', '\n')
    lines = []
    for line in text.split('\n'):
        words = line.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    return lines

# Make text double length by adding a space to each char
def DoubleText(text):
    text = str(text)
    double_text = ""
    for char in text:
        double_text += char + ' '
    return double_text[:-1]  # Remove last space

# Print double height text
def PrintDoubleHeight (text, x, y, clear = 0, right = 0, space = ' '):

    if iniVal['DoubleHeight']:
        escSetCursorPos(x, y - 1)
        escSetDoubleHeightTop()
    else:
        text = DoubleText(text)

    PrintAtPos(text, x, y - 1, clear, right, space)

    if iniVal['DoubleHeight']:
        escSetCursorPos(x, y)
        escSetDoubleHeightBottom()

    PrintAtPos(text, x, y, clear, right, space)

# Print double width text
def PrintDoubleWidth (text, x, y, clear = 0, right = 0, space = ' '):
    
    if iniVal['DoubleWidth']:
        escSetCursorPos(x, y)
        escSetDoubleWidth()
    else:
        text = DoubleText(text)
    
    PrintAtPos(text, x, y, clear, right, space)

# Run loop for 'timing' seconds - return runtime
def run_loop(timing, msg = '', x = 1, y = 1, printTime = 1):
    # Space pauses/continues the loop
    # Enter stops the loop - return 0
    global iOS
    global TriggerTime
    global iniVal
    global termSize

    timing = float(timing)
    start_time = time.time()
    loopCnt = 0

    # All about *PrintTime became necessary for Win to prevent flickering - what a messi OS... :-(
    lastPrintTime = 0 
    actPrintTime = 0

    if msg:
        # Print "Press ENTER / SPACE"
        if iniVal['Italic']:
            escSetItalic(1)
        # PrintAtPos(msg, 23, termSize.lines - 5 )
        msg = TextToLines(msg, termSize.columns - x)
        cntLines = len(msg)
        len1stLine = 0
        for i in range(cntLines):
            if i > 0:
                msg[i] = CenterText(msg[i], len1stLine)
            len1stLine = PrintAtPos(msg[i], x, y + i)
        escResetStyle()

    if printTime:
        # Print time left
        if iniVal['Bold']:
            escSetBold(1)
        actPrintTime = int(timing - (time.time() - start_time) + 1)
        PrintAtPos(f"{actPrintTime}", x - 5, y, 3, 1, ' ')
        lastPrintTime = actPrintTime
        escResetStyle()

    while time.time() - start_time < timing:
        if not iOS: 
            time.sleep(0.05)
        key = GetKeyPress()
        #print("press:" + key, end='', flush=True)
        if key == " ":
            #print("\nspace", end='', flush=True)
            pause_time = time.time()
            while True:
                if not iOS:
                    time.sleep(0.05)
                key = GetKeyPress()
                if key == " ":
                    break
                elif key == "Enter":
                    return 0
                elif IsQuit(key):
                    QuitApp()
            start_time += time.time() - pause_time
        elif key == "Enter":
            return 0
        elif IsQuit(key):
            QuitApp()
        
        loopCnt += 1
        
        if loopCnt > 3:
            # Print time left
            actPrintTime = int(timing - (time.time() - start_time) + 1)
            if actPrintTime != lastPrintTime:
                if iniVal['Bold']:
                    escSetBold(1)
                PrintAtPos(f"{actPrintTime}", x - 5, y, 3, 1, ' ')
                escResetStyle()
                lastPrintTime = actPrintTime
            loopCnt = 0

        # Check on ScreenSaver
        if iniVal['TriggerScreenSaver']:
            if time.time() - TriggerTime > iniVal['TriggerScrTime']:
                TriggerWatchDog()
                TriggerTime = time.time()

    return time.time() - start_time


# Main program

# Get parameters from the command line
TrainType = 'Default'
if len(sys.argv) > 1:
    TrainType = sys.argv[1]

# Load ini-values from the configuration files
iniVal = LoadSettings(TrainType)

escCursorVisible(0)  # Hide cursor
setEcho(0)  # Disable echo

if iniVal['Debug']:
    escCLS()
    print(f"Debug mode is ON. Loaded settings for {TrainType}:\n")
    for key, value in iniVal.items():
        print(f"   {key}: {value}")
    input("\nPress Enter to continue...") 

if iniVal['StartDelay'] > 0:
    # Delay before starting the training
    escCLS()
    # Get terminal size (before eventually changing it - e.g hiding keyboard)
    termSize = escGetTerminalSize()
    run_loop(iniVal['StartDelay'], iniVal['msgStartDelay'], 10, 3)

loopState = 1  # 1=Start, 2=Main, 3=End
loopCnt = 0
loopTime = 0
cntMaxDescription = 0
cntDescription = 0

# Get terminal size - final size - no size change recognition during runtime 
termSize = escGetTerminalSize()

# Training Loop
while loopState < 4:
    
    escCLS()

    # Text positions
    posTime = termSize.lines - (termSize.lines - 24) - 5
    posAction = termSize.lines - (termSize.lines - 24) - 3
    posRepeat = termSize.lines - (termSize.lines - 24) -2
    offsetX = termSize.columns - 80
    if offsetX < -9:
        offsetX = -9
    elif offsetX > 0:
        offsetX = 0
    

    # print inverted header
    escSetInverted(1)
    if iniVal['Bold']:
        escSetBold(1)
    strHeader = f"{appName} {appVersion} - {appCopyright} {appAuthor} - {appDate}"
    # Maybe too long
    strHeader = TextToLines(strHeader, termSize.columns)
    # center all lines
    cntHeaderLines = 0
    for i, line in enumerate(strHeader):
        strHeader[i] = CenterText(line, termSize.columns)
        PrintAtPos(strHeader[i], 1, i + 1)
        cntHeaderLines += 1
    escSetInverted(0)

    # print description/placeholder for loop of loop_repeat  &  action_cnt of action_len  &  action time left 
    PrintAtPos("  Time:", offsetX + 10, posTime)
    PrintAtPos("Action:     /    ", offsetX + 10, posAction)
    PrintAtPos("Repeat:     /    ", offsetX + 10, posRepeat)
    escResetStyle()

    # text - actual procedure - Centered double width or standard bold_italic
    if loopState == 1:
        strProcedure = iniVal['strStart']
    elif loopState == 2:
        strProcedure = iniVal['strMain']
    else:
        strProcedure = iniVal['strEnd']

    # Width - depending on settings DoubleWidth
    if iniVal['DoubleWidth'] or iniVal['SimDoubleWidth']:
        termWidthHlp = termSize.columns // 2
    else:
        termWidthHlp = termSize.columns

    strProcedure = TextToLines(strProcedure, termWidthHlp)
    # Center all lines
    cntProcedureLines = 0
    for i, line in enumerate(strProcedure):
        strProcedure[i] = CenterText(line, termWidthHlp)
        cntProcedureLines += 1

    if not iniVal['DoubleWidth']:
        # bold_italic just for simulated and no real-double
        if iniVal['Italic']:
            escSetItalic(1)
        if iniVal['Bold']:
            escSetBold(1)
    for i in range(cntProcedureLines):
        if iniVal['DoubleWidth'] or iniVal['SimDoubleWidth']:
            # Print double width text
            PrintDoubleWidth(strProcedure[i], 1, cntHeaderLines + 2)
        else:
            # Print normal text
            PrintAtPos(strProcedure[i], 1, cntHeaderLines + 2)

    escResetStyle()

    if loopState == 1:
        loop_list = iniVal['startSequence']
        loop_repeat = iniVal['startRepeat']
    elif loopState == 2:
        loop_list = iniVal['mainSequence']
        loop_repeat = iniVal['mainRepeat']
    else:
        loop_list = iniVal['endSequence']
        loop_repeat = iniVal['endRepeat']

    for loop in range(loop_repeat):
        # count of elements in loop_list
        action_len = len(loop_list)
        if action_len > 0:
            action_cnt = 0
            # Loop the sequences
            for action in loop_list:
                action_cnt += 1
                if action == 'Bl':
                    action_time = iniVal['timeBlink']
                    action_text_long = TextToLines(iniVal['strLongBlink'], termSize.columns - (10 + offsetX))
                    action_text = iniVal['strShortBlink']
                elif action == 'Bu':
                    action_time = iniVal['timeButterfly']
                    action_text_long = TextToLines(iniVal['strLongButterfly'], termSize.columns - (10 + offsetX))
                    action_text = iniVal['strShortButterfly']
                elif action == '10':
                    action_time = iniVal['time10']
                    action_text_long = TextToLines(iniVal['strLong10'], termSize.columns - (10 + offsetX))
                    action_text = iniVal['strShort10']
                elif action == '50':
                    action_time = iniVal['time50']
                    action_text_long = TextToLines(iniVal['strLong50'], termSize.columns - (10 + offsetX))
                    action_text = iniVal['strShort50']
                elif action == '80':
                    action_time = iniVal['time80']
                    action_text_long = TextToLines(iniVal['strLong80'], termSize.columns - (10 + offsetX))
                    action_text = iniVal['strShort80']
                else:
                    # Unknown action - fatal error
                    escSetColor(cRed, cBg)
                    PrintAtPos(f"Unknown action: {action} in sequence {strProcedure}", 1, termSize.lines)
                    QuitApp(0)

                # Print the action. Centered - Double height or simulated bold double width

                termWidthHlp = termSize.columns // 2

                action_text = TextToLines(action_text, termWidthHlp)
                # Center all lines
                cntActionLines = 0
                for i, line in enumerate(action_text):
                    action_text[i] = CenterText(line, termWidthHlp)
                    cntActionLines += 1

                if not iniVal['DoubleHeight']:
                    # All but real double height
                    escSetBold(1)

                for i in range(cntActionLines):
                    if iniVal['DoubleHeight'] or iniVal['SimDoubleHeight']:
                        # Print double height text
                        PrintDoubleHeight(action_text[i], 1, 4 + cntHeaderLines + cntProcedureLines + i * 2)
                    else:
                        #Print standard height text - but double width
                        action_text[i] = DoubleText(action_text[i])
                        PrintAtPos(action_text[i], 1, 3 + cntHeaderLines + cntProcedureLines + i)
                if iniVal['DoubleHeight'] or iniVal['SimDoubleHeight']:
                    cntActionLines *= 2

                escResetStyle()

                # Print the description
                cntDescription = 0
                if iniVal['Italic']:
                    escSetItalic(1)
                for i, line in enumerate(action_text_long):
                    PrintAtPos(line, 10 + offsetX, 4 + cntActionLines + cntHeaderLines + cntProcedureLines + i, termSize.columns - (10 + offsetX))
                    cntDescription += 1
                
                if cntDescription > cntMaxDescription:
                    cntMaxDescription = cntMaxDescription
                
                if cntDescription < cntMaxDescription:
                    # Clear the remaining lines
                    escClrLine(6 + cntHeaderLines + cntHeaderLines + cntProcedureLines, cntMaxDescription - cntDescription)
                
                escResetStyle()

                # print loop of loop_repeat  &  action_cnt of action_len
                PrintAtPos(action_cnt, 18 + offsetX, posAction, 3, 1, '0')
                PrintAtPos(action_len, 24 + offsetX, posAction, 3, 1, '0')
                PrintAtPos((loop + 1), 18 + offsetX, posRepeat, 3, 1, '0')
                PrintAtPos(loop_repeat, 24 + offsetX, posRepeat, 3, 1, '0')

                # Run the timing loop for the specified time 
                escSetColor(cGreen, cBg)
                loopTime = run_loop(action_time, iniVal['msgEnterSpace'], 23 + offsetX, posTime)
                escResetColor()

                # Clear the timer - text and "Press Enter"
                escClrLineEnd(18 + offsetX, posTime, 2)
                # Clear the action and description
                escClrLine(4 + cntHeaderLines, cntHeaderLines + cntActionLines + cntDescription + 3)

                if ((action_cnt < action_len) or (loop + 1 < loop_repeat)) and not action == '10' and not action == '50':
                    # Pause between actions
                    escSetColor(cBlue, cBg)
                    if iniVal['Automatic']:
                        run_loop(iniVal['timeAutoDelay'], iniVal['msgEnterSpace'], 23 + offsetX, posTime)
                    else:
                        PrintAtPos({iniVal['msgEnter']}, 23 + offsetX, posTime)
                    escResetColor()

    # Clear Procedure line
    escClrLine(cntHeaderLines + 2)

    if loopState < 3:
        # Pause between Procedures (Start -> End)
        if iniVal['Automatic']:
            run_loop(int(iniVal['timeAutoDelay'] * 1.5), iniVal['msgEnterSpace'], 23 + offsetX, posTime)
        else:
            PrintAtPos({iniVal['msgEnter']}, 23 + offsetX, posTime)

    loopState += 1

QuitApp()

