import time
import sys
import rich.console
import rich.layout
import rich.panel
import rich.text
import rich.live
import rich.progress
import rich.table
import rich.box

# 使用完整的模块路径来避免循环导入
console = rich.console.Console()

class TUIManager:
    def __init__(self):
        self.title = "📱 奶小龙智能助手"
        self.subtitle = "✨ 您的贴心生活小帮手"
        self.width = console.width - 4  # 预留边距
        self.separator = "=" * self.width

    def clear_screen(self):
        """清空屏幕"""
        console.clear()

    def print_header(self):
        """打印头部标题面板"""
        header_content = rich.text.Text()
        header_content.append(f"{self.title}\n", style="bold cyan")
        header_content.append(self.subtitle, style="green")
        
        panel = rich.panel.Panel(
            header_content,
            box=rich.box.ROUNDED,
            border_style="bright_blue",
            style="on black",
            padding=(1, 2)
        )
        console.print(panel)

    def print_status_bar(self, message):
        """显示底部状态条"""
        status_panel = rich.panel.Panel(
            f" {message} ",
            box=rich.box.ROUNDED,
            border_style="bright_blue",
            style="white on bright_blue",
            height=3
        )
        console.print(status_panel)

    def print_bubble(self, speaker, content, is_user=False):
        """显示对话气泡"""
        # 文本自动换行处理
        wrapped_content = console.render_str(content).wrap(console, width=self.width - 10)
        content_text = "\n".join(wrapped_content)
        
        if is_user:
            # 用户气泡（右对齐）- 修改为蓝色边框
            panel = rich.panel.Panel(
                content_text,
                title=speaker,
                title_align="right",
                box=rich.box.ROUNDED,
                border_style="bright_blue",
                style="on black",
                padding=(1, 2)
            )
            console.print(panel, justify="right")
        else:
            # 助手气泡（左对齐）- 修改为黄色边框
            panel = rich.panel.Panel(
                content_text,
                title=speaker,
                title_align="left",
                box=rich.box.ROUNDED,
                border_style="bright_yellow",
                style="on black",
                padding=(1, 2)
            )
            console.print(panel, justify="left")
        console.print()

    def print_loading(self, message, duration=1.5):
        """显示加载动画"""
        with rich.progress.Progress(
            rich.progress.SpinnerColumn(),
            rich.progress.TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description=message, total=None)
            end_time = time.time() + duration
            while time.time() < end_time:
                progress.update(task, advance=0.1)
                time.sleep(0.1)
        console.print(f"[green]{message} 完成!")

    def print_feature_list(self, features):
        """用表格显示功能列表"""
        table = rich.table.Table(
            title="支持的功能",
            box=rich.box.ROUNDED,
            border_style="bright_yellow",
            expand=True
        )
        
        # 根据功能数量动态创建列
        col_count = 3
        for _ in range(col_count):
            table.add_column(justify="center", style="cyan")
        
        # 填充表格数据
        row = []
        for i, feature in enumerate(features, 1):
            row.append(f"• {feature}")
            if i % col_count == 0:
                table.add_row(*row)
                row = []
        if row:  # 处理剩余项
            while len(row) < col_count:
                row.append("")
            table.add_row(*row)
        
        console.print(table)

    def show_welcome(self):
        """显示欢迎界面"""
        self.clear_screen()
        self.print_header()
        
        welcome_msg = "欢迎使用奶小龙智能助手"
        with rich.live.Live(console=console, transient=True) as live:
            for i in range(len(welcome_msg) + 1):
                text = rich.text.Text(welcome_msg[:i], style="bold magenta")
                live.update(rich.panel.Panel(text, box=rich.box.ROUNDED, padding=(1, 2)))
                time.sleep(0.2)
        
        console.print()
        
        features = [
            "投诉建议", "使用帮助", "修改密码",
            "查询账户信息", "充值", "登录", "注册"
        ]
        self.print_feature_list(features)
        
        self.print_status_bar("系统初始化中...")
        self.print_loading("正在准备服务")


    def show_exit_animation(self):
        """显示退出动画"""
        self.clear_screen()
        self.print_header()
        
        exit_messages = [
            "感谢使用奶小龙智能助手",
            "期待下次为您服务",
            "再见！👋"
        ]
        
        for i, msg in enumerate(exit_messages):
            text = rich.text.Text()
            text.append(" " * ((self.width - len(msg)) // 2), style="white")
            text.append(msg, style="bold cyan" if i == 0 else "green")
            
            panel = rich.panel.Panel(
                text,
                box=rich.box.ROUNDED,
                border_style="bright_blue",
                style="on black",
                padding=(1, 2)
            )
            console.print(panel)
            time.sleep(0.8)
        
        with rich.progress.Progress(
            rich.progress.BarColumn(),
            rich.progress.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            rich.progress.MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("正在安全退出...", total=100)
            
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.02)
        
        for _ in range(3):
            console.print("✨", end="", style="yellow")
            time.sleep(0.3)
            console.print("🌟", end="", style="cyan")
            time.sleep(0.3)
        
        console.print("\n\n[bold green]已安全退出奶小龙智能助手！[/bold green]")
        time.sleep(0.5)