# 干支日历

在日常使用的日历中查看每日干支与节气流月。支持 Apple 日历及其他兼容 iCalendar（ICS）的日历应用。

每天显示日干支，如「己酉」；每个流月的交节当天，额外显示月干支，如「庚寅月」。打开流月事件可查看节气名称、交节时刻和下次换月时间。所有事件均为全天事件，不占用忙碌时间，无内置提醒。

覆盖 **2026 丙午年至 2030 庚戌年**，即公历 **2026 年 2 月 4 日至 2031 年 2 月 3 日**，包含 1826 条日干支和 60 条流月事件。

## 订阅

[添加日历订阅](webcal://huangyungui02.github.io/ganzhi/ganzhi-2026.ics) · [下载 ICS 文件](https://huangyungui02.github.io/ganzhi/ganzhi-2026.ics)

也可以复制以下地址，在日历应用中添加订阅：

```text
https://huangyungui02.github.io/ganzhi/ganzhi-2026.ics
```

**iPhone / iPad：** 打开「日历 → 日历 → 添加日历 → 添加订阅日历」，粘贴上述地址。菜单名称可能随系统版本变化。

**Mac：** 打开「日历 → 文件 → 新建日历订阅」，粘贴上述地址。

订阅会随项目更新，刷新时间由日历应用决定。如需离线使用，也可下载 ICS 文件后导入；导入的副本不会自动更新。订阅和导入选择一种即可，避免重复显示。

更多设置可参考 [Apple 日历使用说明](https://support.apple.com/zh-cn/guide/iphone/iph3d1110d4/ios)。

## 历法说明

- 使用北京时间（UTC+8）确定交节日期，流日按公历零点换日。
- 干支年以立春为界；流月以十二节（立春、惊蛰、清明、立夏、芒种、小暑、立秋、白露、寒露、立冬、大雪、小寒）为界，不按农历初一。
- 流月事件仅标记交节当天，实际换月发生在详情中的交节时刻，当天交节之前仍属于上月。
- 交节时间由[寿星天文历（sxtwl）](https://github.com/yuangu/sxtwl_cpp)计算，显示至分钟。

流月与农历月份不同：农历以初一为月首，这里的流月以交节为起点。例如，2026 年庚寅月从立春开始，辛卯月从惊蛰开始。

## 本地生成

需要 Python 3，安装依赖后运行：

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python generate_calendar.py
```

输出文件为 `ganzhi-2026.ics`，文件名中的年份表示覆盖范围的起始年份。
