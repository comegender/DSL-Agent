import backend.script_achieve as sa
from frontend.terminal_ui import TUIManager

if __name__ == "__main__":
    tui = TUIManager()
    tui.show_welcome()
    
    sa.jump_statement('begin')