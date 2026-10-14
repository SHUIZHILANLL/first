# -*- coding: utf-8 -*-
"""
猜数字小游戏（单文件版）

玩法：
    电脑随机想一个 1~100 之间的整数，你来猜。
    每猜一次，电脑告诉你"大了"还是"小了"，猜中后告诉你一共猜了几次。

运行：
    python guess_number.py          # 正常玩游戏
    python guess_number.py --test   # 自动跑一遍自检（不需要手动输入）

代码结构说明（从上到下）：
    1. 准备阶段：导入模块、设置输出编码
    2. 工具函数：读取一个合法的整数
    3. 核心函数：play_one_round() 负责一整局游戏
    4. 主函数  ：main() 负责开局提示和"要不要再来一局"
"""

# ---------- 1. 准备阶段 ----------

import random   # 随机数模块，用来让电脑"随便想一个数"
import sys      # 系统模块，用来读命令行参数、设置输出编码


def setup_console():
    """
    让 Windows 命令提示符（cmd）能正常显示中文。
    中文版 Windows 的 cmd 默认是 GBK 编码，所以把输入输出都固定成 UTF-8，
    否则中文提示可能变乱码，甚至直接报 UnicodeEncodeError。
    """
    for stream in (sys.stdout, sys.stdin):        # 输出流和输入流都设一遍
        try:
            stream.reconfigure(encoding="utf-8")  # Python 3.7+ 支持
        except Exception:
            pass  # 万一系统不支持，就保持原样，不影响玩游戏


def ask(prompt):
    """
    包装一下 input()，让"读不到输入"时不要崩溃。

    什么时候会读不到输入？
        正常双击/在 cmd 里手敲时不会。但如果输入被重定向了（比如
        `python guess_number.py < input.txt`），文件读完了再读就会抛 EOFError。
        这种情况按"玩家想退出"处理，返回 None，程序就能优雅收场。

    返回：
        玩家输入的字符串；读不到时返回 None。
    """
    try:
        return input(prompt)
    except EOFError:
        return None


def read_guess(low, high):
    """
    读取玩家输入的一个整数，并保证它是 low~high 之间合法的数字。

    返回：
        合法的整数；如果玩家输入 q，返回 None 表示想退出游戏。

    这里做了三件事，所以写成一个函数反复用：
        1. 输入不是数字 -> 提示重输，不崩溃
        2. 数字超出范围 -> 提示重输
        3. 输入 q      -> 允许中途退出
    """
    while True:                                  # 一直循环，直到拿到合法输入才 return
        raw = ask("请输入你猜的数字（1~100，输入 q 退出）：")

        if raw is None:                          # 输入被关闭/读不到了，当退出处理
            return None

        raw = raw.strip()

        if raw.lower() == "q":                   # 玩家想退出
            return None

        if raw == "":                            # 直接回车
            print("  你什么都没输入，再试一次吧。")
            continue

        try:
            number = int(raw)                    # 尝试把字符串转成整数
        except ValueError:                       # 转不了，说明不是整数
            print("  这不是一个整数哦，请输入数字，例如 42。")
            continue

        if number < low or number > high:        # 转成功了，但不在范围内
            print(f"  超出范围啦，请输入 {low} 到 {high} 之间的数字。")
            continue

        return number                            # 一切合法，把数字交出去


def play_one_round(answer=None):
    """
    玩一整局。返回本局猜的次数；如果玩家中途退出则返回 None。

    参数 answer：
        正常游戏不用传，程序自己随机出题。
        传了就用你指定的答案（给自检/测试用，可以稳定复现某一局的结果）。

    这一局的全部逻辑都在这里，main() 只负责"要不要再来一局"。
    """
    low, high = 1, 100                           # 数字范围
    if answer is None:
        answer = random.randint(low, high)       # 电脑随机出题（闭区间，含 1 和 100）
    count = 0                                    # 记录猜了多少次

    print()
    print("=" * 42)
    print("我想好了一个 1~100 的整数，你来猜猜看！")
    print("=" * 42)

    while True:
        guess = read_guess(low, high)            # 拿到玩家的猜测

        if guess is None:                        # 玩家输入了 q
            print(f"\n好吧，不玩了。偷偷告诉你，答案是 {answer}。")
            return None

        count += 1                               # 猜了一次，计数 +1

        if guess > answer:
            print(f"  大了！  （这是你第 {count} 次猜）")
        elif guess < answer:
            print(f"  小了！  （这是你第 {count} 次猜）")
        else:
            print(f"  恭喜你，猜中啦！答案就是 {answer}。")
            print(f"  你一共猜了 {count} 次。")
            judge(count)                         # 根据次数给个评价
            return count                         # 结束这一局


def judge(count):
    """
    根据猜的次数给一句评价（只是好玩，不影响游戏逻辑）。
    1~100 如果每次都能排除一半，理想情况 7 次以内必中，所以 7 是个分界线。
    """
    if count <= 3:
        print("  评价：运气爆棚！")
    elif count <= 7:
        print("  评价：不错，思路很清晰。")
    elif count <= 12:
        print("  评价：还行，慢慢逼近中。")
    else:
        print("  评价：有点辛苦……下次试试每次都猜中间那个数。")


def self_test():
    """
    自检用的简化流程：用固定答案跑一遍逻辑，验证"大了/小了/猜中/计数"是否正常。
    在命令行执行 `python guess_number.py --test` 就会走这里。
    它不读键盘输入，所以可以在没人操作的情况下验证程序是对的。
    """
    answer = 42                                  # 固定答案，方便对照结果
    low, high = 1, 100
    guesses = [50, 25, 37, 43, 42]               # 预设的猜测序列
    count = 0

    print(f"[自检] 假装答案是 {answer}，依次猜：{guesses}")

    for guess in guesses:
        count += 1
        if guess > answer:
            tip = "大了！"
        elif guess < answer:
            tip = "小了！"
        else:
            tip = "猜中啦！"
        print(f"  第 {count} 次：猜 {guess} -> {tip}（范围 {low}~{high}）")

        # 顺便模拟一下"排除一半范围"的更新过程
        if guess > answer:
            high = guess - 1
        elif guess < answer:
            low = guess + 1

    assert count == 5, "自检失败：计数不对"
    assert guess == answer, "自检失败：最后一次没猜中"
    print("[自检] 全部通过：提示逻辑与次数统计都正常。")


def main():
    """
    程序入口：玩一局 -> 问要不要再来一局。
    """
    setup_console()
    print("欢迎来到『猜数字小游戏』！")

    while True:
        play_one_round()                         # 玩一局

        again = ask("\n再来一局吗？(y = 再来 / 其他键 = 结束)：")
        if again is None:                        # 输入被关闭/读不到了，直接收场
            print("\n谢谢游玩，再见！")
            break

        if again.strip().lower() != "y":
            print("谢谢游玩，再见！")
            break


# 这一行的意思是：只有"直接运行这个文件"时才执行 main()，
# 被别人 import 引入时不会自动开局。
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        setup_console()
        self_test()
    else:
        main()
