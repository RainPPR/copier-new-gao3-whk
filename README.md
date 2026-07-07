# copier-new-gao3-whk

新高三用的考课件的东西

uv run nuitka main.py --standalone --enable-plugin=tk-inter --zig

uv run --python=3.13 pyinstaller --noupx --onefile --name copier-new-gao3-whk-313 --clean --uac-admin --hidden-import=allpath --hidden-import=ignore main.py
uv run --python=3.8 pyinstaller --noupx --onefile --name copier-new-gao3-whk-38 --clean --uac-admin --hidden-import=allpath --hidden-import=ignore main.py

uv run --python=3.8 pyinstaller --noupx --onedir --name copier-new-gao3-whk-38 --clean --uac-admin --hidden-import=allpath --hidden-import=ignore main.py

## PyInstaller 打包方案

由于 Nuitka 打包的 exe 在学校老系统上可能因缺少特定运行时库或系统兼容性导致无法运行，现改用 PyInstaller 重新打包。PyInstaller 自带 Python 运行时与依赖库，通常旧系统兼容性更好，但需按需求选择对应参数。

### 基础打包指令

```bash
pyinstaller --onefile --noconsole --name copier-new-gao3-whk --hidden-import=allpath --hidden-import=ignore main.py
```

### 参数释义

| 参数 | 作用 |
|------|------|
| `--onefile` | 将所有内容打包为**单个** `.exe` 文件，方便拷贝到别的电脑 |
| `--noconsole` | 程序启动时不显示 CMD 黑框（GUI 程序必加） |
| `--name` | 指定最终输出的可执行文件名 |
| `--hidden-import` | 显式声明本地模块 `allpath` 和 `ignore`，防止 PyInstaller 的自动分析漏掉 |

### 进阶 / 按需开启的参数

| 参数 | 说明 |
|------|------|
| `--windowed` | 与 `--noconsole` 等价，作用相同，二选一即可 |
| `--onedir` | 与 `--onefile` 相反，打包成**文件夹**（内有很多 `.dll`/`.pyd`），冷启动比单文件更快，且运行时不需要临时解压 |
| `--clean` | 每次打包前清空之前的构建缓存，避免旧配置残留导致奇怪问题 |
| `--add-data "src;dst"` | 如果程序需要读写额外的非 `.py` 文件（如配置文件、模板、数据库等），用这个参数把它一起打包进去。Windows 用 `;` 分隔，格式为 `"源路径;目标路径"` |
| `--icon=icon.ico` | 指定 `.exe` 的图标 |
| `--target-architecture 32bit` / `--target-architecture 64bit` | **重要！** 如果学校电脑是 32 位 Windows，必须用 32 位 Python 打包并使用此参数 |
| `--uac-admin` | 打包后的程序以管理员身份运行（如果涉及 U 盘拷贝到系统目录可能需要） |
| `--upx-dir path` / `--upx-exclude dllname` | 开启或排除 UPX 压缩，UPX 能减小体积，但在某些老系统上可能导致被杀毒误报 |

### 推荐的几种用法

**1. 最稳妥（文件夹模式，不用解压，兼容最好）：**

```bash
pyinstaller --onedir --noconsole --clean --name copier-new-gao3-whk --hidden-import=allpath --hidden-import=ignore main.py
```

**2. 单文件但保留调试窗口（排查问题时用）：**

```bash
pyinstaller --onefile --clean --name copier-new-gao3-whk --hidden-import=allpath --hidden-import=ignore main.py
```

**3. 单文件、图标、最精简：**

```bash
pyinstaller --onefile --noconsole --clean --name copier-new-gao3-whk --hidden-import=allpath --hidden-import=ignore --icon=icon.ico main.py
```

**4. 兼容旧系统的单文件版本（如果怀疑是位数问题）：**

- 需要先安装 32 位 Python，然后在该 Python 环境下执行：

```bash
pyinstaller --onefile --noconsole --clean --name copier-new-gao3-whk --hidden-import=allpath --hidden-import=ignore --target-architecture 32bit main.py
```

### 常见问题排查

- **缺少 DLL / 启动报错**：先用 `--onedir` 模式打一次包，然后运行生成的 `.exe`。如果这样没问题而 `--onefile` 有问题，通常是解压路径或杀毒软件拦截。
- **杀毒软件报毒**：单文件 PyInstaller 产物较容易被误报，可尝试 `--upx-exclude vcruntime140.dll` 关闭 UPX 压缩，或改用 `--onedir`。
- **tkinter 界面出不来**：确保加了 `--noconsole` 或 `--windowed`，因为无 GUI 的终端模式可能导致 tkinter 事件循环异常。
- **学校电脑 Win7 仍无法运行**：Python 3.10+ 官方已不支持 Windows 7。如果确认学校是 Win7，建议安装 Python 3.8（或 3.9）再重新打包。
