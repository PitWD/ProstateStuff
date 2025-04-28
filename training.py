import os
import sys
import configparser
import time
import select

if os.name == 'nt':  # Windows
    import msvcrt
else:  # Linux und MacOS
    import tty
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
appName = "Powerful Prostate & Potence"
appVersion = "0.0.1a"
appAuthor = "github.com/PitWD"
appCopyright = "(c) GPL by"
appDate = "2025-04-27"


# Load Values from INI (quick 'n' dirty, slow but type-safe)
def LoadSettings(TrainType = 'Default'):

    # Define the path to Settings.ini
    config_file_path = os.path.join(os.path.dirname(__file__), 'Settings.ini')

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(config_file_path)

    # Values from Settings.ini
    iniVal = {
        'version': config.get('Global', 'Version' if config.has_option('Global', 'Version') else '0.0.1a'),
        'debug': config.get('Global', 'Debug' if config.has_option('Global', 'Debug') else '1'),
        'blink_time': config.get(TrainType, 'Blink' if config.has_option(TrainType, 'Blink') else '60'),
        'butterfly_time': config.get(TrainType, 'Butterfly' if config.has_option(TrainType, 'Butterfly') else '10'),
        'percent10_time': config.get(TrainType, '10Percent' if config.has_option(TrainType, '10Percent') else '10'),
        'percent50_time': config.get(TrainType, '50Percent' if config.has_option(TrainType, '50Percent') else '10'),
        'percent80_time': config.get(TrainType, '80Percent' if config.has_option(TrainType, '80Percent') else '10'),
        'start_sequence': config.get(TrainType, 'Start' if config.has_option(TrainType, 'Start') else 'Bl_Bu'),
        'start_repeat': config.get(TrainType, 'RepeatStart' if config.has_option(TrainType, 'RepeatStart') else '2'),
        'main_sequence': config.get(TrainType, 'Main' if config.has_option(TrainType, 'Main') else '10_50_80_Bu_10_50_80_Bu_Bl_Bu'),
        'main_repeat': config.get(TrainType, 'RepeatMain' if config.has_option(TrainType, 'RepeatMain') else '3'),
        'end_sequence': config.get(TrainType, 'End' if config.has_option(TrainType, 'End') else ''),
        'end_repeat': config.get(TrainType, 'RepeatEnd' if config.has_option(TrainType, 'RepeatEnd') else '0'),
        'language': config.get('Global', 'Language' if config.has_option('Global', 'Language') else 'EN'),
        'automatic': config.get('Global', 'Automatic' if config.has_option('Global', 'Automatic') else '1'),
        'auto_delay_time': config.get('Global', 'AutoDelayTime' if config.has_option('Global', 'AutoDelayTime') else '0'),
        'DoubleHeight': config.get('Global', 'DoubleHeight' if config.has_option('Global', 'DoubleHeight') else '0'),
        'DoubleWidth': config.get('Global', 'DoubleWidth' if config.has_option('Global', 'DoubleWidth') else '0'),
        'Bold': config.get('Global', 'Bold' if config.has_option('Global', 'Bold') else '0'),
        'Italic': config.get('Global', 'Italic' if config.has_option('Global', 'Italic') else '0'),
        'Underline': config.get('Global', 'Underline' if config.has_option('Global', 'Underline') else '0')
    }

    # Define the path to Language.ini
    config_file_path = os.path.join(os.path.dirname(__file__), 'Language.ini')
    # config = configparser.ConfigParser()
    config.read(config_file_path)

    # Get Language
    iniVal['language'] = iniVal['language'].strip('"')
    LangShort = 'ActionShort' + iniVal['language']
    LangLong = 'ActionLong' + iniVal['language']
    LangProcedure = 'Procedures' + iniVal['language']
    LangMessage = 'Messages' + iniVal['language']

    # Values from Language.ini
    lang_values = {
        'short_blink': config.get(LangShort, 'Blink' if config.has_option(LangShort, 'Blink') else 'Blink'),
        'short_butterfly': config.get(LangShort, 'Butterfly' if config.has_option(LangShort, 'Butterfly') else 'Butterfly/Windshield Wiper'),
        'short_10percent': config.get(LangShort, 'Percent10' if config.has_option(LangShort, 'Percent10') else '10% Tension'),
        'short_50percent': config.get(LangShort, '50Percent' if config.has_option(LangShort, '50Percent') else '50% Tension'),
        'short_80percent': config.get(LangShort, '80Percent' if config.has_option(LangShort, '80Percent') else '80% Tension'),
        'long_blink': config.get(LangLong, 'Blink' if config.has_option(LangLong, 'Blink') else 'Tighten/Relax - As if you want to interrupt minimal urine flow.'),
        'long_butterfly': config.get(LangLong, 'Butterfly' if config.has_option(LangLong, 'Butterfly') else 'Relaxed left and right, or opening and closing the legs as if suppressing the urge to urinate.'),
        'long_10percent': config.get(LangLong, '10Percent' if config.has_option(LangLong, '10Percent') else 'Hold the tension like Blinking - As if you want to interrupt minimal urine flow.'),
        'long_50percent': config.get(LangLong, '50Percent' if config.has_option(LangLong, '50Percent') else 'Hold the tension like 50% Tension - As if you want to interrupt medium urine flow.'),
        'long_80percent': config.get(LangLong, '80Percent' if config.has_option(LangLong, '80Percent') else 'Hold the tension like 80% Tension - As if you want to interrupt strong urine flow. The anal sphincter is only activated here.'),
        'start_procedure': config.get(LangProcedure, 'Start' if config.has_option(LangProcedure, 'Start') else 'Start procedure'),
        'main_procedure': config.get(LangProcedure, 'Main' if config.has_option(LangProcedure, 'Main') else 'Main procedure'),
        'end_procedure': config.get(LangProcedure, 'End' if config.has_option(LangProcedure, 'End') else 'End procedure'),
        'msg_press_enter': config.get(LangMessage, 'PressEnter' if config.has_option(LangMessage, 'PressEnter') else 'Press Enter to continue...'),
        'msg_press_enter_space': config.get(LangMessage, 'PressEnterSpace' if config.has_option(LangMessage, 'PressEnterSpace') else 'Press ENTER to cancel, SPACE to pause')
    }

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
    # Bool values to boolean
    iniVal['automatic'] = bool(int(iniVal['automatic']))
    iniVal['debug'] = bool(int(iniVal['debug']))
    iniVal['DoubleHeight'] = bool(int(iniVal['DoubleHeight']))
    iniVal['DoubleWidth'] = bool(int(iniVal['DoubleWidth']))
    iniVal['Bold'] = bool(int(iniVal['Bold']))
    iniVal['Italic'] = bool(int(iniVal['Italic']))
    iniVal['Underline'] = bool(int(iniVal['Underline']))
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
    # Make lists from sequences (" " and "_" are legal separators)
    iniVal['start_sequence'] = iniVal['start_sequence'].replace(' ', '_').split('_')
    iniVal['main_sequence'] = iniVal['main_sequence'].replace(' ', '_').split('_')
    iniVal['end_sequence'] = iniVal['end_sequence'].replace(' ', '_').split('_')

    return iniVal

