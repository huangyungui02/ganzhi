"""生成 2026—2030 干支年合并日历，沿用已发布的订阅文件名与 UID。"""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import sxtwl

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
FIRST_YEAR = 2026
LAST_YEAR = 2030
TERM_NAMES = {1: "小寒", 3: "立春", 5: "惊蛰", 7: "清明", 9: "立夏",
              11: "芒种", 13: "小暑", 15: "立秋", 17: "白露", 19: "寒露",
              21: "立冬", 23: "大雪"}


def month_boundaries():
    """寿星天文历返回北京时间；包含下一年立春，供末月结束边界使用。"""
    result = []
    day = date(FIRST_YEAR, 2, 1)
    while day < date(LAST_YEAR + 1, 2, 10):
        lunar = sxtwl.fromSolar(day.year, day.month, day.day)
        if lunar.hasJieQi() and lunar.getJieQi() in TERM_NAMES:
            term = lunar.getJieQi()
            t = sxtwl.JD2DD(lunar.getJieQiJD())
            instant = datetime(int(t.Y), int(t.M), int(t.D), int(t.h), int(t.m)) + timedelta(seconds=t.s)
            # 日期以实际交节日期为准；详情中的时刻四舍五入至分钟。
            clock = (instant + timedelta(seconds=30)).strftime("%H:%M")
            result.append((instant.date(), clock, TERM_NAMES[term]))
            if day.year == LAST_YEAR + 1 and term == 3:
                break
        day += timedelta(days=1)
    assert len(result) == (LAST_YEAR - FIRST_YEAR + 1) * 12 + 1
    assert result[0][2] == result[-1][2] == "立春"
    return result


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


def event(day, kind, title, description, stamp):
    return [
        "BEGIN:VEVENT",
        f"UID:bingwu-2026-{kind}-{day:%Y%m%d}@ganzhi.calendar",
        "DTSTAMP:" + stamp,
        "LAST-MODIFIED:" + stamp,
        "SEQUENCE:1",
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
        "PRODID:-//Ganzhi Calendar//2026-2030//ZH-CN",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        "X-WR-CALNAME:" + name,
        "X-WR-CALDESC:2026丙午年至2030庚戌年；立春换年；北京时间交节；日干支按零点换日。",
        "X-WR-TIMEZONE:Asia/Shanghai", "X-APPLE-CALENDAR-COLOR:" + color,
    ]
    for item in events:
        lines.extend(item)
    lines.append("END:VCALENDAR")
    Path(filename).write_bytes(("\r\n".join(map(fold, lines)) + "\r\n").encode("utf-8"))


def main():
    terms = month_boundaries()
    start, end = terms[0][0], terms[-1][0]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    daily, monthly = [], []
    day = start
    while day < end:
        daily.append(event(day, "day", day_ganzhi(day),
            f"公历：{day.isoformat()}\n日干支：{day_ganzhi(day)}\n按民用日历零点换日，不采用子初（23点）换日。", stamp))
        day += timedelta(days=1)
    for index, (day, clock, term) in enumerate(terms[:-1]):
        iso = day.isoformat()
        month = GAN[(6 + index) % 10] + ZHI[(2 + index) % 12]
        year_index = FIRST_YEAR + index // 12 - 4
        year = GAN[year_index % 10] + ZHI[year_index % 12]
        following = terms[index + 1]
        monthly.append(event(day, "month", f"{month}月",
            f"{year}年 · {month}月开始\n节气：{term}\n交节：{iso} {clock}（北京时间，约至分钟）\n"
            f"本月到下一交节：{following[0]} {following[1]}（北京时间）\n"
            "以十二节划分流月，不按农历初一。全天事件标记交节所在日期，实际从上述时刻起换月。\n"
            "节气来源：寿星天文历 sxtwl 2.0.7。", stamp))
    # 保留旧文件名与事件 UID，已有订阅无需更换网址。
    write_calendar("ganzhi-2026.ics", "干支 · 2026—2030", daily + monthly, "#8E5AC7")
    print(f"已生成 {start} 至 {end - timedelta(days=1)}：{len(daily)} 条每日事件、{len(monthly)} 条流月事件。")


if __name__ == "__main__":
    main()
