import backend.script_achieve as sa
from frontend.terminal_ui import TUIManager
import backend.test_script as ts

if __name__ == "__main__":
    tui = TUIManager()
    tui.show_welcome()
    print("🤖：请选择业务场景：")
    print("1. 账号管理\n2. 医院挂号\n3. 餐厅点餐")
    choice = input("请输入选项编号（1-3）：")
    while choice not in ['1', '2', '3']:
        choice = input("无效输入，请重新输入选项编号（1-3）：")
    ts.set_mode(int(choice))
    sa.jump_statement('begin')