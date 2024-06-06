import re
from typing import List, Dict

def reg_search(text: str, regex_list: List[Dict[str, str]]) -> List[Dict[str, Dict[str, List[str]]]]:
    results = []

    for regex_dict in regex_list:
        match_dict = {}
        for key, pattern in regex_dict.items():
            if key == '换股期限':
                # 特别处理换股期限，捕获多个日期并格式化
                date_pattern = re.compile(pattern)
                matches = date_pattern.findall(text)
                if matches:
                    formatted_dates = []
                    for match in matches:
                        year, month, day = match
                        formatted_date = f"{year}-{int(month):02d}-{int(day):02d}"
                        formatted_dates.append(formatted_date)
                    match_dict[key] = formatted_dates
            else:
                # 对其他字段使用一般的正则表达式匹配
                matches = re.findall(pattern, text)
                if matches:
                    match_dict[key] = matches
        results.append(match_dict)

    return results

# 示例用法
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''
regex_list = [
    {
        '标的证券': r'\b\d{6}\.SH\b',
        '换股期限': r'(\d{4}) 年 (\d{1,2}) 月 (\d{1,2}) 日'
    }
]

results = reg_search(text, regex_list)
print(results)
