# biliM4sVideoConerter
一款轻量级 Windows GUI 工具，专注于处理bilibili视频平台的 M4S 分片文件。支持拖放或手动选择包含两个 M4S 文件的文件夹，自动转换缓存的M4S文件为MP3和MP4格式文件，解决 M4S 文件无法直接播放的问题。

##   **一、项目简介**
​
M4S 文件是视频平台（B站）的分片加密文件，单个 M4S 文件无法直接播放，需与另一个关联 M4S 文件合并并删除头部加密字节后才能还原视频并播放。本工具专为简化这一操作设计，提供图形化界面，支持拖放或手动选择文件夹，自动完成以下操作：

- 检测文件夹内是否包含 ​**恰好两个 .m4s 文件**；
- 按文件大小排序（小文件为音频，大文件为视频）；
- 自动创建 `ending`子文件夹并保存处理后的文件（`audio.mp3`和 `video.mp4`）
- 将两个m4s文件自动转换为mp3和mp4文件
    

## ​**二、功能特性**​

- ​**图形化操作**​：基于 Tkinter 开发，界面简洁易用，支持拖放文件夹或手动选择路径；
    
- ​**自动检测**​：严格校验文件夹内 M4S 文件数量（需恰好 2 个），避免误操作；
    
- ​**轻量高效**​：纯 Python 实现，无冗余依赖，打包后 exe 体积小巧（约 10MB）；
    
- ​**错误提示**​：详细的异常捕获与提示（如文件缺失、数量不符、处理失败等）。
    

## ​**三、使用说明**​

### ​**1. 运行环境**​

- ​**操作系统**​：Windows 10/11（推荐，其他系统需自行适配）；
    
- ​**Python 版本**​：推荐Python 3.12 及以上（需安装依赖库）；
    
- ​**依赖库**​：`tkinter`（系统自带）、`tkinterdnd2`、`shutil`（系统自带）。
    

### ​**2. 安装与运行**​

#### ​**方式 1：直接运行 Python 脚本**​

1. 安装依赖：
    
    ```
    pip install tkinterdnd2
    ```
    
2. 下载本项目代码，进入 `M4S Video Converter`文件夹；
    
3. 双击运行 `main.py`（或通过命令行执行 `python main.py`）。

#### ​**方式 2：打包为独立 exe（推荐分发）​**​

1. 安装 PyInstaller：
    
    ```
    pip install pyinstaller
    ```
    
2. 下载 UPX 压缩工具并解压（可选，用于减小 exe 体积）；
    
3. 执行打包命令（替换 `UPX路径`为实际路径）：
    
    ```
    pyinstaller -F -w -i bilibili.ico --name "biliM4sVideoConerter" --hidden-import=tkinterdnd2 --hidden-import=tkdnd --exclude-module=fastapi --exclude-module=pydantic --exclude-module=scikit-learn --exclude-module=scipy --exclude-module=uvicorn --exclude-module=annotated-types --exclude-module=anyio --exclude-module=idna --exclude-module=joblib --exclude-module=packaging --exclude-module=pefile --exclude-module=sniffio --exclude-module=starlette --exclude-module=threadpoolctl --exclude-module=typing-inspection --upx-dir="UPX路径" --clean main.py
    ```
    
4. 打包完成后，`dist`文件夹中生成 `biliM4sVideoConerter.exe`，双击即可运行。
    

### ​**3. 操作步骤**
**教程链接：**https://www.bilibili.com/video/BV1i7JyzEE7m/?vd_source=877f1d3fe92b481ee490720c4c7efc40​

1. ​**选择文件夹**​：
    - 进入哔哩哔哩缓存视频
    
    - 点击哔哩哔哩的设置->找到视频文件缓存目录

    - 哔哩哔哩的视频文件夹为缓存目录下的纯数字目录，一个纯数字目录代表一个视频缓存文件夹（特征为文件夹内会包含两个m4s后缀的文件）

    - 找到要转换的视频文件夹
    
    - 拖放包含两个 .m4s 文件的文件夹到工具窗口的拖放区域；
        
    - 或点击「选择视频文件夹」按钮手动选择路径。
        
    
2. ​**确认路径**​：工具会显示选中的文件夹路径，确保路径正确。
    
3. ​**开始处理**​：点击「开始处理」按钮，工具会自动完成以下操作：
    
    - 检测文件夹内 .m4s 文件数量（需恰好 2 个）；
        
    - 创建 `ending`子文件夹；
        
    - 复制并处理两个 .m4s 文件；
        
    - 生成 `audio.mp3`（音频）和 `video.mp4`（视频）到 `ending`文件夹。
        
    
4. ​**查看结果**​：处理完成后弹出提示，可到 `ending`文件夹查看输出文件。
    

## ​**四、注意事项**​

- ​**文件要求**​：仅支持处理 ​**恰好两个 .m4s 文件**​ 的文件夹（常见于 B站等平台的视频分片）；
    
- ​**加密头差异**​：若处理后文件仍无法播放，可能是加密头长度非 9 字节（需自行调整代码中 `n=9`的值）；
    
- ​**权限问题**​：若提示「无权限访问文件」，请以管理员身份运行工具；
    

## ​**五、贡献与反馈**​

- ​**Issue 提交**​：若遇到 bug 或功能需求，可在 GitHub Issues提交详细描述；
    
- ​**PR 提交**​：欢迎提交代码改进（如新增功能、优化界面、修复 bug 等），需附测试说明；
    
- ​**联系方式**​：可通过邮箱（你的邮箱）或 GitHub 私信联系开发者。
    

## ​**六、许可证**​

本项目采用 ​**MIT 开源许可证**，允许自由使用、修改和分发，只需保留原版权声明。

​**项目仓库**​：https://github.com/你的用户名/M4S-Video-Converter（替换为实际仓库链接）


## 声明：
本项目仅供学习python的可视化界面开发以及项目打包成exe文件使用，请勿用于非法途径！