# Look for Keypress - returns key or "" (to esc.py)
def GetKeyPress():
    """
    Non-blocking key press detection.
    Returns the pressed key or an empty string if no key is pressed.
    """
    if os.name == 'nt':  # Windows
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
    else:  # Linux and macOS
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Check if input is available
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ""

# Clear the console (to esc.py)
def escCLS():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux and MacOS
        os.system('clear')

# Set cursor position (to esc.py)
def escSetCursorPos(x, y):
    #if os.name == 'nt':  # Windows
        #os.system(f'echo \033[{y};{x}H')
    #else:  # Linux and MacOS
    print(f'\033[{y};{x}H', end='', flush=True)

# Set cursor color - 16 Colors (to esc.py)
def escSetColor(fg, bg):
    #if os.name == 'nt':  # Windows
     #   os.system(f'echo \033[{30 + (fg % 8)}m\033[{40 + (bg % 8)}m')
      #  if fg >= 8:  # Bright foreground
       #     os.system('echo \033[1m')
        #if bg >= 8:  # Bright background
         #   os.system('echo \033[5m')  # Optional: Blink for bright background
    #else:  # Linux and MacOS
    print(f'\033[{30 + (fg % 8)}m\033[{40 + (bg % 8)}m', end='', flush=True)
    if fg >= 8:  # Bright foreground
        print('\033[1m', end='', flush=True)
    if bg >= 8:  # Bright background
        print('\033[5m', end='', flush=True)  # Optional: Blink for bright background

