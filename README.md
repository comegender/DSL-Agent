# 智能客服机器人 DSL 解释器

## 项目简介

该项目旨在设计并实现一种领域特定语言（DSL），用于描述智能客服机器人的应答逻辑。通过结合传统的规则引擎与前沿的大型语言模型（LLM）API，该系统能够理解用户的自然语言输入，识别其意图，并根据预定义的DSL脚本自动执行相应的应答流程。

本项目的核心价值在于提供了一个灵活、可配置的框架，允许非技术人员（如客服运营专家）通过编写简单的DSL脚本来定制和扩展客服机器人的功能，而无需修改底层的程序代码。

## 核心功能

1.  **DSL设计**：定义了一套简洁、直观的语法，用于描述对话流程、条件判断、变量赋值和外部函数调用。
2.  **解释器实现**：开发了一个完整的解释器，能够对DSL脚本进行词法分析、语法分析和执行。
3.  **意图识别**：集成了LLM API（如豆包），能够将用户的自然语言输入映射到DSL脚本中定义的具体意图或操作。
4.  **多业务场景支持**：通过编写不同的DSL脚本，可以轻松实现如用户登录、账户查询、业务咨询、投诉建议等多种客服场景。
5.  **命令行交互界面**：提供了一个简单的命令行界面（TUI），用于模拟用户与客服机器人的交互。

## 技术架构

1.  **前端交互层 (TUI Manager)**：负责接收用户输入并展示机器人的回复，提供基本的交互体验。
2.  **意图识别层 (AI API Client)**：封装了对LLM API的调用。它接收用户的原始输入，通过API请求获得标准化的意图识别结果，为解释器提供明确的执行入口。
3.  **核心解释器层 (Interpreter)**：
    *   **词法分析器 (Lexical Analyzer / Lexer)**：负责将DSL脚本的字符串流转换为一个个有意义的单词（Token），如关键字、变量名、字符串等。
    *   **语法分析器 (Syntactic Analyzer / Parser)**：在词法分析的基础上，根据DSL的语法规则，将Token序列构建成一个抽象语法树（AST）。
    *   **执行引擎 (Execution Engine)**：遍历并执行AST，负责维护执行上下文（如变量表）、处理流程控制（如`if-else`, `jump`）以及调用业务逻辑接口。
4.  **业务逻辑层 (Business Logic Interface)**：提供了一系列函数接口，用于执行具体的业务操作，如查询数据库、调用其他服务等。解释器通过`call`关键字来触发这些操作。

## 快速开始

### 1. 环境准备

*   **Python 3.8+**
*   安装依赖库:
    ```bash
    pip install ply requests
    ```
*   **LLM API Key**: 你需要拥有一个豆包（或其他支持的LLM）的API密钥，并将其配置在项目中。

### 2. 配置API密钥

将你的API密钥填入 `config.py` 文件中：
```python
# config.py
API_KEY = "你的API密钥"
API_URL = "https://api.doubao.com/v1/chat/completions" # 示例URL，请根据实际情况修改
```

### 3. 运行程序

在项目根目录下，通过以下命令启动客服机器人：
```bash
python main.py
```
启动后，你将看到一个命令行提示符，可以开始与机器人进行对话。

## DSL脚本编写指南

### 语法概览

DSL脚本由一系列**行为块 (Behavior Block)** 组成。每个行为块定义了一个独立的对话流程。

#### 1. 行为块定义

```dsl
do [行为块名称] {
    // 指令列表
}
```
*   `do`: 关键字，用于定义一个行为块。
*   `[行为块名称]`: 例如 `login`, `query_balance`, `handle_complaint`。这也是LLM意图识别后需要匹配的目标。
*   `{...}`: 花括号内包含了该行为块的执行指令。

#### 2. 核心指令

*   **`speak "文本内容"`**: 让机器人向用户发送指定的文本消息。
    ```dsl
    speak "你好！有什么可以帮助你的吗？"
    ```

*   **`set [变量名] = [表达式]`**: 用于赋值。`@content@` 是一个特殊变量，代表用户的最新输入内容。
    ```dsl
    set username = @content@  // 将用户输入的内容赋值给变量 username
    set is_vip = true         // 赋值布尔值
    set greeting = "欢迎, " + username  // 字符串拼接
    ```

*   **`call [函数名]([参数列表])`**: 调用一个预定义的业务逻辑函数。函数的返回值可以被赋值给变量。
    ```dsl
    set login_result = call check_credentials(username, password)
    call save_complaint(user_id, complaint_text) // 调用无返回值的函数
    ```

*   **`if ([条件表达式]) { ... } else { ... }`**: 条件判断语句，用于实现分支逻辑。
    ```dsl
    if (login_result == "success") {
        speak "登录成功！"
    } else {
        speak "用户名或密码错误，请重试。"
    }
    ```

*   **`jump [行为块名称]`**: 流程跳转指令，用于中断当前行为块的执行，并跳转到指定的行为块。
    ```dsl
    jump main_menu  // 跳转到名为 main_menu 的行为块
    ```

### 脚本示例

下面是一个处理用户投诉的完整DSL脚本示例 (`complaint.dsl`)：

```dsl
// 定义处理投诉的行为块
do handle_complaint {
    speak "很抱歉给您带来不好的体验。请详细描述一下您的问题，我们会尽快处理。";
    
    // 等待用户输入，并将输入内容存入 complaint_content 变量
    set complaint_content = @content@;
    
    // 调用业务函数，将投诉内容保存到数据库
    // 假设当前已登录用户的ID存储在全局变量 user_id 中
    call save_complaint(user_id, complaint_content);
    
    speak "您的投诉内容已收到，我们的工作人员将在24小时内与您联系。";
    speak "请问还有其他可以帮助您的吗？";
    
    // 跳转到主菜单行为块，等待用户的下一个指令
    jump main_menu;
}

// 定义主菜单行为块
do main_menu {
    speak "请选择服务：1. 账户查询 2. 业务办理 3. 投诉建议"
    // 后续逻辑可以根据用户输入的数字进行分支
}
```

## 测试

项目包含了一套完整的测试用例，用于验证解释器各模块的正确性。

```bash
# 运行所有测试
python -m pytest tests/ -v
```

## 开发与贡献

1.  **Fork**本仓库
2.  创建你的开发分支 (`git checkout -b feature/amazing-feature`)
3.  提交你的修改 (`git commit -m 'Add some amazing feature'`)
4.  推送到分支 (`git push origin feature/amazing-feature`)
5.  打开一个**Pull Request**

## 许可证

本项目采用 [MIT License](LICENSE) - 详见 LICENSE 文件。
