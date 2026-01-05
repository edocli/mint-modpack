import re
import subprocess
import os
import sys

INPUT_FILE = '1.txt'

def install_mods():
    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到文件 {INPUT_FILE}")
        return

    # 检查 pack.toml 是否存在
    if not os.path.exists("pack.toml"):
        print("❌ 错误: 当前目录下没有 pack.toml 文件！")
        print("请先执行初始化命令，例如: packwiz init --fabric --mc-version 1.20.1")
        return

    url_pattern = re.compile(r'\((https?://[^\)]+)\)')

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"📦 准备安装 {len(lines)} 个模组...")

    success_count = 0
    fail_count = 0

    for index, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        match = url_pattern.search(line)
        if not match:
            continue

        url = match.group(1)
        mod_name = line.split('(')[0].strip()
        
        command = []
        if "modrinth.com" in url:
            command = ["packwiz", "mr", "add", url]
        elif "curseforge.com" in url:
            command = ["packwiz", "cf", "add", url]
        else:
            continue

        print(f"\n[{index+1}/{len(lines)}] 正在安装: {mod_name} ...")
        
        # === 优化部分：实时输出，防止卡死 ===
        try:
            # 不捕获输出，直接让 packwiz 打印到终端
            # 这样如果它问问题，你可以看到（虽然脚本很难交互，但至少你知道它卡在哪）
            process = subprocess.run(command, text=True)
            
            if process.returncode == 0:
                print(f"✅ {mod_name} 安装成功")
                success_count += 1
            else:
                print(f"❌ {mod_name} 安装失败 (可能没有适配 1.20.1 的版本)")
                fail_count += 1
                
        except KeyboardInterrupt:
            print("\n⛔ 用户手动终止脚本。")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 发生异常: {e}")

    print(f"\n🎉 任务结束! 成功: {success_count}, 失败: {fail_count}")
    print("提示: 失败的模组通常是因为该作者还没发布 1.20.1 Fabric 版本，或者链接已失效。")

if __name__ == "__main__":
    install_mods()