# Set cursor color - 255 Colors (to esc.py)
def escSet255Color(fg, bg):
    #if os.name == 'nt':  # Windows
     #   os.system(f'echo \033[38;5;{fg}m\033[48;5;{bg}m')
    #else:  # Linux and MacOS
    print(f'\033[38;5;{fg}m\033[48;5;{bg}m', end='', flush=True)

# Reset colors to terminal standard (to esc.py)
def escResetColor():
    #if os.name == 'nt':  # Windows
     #   os.system('echo \033[0m')
    #else:  # Linux and MacOS
    print('\033[0m', end='', flush=True)

# Get Terminal Size (to esc.py)
def escGetTerminalSize():
    return os.get_terminal_size()


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
    if os.name == 'nt':  # Windows
        os.system(f'echo \033#{state}')
    else:  # Linux and MacOS
        os.system(f'\033#{state}')
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
            # Right align the text
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

# Run loop for 'time' seconds - return runtime
def run_loop(timing):
    # Space pauses/continues the loop
    # Enter stops the loop - return 0
    timing = float(timing)
    start_time = time.time()
    term_size = escGetTerminalSize()
    term_width = term_size.columns
    term_height = term_size.lines
    loop_cnt = 0

    while time.time() - start_time < timing:
        time.sleep(0.05)
        key = GetKeyPress()
        if key == ' ':
            pause_time = time.time()
            while True:
                time.sleep(0.05)
                key = GetKeyPress()
                if key == ' ':
                    break
                elif key == '\n':
                    return 0
            start_time += time.time() - pause_time
        elif key == '\n':
            return 0
        loop_cnt += 1
        if loop_cnt > 4:
            if iniVal['Bold']:
                escSetBold(1)
            PrintAtPos(f"{int(timing - (time.time() - start_time))}", 17, term_height - 5, 3, 1, ' ')
            escResetStyle()
            loop_cnt = 0
    return time.time() - start_time


# Main program

# Get parameters from the command line
if len(sys.argv) > 1:
    TrainType = sys.argv[1]
else:
    TrainType = 'Default'

# Load ini-values from the configuration file
iniVal = LoadSettings(TrainType)

if iniVal['debug']:
    escCLS()
    print(f"Debug mode is ON. Loaded settings for {TrainType}:\n")
    for key, value in iniVal.items():
        print(f"   {key}: {value}")
    input("\nPress Enter to continue...") 

loop_state = 1  # 1=Start, 2=Main, 3=End
loop_cnt = 0
loop_time = 0
loop_max_description = 0
loop_act_description = 0

