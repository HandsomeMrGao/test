import requests
import pandas as pd

url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"
params = {
    "pageNo": 1,
    "pageSize": 15,
    "bondType": 100001,
    "issueYear": 2023,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Cookie": "AlteonP10=CJUuIiw/F6wZxk4szxhieg$$; apache=4a63b086221745dd13be58c2f7de0338; ags=a23ede7e97bccb1b2380be21609ada80; _ulta_id.ECM-Prod.ccc4=5ac035e1b2b2f709; _ulta_ses.ECM-Prod.ccc4=148a537bb0a0b097",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://iftp.chinamoney.com.cn/english/bdInfo/",
}

final_df = pd.DataFrame(columns=['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating'])

total_pages = 8

for page_no in range(1, total_pages + 1):
    params["pageNo"] = page_no

    response = requests.post(url, data=params, headers=headers)
    data = response.json()
    bond_data = data['data']['resultList']

    formatted_data = []
    for bond in bond_data:
        formatted_data.append([
            bond['isin'],
            bond['bondCode'],
            bond['entyFullName'],
            bond['bondType'],
            bond['issueStartDate'],
            bond['debtRtng']
        ])

    df = pd.DataFrame(formatted_data,
                      columns=['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating'])

    final_df = pd.concat([final_df, df], ignore_index=True)

final_df.to_csv('bond_data.csv', index=False)
