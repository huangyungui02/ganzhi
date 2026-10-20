# 干支日历 2026—2030（iOS / iCloud）

一个日历同时包含每日干支和流月开始事件。流日仅显示「己酉」，流月首日额外显示「庚寅月」，颜色一致。节气和交节时刻保留在事件详情中。

范围为 **2026-02-04 至 2031-02-03**，覆盖 2026 丙午、2027 丁未、2028 戊申、2029 己酉、2030 庚戌五个完整干支年；到 2031 辛亥年立春当天停止。共 1826 条每日事件、60 条流月事件。所有事件均为全天、不占用忙碌时间，无内置提醒。

## 订阅

在 iPhone「日历 → 日历 → 添加日历 → 添加订阅日历」中填入：

```text
https://huangyungui02.github.io/ganzhi/ganzhi-2026.ics
```

或打开 `webcal://huangyungui02.github.io/ganzhi/ganzhi-2026.ics`。菜单名称可能随系统版本变化。

**原有订阅网址保持不变。** 文件名中的 2026 表示起始年份，内容已扩展到 2030 干支年结束。订阅为只读，更新频率由 Apple 日历控制；已有订阅无需再添加一个日历。原日、月拆分文件已删除。

如需静态导入，只使用 `ganzhi-2026.ics`。在 Mac「日历」中新建 iCloud 日历，通过「文件 → 导入」选择此文件，再同步到 iPhone。静态导入不会自动更新；替换之前导入的版本时，建议删除专用旧日历后重新导入，以免重复。

Apple 官方说明：https://support.apple.com/zh-cn/guide/iphone/iph3d1110d4/ios

## 历法口径

- 使用北京时间（UTC+8）确定交节日期，流日按公历零点换日。
- 干支年以立春为界；流月以十二节（立春、惊蛰、清明、立夏、芒种、小暑、立秋、白露、寒露、立冬、大雪、小寒）为界，不按农历初一。
- 各年首月依次为：2026 庚寅、2027 壬寅、2028 甲寅、2029 丙寅、2030 戊寅，逐月按六十甲子顺推。
- 流月事件仅标记交节当天，实际换月发生在详情中的交节时刻，当天交节之前仍属于上月。
- 交节由寿星天文历 `sxtwl==2.0.7` 计算，详情时刻四舍五入至分钟。日期取实际交节日期，不因分钟取整而变更。
- 2026 芒种为北京时间 6 月 5 日深夜；2029 立春为 2 月 3 日，不能硬编码为每年 2 月 4 日。
- 日干支以 2000-01-07 甲子日为基准，按六十日连续循环，跨年与闰日均不重置。
- 全天显示的最后一天为 2031-02-03；2031 立春当天不生成事件。

计算库和交叉核对资料：

- https://github.com/yuangu/sxtwl_cpp
- https://pypi.org/project/sxtwl/
- https://eco.mtk.nao.ac.jp/koyomi/yoko/2026/rekiyou262.html
- https://eco.mtk.nao.ac.jp/koyomi/yoko/2027/rekiyou272.html

## 重新生成和发布

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python generate_calendar.py
```

仅生成 `ganzhi-2026.ics` 一个日历文件。使用 UTF-8、CRLF、RFC 5545 字节折行、稳定 UID 和排他的结束日期。现有事件保留原 UID，确保订阅更新时可识别同一事件。

将更新提交并推送到 `main`，GitHub Pages 会从根目录重新发布。公网文件应返回 HTTP 200 和 `Content-Type: text/calendar`。