while loop_state > 0 and loop_state < 4:
    escCLS()
    # Get terminal size
    term_size = escGetTerminalSize()
    term_width = term_size.columns
    term_height = term_size.lines
    
    # print inverted header
    escSetInverted(1)
    escSetBold(1)
    strHeader = f"{appName} {appVersion} - {appCopyright} {appAuthor} - {appDate}"
    strHeader = CenterText(strHeader, term_width)
    PrintAtPos(strHeader, 0, 0)
    escSetInverted(0)

    # print loop of loop_repeat  &  action_cnt of action_len  &  action time left 
    if iniVal['Bold']:
        escSetBold(1)
    PrintAtPos("  Time:", 9, term_height - 5)
    PrintAtPos("Action:     /    ", 9, term_height - 3)
    PrintAtPos("Repeat:     /    ", 9, term_height - 2)
    escResetStyle()

    # print procedure
    if loop_state == 1:
        strProcedure = iniVal['start_procedure']
    elif loop_state == 2:
        strProcedure = iniVal['main_procedure']
    else:
        strProcedure = iniVal['end_procedure']
    strProcedure = CenterText(strProcedure, term_width)
    if iniVal['Bold']:
        escSetBold(1)
    if iniVal['Italic']:
        escSetItalic(1)
    if iniVal['Underline']:
        escSetUnderline(1)
    PrintAtPos(strProcedure, 0, 3, term_width)
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
                    action_text_long = TextToLines(iniVal['long_blink'], term_width - 20)
                    action_text = iniVal['short_blink']
                elif action == 'Bu':
                    action_time = iniVal['butterfly_time']
                    action_text_long = TextToLines(iniVal['long_butterfly'], term_width - 20)
                    action_text = iniVal['short_butterfly']
                elif action == '10':
                    action_time = iniVal['percent10_time']
                    action_text_long = TextToLines(iniVal['long_10percent'], term_width - 20)
                    action_text = iniVal['short_10percent']
                elif action == '50':
                    action_time = iniVal['percent50_time']
                    action_text_long = TextToLines(iniVal['long_50percent'], term_width - 20)
                    action_text = iniVal['short_50percent']
                elif action == '80':
                    action_time = iniVal['percent80_time']
                    action_text_long = TextToLines(iniVal['long_80percent'], term_width - 20)
                    action_text = iniVal['short_80percent']
                else:
                    # Unknown action - fatal error
                    escSetColor(cRed, cBg)
                    PrintAtPos(f"Unknown action: {action} in sequence {strProcedure}", 0, term_height - 1)
                    escResetColor()
                    sys.exit(1)

                # Print the action
                strAction = CenterText(action_text, term_width)
                if iniVal['Bold']:
                    escSetBold(1)
                PrintAtPos(strAction, 0, 5)
                escResetStyle()

                # Print the description
                loop_act_description = 0
                if iniVal['Italic']:
                    escSetItalic(1)
                for i, line in enumerate(action_text_long):
                    PrintAtPos(line, 9, 6 + i, term_width - 10)
                    loop_act_description += 1
                
                if loop_act_description > loop_max_description:
                    loop_max_description = loop_act_description
                
                if loop_act_description < loop_max_description:
                    # Clear the remaining lines
                    for i in range(loop_act_description, loop_max_description):
                        PrintAtPos(' ', 9, 6 + i, term_width - 10)
                escResetStyle()

                # print loop of loop_repeat  &  action_cnt of action_len

                PrintAtPos(action_cnt, 17, term_height - 3, 3, 1, '0')
                PrintAtPos(action_len, 23, term_height - 3, 3, 1, '0')
                PrintAtPos((loop + 1), 17, term_height - 2, 3, 1, '0')
                PrintAtPos(loop_repeat, 23, term_height - 2, 3, 1, '0')

                # Run the timing loop for the specified time
                loop_time = run_loop(action_time)

                # Clear the timer - text
                PrintAtPos(' ' * (term_width - 18), 17, term_height - 5 )

                if iniVal['automatic']:
                    PrintAtPos(iniVal['msg_press_enter_space'], 22, term_height - 5 )
                    run_loop(iniVal['auto_delay_time'])
                else:
                    PrintAtPos({iniVal['msg_press_enter']}, 17, term_height - 5 )

                PrintAtPos(" " * (term_width - 18), 17, term_height - 5 )
                                  
    loop_state += 1


