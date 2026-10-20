"""生成丙午年 iCalendar 文件；仅使用 Python 标准库。"""
from datetime import date, timedelta
from pathlib import Path

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
START = date(2026, 2, 4)
END = date(2027, 2, 4)  # 不含丁未年立春当天
# 日本国立天文台 2026/2027 暦要項；日本标准时减一小时为北京时间。
# 时间精度为分钟；尤其注意芒种由日本时间 6 月 6 日转换为北京 6 月 5 日。
TERMS = [
    ("2026-02-04", "04:02", "立春"),
    ("2026-03-05", "21:59", "惊蛰"),
    ("2026-04-05", "02:40", "清明"),
    ("2026-05-05", "19:49", "立夏"),
    ("2026-06-05", "23:48", "芒种"),
    ("2026-07-07", "09:57", "小暑"),
    ("2026-08-07", "19:43", "立秋"),
    ("2026-09-07", "22:41", "白露"),
    ("2026-10-08", "14:29", "寒露"),
    ("2026-11-07", "17:52", "立冬"),
    ("2026-12-07", "10:53", "大雪"),
    ("2027-01-05", "22:10", "小寒"),
]


def day_ganzhi(day):
    # 公历 2000-01-07 为甲子日；逐日连续循环，不随农历月份重置。
    index = (day - date(2000, 1, 7)).days % 60
    return GAN[index % 10] + ZHI[index % 12]


def escape(value):
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def fold(line):
    """RFC 5545：每物理行至多 75 个 UTF-8 字节，不拆开汉字。"""
    parts, current = [], ""
    for char in line:
        if len((current + char).encode("utf-8")) > 75:
            parts.append(current)
            current = " "
        current += char
    return "\r\n".join(parts + [current])


def event(day, kind, title, description):
    return [
        "BEGIN:VEVENT",
        f"UID:bingwu-2026-{kind}-{day:%Y%m%d}@ganzhi.calendar",
        "DTSTAMP:20261020T000000Z",
        f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
        f"DTEND;VALUE=DATE:{day + timedelta(days=1):%Y%m%d}",
        "SUMMARY:" + escape(title),
        "DESCRIPTION:" + escape(description),
        "TRANSP:TRANSPARENT",
        "STATUS:CONFIRMED",
        "END:VEVENT",
    ]


def write_calendar(filename, name, events, color):
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//Ganzhi Calendar//Bingwu 2026//ZH-CN",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        "X-WR-CALNAME:" + name,
        "X-WR-CALDESC:丙午年（立春至次年立春前）；北京时间交节；日干支按零点换日。",
        "X-WR-TIMEZONE:Asia/Shanghai", "X-APPLE-CALENDAR-COLOR:" + color,
    ]
    for item in events:
        lines.extend(item)
    lines.append("END:VCALENDAR")
    Path(filename).write_bytes(("\r\n".join(map(fold, lines)) + "\r\n").encode("utf-8"))


def main():
    daily, monthly = [], []
    day = START
    while day < END:
        daily.append(event(day, "day", day_ganzhi(day),
            f"公历：{day.isoformat()}\n日干支：{day_ganzhi(day)}\n按民用日历零点换日，不采用子初（23点）换日。"))
        day += timedelta(days=1)
    for index, (iso, clock, term) in enumerate(TERMS):
        day = date.fromisoformat(iso)
        month = GAN[(6 + index) % 10] + ZHI[(2 + index) % 12]
        following = TERMS[index + 1][:2] if index < 11 else ("2027-02-04", "09:46")
        monthly.append(event(day, "month", f"{month}月",
            f"丙午年 · {month}月开始\n节气：{term}\n交节：{iso} {clock}（北京时间，精确到分钟）\n"
            f"本月到下一交节：{following[0]} {following[1]}（北京时间）\n"
            "以十二节划分流月，不按农历初一。全天事件标记交节所在日期，实际从上述时刻起换月。\n"
            "节气来源：日本国立天文台暦要項（日本标准时减一小时）。"))
    write_calendar("ganzhi-2026.ics", "丙午年 · 干支", daily + monthly, "#8E5AC7")
    write_calendar("ganzhi-2026-daily.ics", "丙午年 · 每日干支", daily, "#007AFF")
    write_calendar("ganzhi-2026-monthly.ics", "丙午年 · 流月干支", monthly, "#FF9500")
    print(f"已生成：{len(daily)} 条每日事件、{len(monthly)} 条流月事件。")


if __name__ == "__main__":
    main()
