import os
import sys
import configparser
import time
import select
import tty
import platform

if os.name == 'nt':  # Windows
    import msvcrt
else:  # Linux und MacOS
    import termios

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
appVersion = "0.0.8a"
appAuthor = "github.com/PitWD"
appCopyright = "(c) GPL by"
appDate = "2025-05-05"

# OS
iOS = 0  # iOS special (a-shell)

# Trigger time for ScreenSaver WatchDog
TriggerTime = time.time() 

# Load Values from INI (quick 'n' dirty, slow, case sensitive but type-safe)
def LoadSettings(TrainType = 'Default'):

    global iOS

    NoSettings = False
    NoLanguage = False

    # Define the path to Settings.ini
    config_file_path = os.path.join(os.path.dirname(__file__), 'Settings.ini')

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    # Check if file was read successfully
    if not config.read(config_file_path):
        NoSettings = True

    # Values from Settings.ini
    iniVal = {
        'version': config.get('Global', 'Version') if config.has_option('Global', 'Version') else '1.0.0',
        'debug': config.get('Global', 'Debug') if config.has_option('Global', 'Debug') else '0',
        'StartDelay': config.get('Global', 'StartDelay') if config.has_option('Global', 'StartDelay') else '1',
        'blink_time': config.get(TrainType, 'Blink') if config.has_option(TrainType, 'Blink') else '60',
        'butterfly_time': config.get(TrainType, 'Butterfly') if config.has_option(TrainType, 'Butterfly') else '10',
        'percent10_time': config.get(TrainType, '10Percent') if config.has_option(TrainType, '10Percent') else '10',
        'percent50_time': config.get(TrainType, '50Percent') if config.has_option(TrainType, '50Percent') else '10',
        'percent80_time': config.get(TrainType, '80Percent') if config.has_option(TrainType, '80Percent') else '10',
        'start_sequence': config.get(TrainType, 'Start') if config.has_option(TrainType, 'Start') else 'Bu_Bl',
        'start_repeat': config.get(TrainType, 'RepeatStart') if config.has_option(TrainType, 'RepeatStart') else '2',
        'main_sequence': config.get(TrainType, 'Main') if config.has_option(TrainType, 'Main') else 'Bu_10_50_80_Bu_10_50_80_Bu_Bl',
        'main_repeat': config.get(TrainType, 'RepeatMain') if config.has_option(TrainType, 'RepeatMain') else '6',
        'end_sequence': config.get(TrainType, 'End') if config.has_option(TrainType, 'End') else 'Bu',
        'end_repeat': config.get(TrainType, 'RepeatEnd') if config.has_option(TrainType, 'RepeatEnd') else '1',
        'language': config.get('Global', 'Language') if config.has_option('Global', 'Language') else '"EN"',
        'automatic': config.get('Global', 'Automatic') if config.has_option('Global', 'Automatic') else '1',
        'auto_delay_time': config.get('Global', 'AutoDelayTime') if config.has_option('Global', 'AutoDelayTime') else '3',
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
        'TriggerScrText_X': config.get('Global', 'TriggerScrText_X') if config.has_option('Global', 'TriggerScrText_X') else 'xset s reset',
        'TriggerScrText_Mac': config.get('Global', 'TriggerScrText_Mac') if config.has_option('Global', 'TriggerScrText_Mac') else 'caffeinate -u -t 90',
        'TriggerScrText_Win': config.get('Global', 'TriggerScrText_Win') if config.has_option('Global', 'TriggerScrText_Win') else '''powershell -Command "[System.Windows.Forms.SendKeys]::SendWait(\'{F15}\')"''',
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
            config.set('Global', 'Language', iniVal['language'])
            config.set('Global', 'Automatic', iniVal['automatic'])
            config.set('Global', 'AutoDelayTime', iniVal['auto_delay_time'])
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
            config.set(TrainType, 'Blink', iniVal['blink_time'])
            config.set(TrainType, 'Butterfly', iniVal['butterfly_time'])
            config.set(TrainType, '10Percent', iniVal['percent10_time'])
            config.set(TrainType, '50Percent', iniVal['percent50_time'])
            config.set(TrainType, '80Percent', iniVal['percent80_time'])
            config.set(TrainType, 'Start', iniVal['start_sequence'])
            config.set(TrainType, 'RepeatStart', iniVal['start_repeat'])
            config.set(TrainType, 'Main', iniVal['main_sequence'])
            config.set(TrainType, 'RepeatMain', iniVal['main_repeat'])
            config.set(TrainType, 'End', iniVal['end_sequence'])
            config.set(TrainType, 'RepeatEnd', iniVal['end_repeat'])
            config.write(configfile)

    # Define the path to Language.ini
    config_file_path = os.path.join(os.path.dirname(__file__), 'Language.ini')

    # Read the configuration file
    # Check if file was read successfully
    if not config.read(config_file_path):
        NoLanguage = True

    # Get Language
    iniVal['language'] = iniVal['language'].strip('"')
    LangShort = 'ActionShort' + iniVal['language']
    LangLong = 'ActionLong' + iniVal['language']
    LangProcedure = 'Procedures' + iniVal['language']
    LangMessage = 'Messages' + iniVal['language']

    # Values from Language.ini
    lang_values = {
        'short_blink': config.get(LangShort, 'Blink') if config.has_option(LangShort, 'Blink') else '"Blink"',
        'short_butterfly': config.get(LangShort, 'Butterfly') if config.has_option(LangShort, 'Butterfly') else '"Butterfly / Windshield Wiper"',
        'short_10percent': config.get(LangShort, '10Percent') if config.has_option(LangShort, '10Percent') else '"10%% Tension"',
        'short_50percent': config.get(LangShort, '50Percent') if config.has_option(LangShort, '50Percent') else '"50%% Tension"',
        'short_80percent': config.get(LangShort, '80Percent') if config.has_option(LangShort, '80Percent') else '"80%% Tension"',
        'long_blink': config.get(LangLong, 'Blink') if config.has_option(LangLong, 'Blink') else '"Tighten / Relax - As if you want to interrupt minimal urine flow."',
        'long_butterfly': config.get(LangLong, 'Butterfly') if config.has_option(LangLong, 'Butterfly') else '"Relaxed left and right, or opening and closing the legs as if suppressing the urge to urinate."',
        'long_10percent': config.get(LangLong, '10Percent') if config.has_option(LangLong, '10Percent') else '"Hold the tension like Blinking - As if you want to interrupt minimal urine flow."',
        'long_50percent': config.get(LangLong, '50Percent') if config.has_option(LangLong, '50Percent') else '"Hold the tension like 50%% Tension - As if you want to interrupt medium urine flow."',
        'long_80percent': config.get(LangLong, '80Percent') if config.has_option(LangLong, '80Percent') else '"Hold the tension like 80%% Tension - As if you want to interrupt strong urine flow. The anal sphincter is only activated here."',
        'start_procedure': config.get(LangProcedure, 'Start') if config.has_option(LangProcedure, 'Start') else '"Start procedure"',
        'main_procedure': config.get(LangProcedure, 'Main') if config.has_option(LangProcedure, 'Main') else '"Main procedure"',
        'end_procedure': config.get(LangProcedure, 'End') if config.has_option(LangProcedure, 'End') else '"End procedure"',
        'msg_press_enter': config.get(LangMessage, 'PressEnter') if config.has_option(LangMessage, 'PressEnter') else '"Press Enter to continue..."',
        'msg_press_enter_space': config.get(LangMessage, 'PressEnterSpace') if config.has_option(LangMessage, 'PressEnterSpace') else '"Press ENTER to cancel, SPACE to pause"',
        'msg_iOS_enter_space': config.get(LangMessage, 'iOSEnterSpace') if config.has_option(LangMessage, 'iOSEnterSpace') else '"Press SPACE + ENTER to cancel, ENTER to pause"',
        'msg_start_delay': config.get(LangMessage, 'StartDelay') if config.has_option(LangMessage, 'StartDelay') else '"Start delay"',
    }

    # Save default values to Language.ini
    if NoLanguage:
        # Save default values to Language.ini
        with open(config_file_path, 'w') as configfile:
            config.add_section(LangShort)
            config.set(LangShort, 'Blink', lang_values['short_blink'])
            config.set(LangShort, 'Butterfly', lang_values['short_butterfly'])
            config.set(LangShort, '10Percent', lang_values['short_10percent'])
            config.set(LangShort, '50Percent', lang_values['short_50percent'])
            config.set(LangShort, '80Percent', lang_values['short_80percent'])
            config.add_section(LangLong)
            config.set(LangLong, 'Blink', lang_values['long_blink'])
            config.set(LangLong, 'Butterfly', lang_values['long_butterfly'])
            config.set(LangLong, '10Percent', lang_values['long_10percent'])
            config.set(LangLong, '50Percent', lang_values['long_50percent'])
            config.set(LangLong, '80Percent', lang_values['long_80percent'])
            config.add_section(LangProcedure)
            config.set(LangProcedure, 'Start', lang_values['start_procedure'])
            config.set(LangProcedure, 'Main', lang_values['main_procedure'])
            config.set(LangProcedure, 'End', lang_values['end_procedure'])
            config.add_section(LangMessage)
            config.set(LangMessage, 'PressEnter', lang_values['msg_press_enter'])
            config.set(LangMessage, 'PressEnterSpace', lang_values['msg_press_enter_space'])
            config.set(LangMessage, 'iOSEnterSpace', lang_values['msg_iOS_enter_space'])
            config.set(LangMessage, 'StartDelay', lang_values['msg_start_delay'])
            config.write(configfile)
        # Restart App for right parsing %%
        os.execv(sys.executable, ['python3'] + sys.argv)

    # Combine iniVal and lang_values
    iniVal.update(lang_values)
    
    # Int values to integers
    iniVal['blink_time'] = int(iniVal['blink_time'])
    iniVal['butterfly_time'] = int(iniVal['butterfly_time'])
    iniVal['percent10_time'] = int(iniVal['percent10_time'])
    iniVal['percent50_time'] = int(iniVal['percent50_time'])
    iniVal['percent80_time'] = int(iniVal['percent80_time'])
    iniVal['start_repeat'] = int(iniVal['start_repeat'])
    iniVal['main_repeat'] = int(iniVal['main_repeat'])
    iniVal['end_repeat'] = int(iniVal['end_repeat'])
    iniVal['auto_delay_time'] = int(iniVal['auto_delay_time'])
    iniVal['TriggerScrTime'] = int(iniVal['TriggerScrTime'])
    iniVal['StartDelay'] = int(iniVal['StartDelay'])
    # Bool values to boolean
    iniVal['automatic'] = bool(int(iniVal['automatic']))
    iniVal['debug'] = bool(int(iniVal['debug']))
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
    iniVal['version'] = iniVal['version'].strip('"')
    iniVal['start_sequence'] = iniVal['start_sequence'].strip('"')
    iniVal['main_sequence'] = iniVal['main_sequence'].strip('"')
    iniVal['end_sequence'] = iniVal['end_sequence'].strip('"')
    iniVal['short_blink'] = iniVal['short_blink'].strip('"')
    iniVal['short_butterfly'] = iniVal['short_butterfly'].strip('"')
    iniVal['short_10percent'] = iniVal['short_10percent'].strip('"')
    iniVal['short_50percent'] = iniVal['short_50percent'].strip('"')
    iniVal['short_80percent'] = iniVal['short_80percent'].strip('"')
    iniVal['long_blink'] = iniVal['long_blink'].strip('"')
    iniVal['long_butterfly'] = iniVal['long_butterfly'].strip('"')
    iniVal['long_10percent'] = iniVal['long_10percent'].strip('"')
    iniVal['long_50percent'] = iniVal['long_50percent'].strip('"')
    iniVal['long_80percent'] = iniVal['long_80percent'].strip('"')
    iniVal['start_procedure'] = iniVal['start_procedure'].strip('"')
    iniVal['main_procedure'] = iniVal['main_procedure'].strip('"')
    iniVal['end_procedure'] = iniVal['end_procedure'].strip('"')
    iniVal['msg_press_enter'] = iniVal['msg_press_enter'].strip('"')
    iniVal['msg_press_enter_space'] = iniVal['msg_press_enter_space'].strip('"')
    iniVal['msg_iOS_enter_space'] = iniVal['msg_iOS_enter_space'].strip('"')
    iniVal['msg_start_delay'] = iniVal['msg_start_delay'].strip('"')
    iniVal['TriggerScrText_X'] = iniVal['TriggerScrText_X'].strip('"')
    iniVal['TriggerScrText_Mac'] = iniVal['TriggerScrText_Mac'].strip('"')
    iniVal['TriggerScrText_Win'] = iniVal['TriggerScrText_Win'].strip("'")  # Win string is encapsulated in single quotes
    iniVal['TriggerScrText_Other'] = iniVal['TriggerScrText_Other'].strip('"')

    # Make lists from sequences (" " and "_" are legal separators)
    iniVal['start_sequence'] = iniVal['start_sequence'].replace(' ', '_').split('_')
    iniVal['main_sequence'] = iniVal['main_sequence'].replace(' ', '_').split('_')
    iniVal['end_sequence'] = iniVal['end_sequence'].replace(' ', '_').split('_')

    if iniVal['iOS']:
        # iOS (a-shell) special - swap Enter and Space 
        iniVal['msg_press_enter_space'] = iniVal['msg_iOS_enter_space']
        iOS = 1

    return iniVal


# Trigger the ScreenSaver WatchDog
def TriggerWatchDog():

    system = platform.system()

    if system == "Windows":
        # Windows: Sim a mouse move - Win10 or higher
        # 'powershell -Command "[System.Windows.Forms.SendKeys]::SendWait(\'{F15}\')"'
        os.system(iniVal['TriggerScrText_Win'])

    elif system == "Darwin":
        # 'caffeinate -u -t 90'
        os.system(iniVal['TriggerScrText_Mac'])
    
    elif system == "Linux":
        # 'xset s reset'
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

# Look for Keypress - returns key or "" (to esc.py)
def GetKeyPress():
    global iOS
    key= ''

    if os.name == 'nt':  # Windows - not working yet
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
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

# Cursor On/Offursor
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
        print(space * clear, end='', flush=True)
        if right > 0:
            # Right align the text (need improvement - real reverse print)
            x += clear - len(text)
        escSetCursorPos(x, y)
    print(text, end='', flush=True)

# Builds centered text with leading and trailing spaces
def CenterText(text, width):
    text = str(text)
    if len(text) >= width:
        return text
    spaces = (width - len(text)) // 2
    return ' ' * spaces + text + ' ' * (width - len(text) - spaces)

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

    timing = float(timing)
    start_time = time.time()
    term_size = escGetTerminalSize()
    term_width = term_size.columns
    term_height = term_size.lines
    loop_cnt = 0

    if msg:
        # Print "Press ENTER / SPACE"
        if iniVal['Italic']:
            escSetItalic(1)
        # PrintAtPos(msg, 23, term_height - 5 )
        PrintAtPos(msg, x, y )
        escResetStyle()

    if printTime:
        # Print time left
        if iniVal['Bold']:
            escSetBold(1)
        # PrintAtPos(f"{int(timing - (time.time() - start_time) + 1)}", 18, term_height - 5, 3, 1, ' ')
        PrintAtPos(f"{int(timing - (time.time() - start_time) + 1)}", x - 5, y, 3, 1, ' ')
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
        
        loop_cnt += 1
        
        if loop_cnt > 3:
            # Print time left
            if iniVal['Bold']:
                escSetBold(1)
            PrintAtPos(f"{int(timing - (time.time() - start_time) + 1)}", x - 5, y, 3, 1, ' ')
            escResetStyle()
            loop_cnt = 0

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

# Load ini-values from the configuration file
iniVal = LoadSettings(TrainType)

escCursorVisible(0)  # Hide cursor
setEcho(0)  # Disable echo

if iniVal['debug']:
    escCLS()
    print(f"Debug mode is ON. Loaded settings for {TrainType}:\n")
    for key, value in iniVal.items():
        print(f"   {key}: {value}")
    input("\nPress Enter to continue...") 

if iniVal['StartDelay'] > 0:
    # Delay before starting the training
    escCLS()
    run_loop(iniVal['StartDelay'], iniVal['msg_start_delay'], 10, 3)

loop_state = 1  # 1=Start, 2=Main, 3=End
loop_cnt = 0
loop_time = 0
cntMaxDescription = 0
cntDescription = 0
# Get terminal size
term_size = escGetTerminalSize()
term_width = term_size.columns
term_height = term_size.lines

# Training Loop
while loop_state < 4:
    
    escCLS()

    # Text positions
    posTime = term_height - (term_height - 24) - 5
    posAction = term_height - (term_height - 24) - 3
    posRepeat = term_height - (term_height - 24) -2
    offsetX = term_width - 80
    if offsetX < -9:
        offsetX = -9

    # print inverted header
    escSetInverted(1)
    if iniVal['Bold']:
        escSetBold(1)
    strHeader = f"{appName} {appVersion} - {appCopyright} {appAuthor} - {appDate}"
    # Maybe too long
    strHeader = TextToLines(strHeader, term_width)
    # center all lines
    cntHeaderLines = 0
    for i, line in enumerate(strHeader):
        strHeader[i] = CenterText(line, term_width)
        PrintAtPos(strHeader[i], 1, i + 1)
        cntHeaderLines += 1
    escSetInverted(0)

    # print description/placeholder for loop of loop_repeat  &  action_cnt of action_len  &  action time left 
    PrintAtPos("  Time:", offsetX + 10, posTime)
    PrintAtPos("Action:     /    ", offsetX + 10, posAction)
    PrintAtPos("Repeat:     /    ", offsetX + 10, posRepeat)
    escResetStyle()

    # text - actual procedure - Centered double width or standard bold_italic
    if loop_state == 1:
        strProcedure = iniVal['start_procedure']
    elif loop_state == 2:
        strProcedure = iniVal['main_procedure']
    else:
        strProcedure = iniVal['end_procedure']

    # Width - depending on settings DoubleWidth
    if iniVal['DoubleWidth'] or iniVal['SimDoubleWidth']:
        term_width_hlp = term_width // 2
    else:
        term_width_hlp = term_width

    strProcedure = TextToLines(strProcedure, term_width_hlp)
    # Center all lines
    cntProcedureLines = 0
    for i, line in enumerate(strProcedure):
        strProcedure[i] = CenterText(line, term_width_hlp)
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

    if loop_state == 1:
        loop_list = iniVal['start_sequence']
        loop_repeat = iniVal['start_repeat']
    elif loop_state == 2:
        loop_list = iniVal['main_sequence']
        loop_repeat = iniVal['main_repeat']
    else:
        loop_list = iniVal['end_sequence']
        loop_repeat = iniVal['end_repeat']

    for loop in range(loop_repeat):
        # count of elements in loop_list
        action_len = len(loop_list)
        if action_len > 0:
            action_cnt = 0
            # Loop the sequences
            for action in loop_list:
                action_cnt += 1
                if action == 'Bl':
                    action_time = iniVal['blink_time']
                    action_text_long = TextToLines(iniVal['long_blink'], term_width - (10 + offsetX) * 2)
                    action_text = iniVal['short_blink']
                elif action == 'Bu':
                    action_time = iniVal['butterfly_time']
                    action_text_long = TextToLines(iniVal['long_butterfly'], term_width - (10 + offsetX) * 2)
                    action_text = iniVal['short_butterfly']
                elif action == '10':
                    action_time = iniVal['percent10_time']
                    action_text_long = TextToLines(iniVal['long_10percent'], term_width - (10 + offsetX) * 2)
                    action_text = iniVal['short_10percent']
                elif action == '50':
                    action_time = iniVal['percent50_time']
                    action_text_long = TextToLines(iniVal['long_50percent'], term_width - (10 + offsetX) * 2)
                    action_text = iniVal['short_50percent']
                elif action == '80':
                    action_time = iniVal['percent80_time']
                    action_text_long = TextToLines(iniVal['long_80percent'], term_width - (10 + offsetX) * 2)
                    action_text = iniVal['short_80percent']
                else:
                    # Unknown action - fatal error
                    escSetColor(cRed, cBg)
                    PrintAtPos(f"Unknown action: {action} in sequence {strProcedure}", 1, term_height)
                    QuitApp(0)

                # Print the action. Centered - Double height or simulated bold double width

                term_width_hlp = term_width // 2

                action_text = TextToLines(action_text, term_width_hlp)
                # Center all lines
                cntActionLines = 0
                for i, line in enumerate(action_text):
                    action_text[i] = CenterText(line, term_width_hlp)
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
                    PrintAtPos(line, 10 + offsetX, 4 + cntActionLines + cntHeaderLines + cntProcedureLines + i, term_width - (10 + offsetX))
                    cntDescription += 1
                
                if cntDescription > cntMaxDescription:
                    cntMaxDescription = cntMaxDescription
                
                if cntDescription < cntMaxDescription:
                    # Clear the remaining lines
                    for i in range(cntDescription, cntMaxDescription):
                        PrintAtPos(' ', 10 + offsetX, 6 + cntHeaderLines + cntHeaderLines + cntProcedureLines + i, term_width - (10 + offsetX))
                
                escResetStyle()

                # print loop of loop_repeat  &  action_cnt of action_len
                PrintAtPos(action_cnt, 18 + offsetX, posAction, 3, 1, '0')
                PrintAtPos(action_len, 24 + offsetX, posAction, 3, 1, '0')
                PrintAtPos((loop + 1), 18 + offsetX, posRepeat, 3, 1, '0')
                PrintAtPos(loop_repeat, 24 + offsetX, posRepeat, 3, 1, '0')

                # Run the timing loop for the specified time 
                escSetColor(cGreen, cBg)
                loop_time = run_loop(action_time, iniVal['msg_press_enter_space'], 23 + offsetX, posTime)
                escResetColor()

                # Clear the timer - text
                PrintAtPos(' ' * (term_width - (18 + offsetX)), 18 + offsetX, posTime)
                # Clear the action and description
                for i in range(0, cntHeaderLines + cntDescription + cntActionLines + 3):
                    PrintAtPos(' ', 1, 4 + cntHeaderLines + i, term_width)

                if ((action_cnt < action_len) or (loop + 1 < loop_repeat)) and not action == '10' and not action == '50':
                    # Pause between actions
                    escSetColor(cBlue, cBg)
                    if iniVal['automatic']:
                        # PrintAtPos(iniVal['msg_press_enter_space'], 22, term_height - 5 )
                        run_loop(iniVal['auto_delay_time'], iniVal['msg_press_enter_space'], 23 + offsetX, posTime)
                    else:
                        PrintAtPos({iniVal['msg_press_enter']}, 23 + offsetX, posTime)
                    escResetColor()

    # Clear Procedure line
    PrintAtPos(' ' * (term_width - 1), cntHeaderLines, 3, term_width)
    if loop_state < 3:
        # Pause between Procedures (Start -> End)
        if iniVal['automatic']:
            run_loop(int(iniVal['auto_delay_time'] * 1.5), iniVal['msg_press_enter_space'], 23 + offsetX, posTime)
        else:
            PrintAtPos({iniVal['msg_press_enter']}, 23 + offsetX, posTime)


    loop_state += 1

QuitApp()

