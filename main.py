# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import datetime
from bs4 import BeautifulSoup as bs
import urllib.request
import yagmail

from github_issue import make_github_issue
from config import NEW_SUB_URLS, KEYWORD_LIST, KEYWORD_EX_LIST, USERNAME

def send_email(subject, content, to_email, user, password):
    try:
        yag = yagmail.SMTP(user, password)
        yag.send(to=to_email, subject=subject, contents=content)
        print("邮件已发送到", to_email)
    except Exception as e:
        print("发送邮件失败:", str(e))

def main(args):
    keyword_list = KEYWORD_LIST
    keyword_ex_list = KEYWORD_EX_LIST
    #keyword_dict = {key: [] for key in keyword_list}
    keyword_dict = []
    
    # TOKEN = args.token
    for url in NEW_SUB_URLS:
        page = urllib.request.urlopen(url)
        soup = bs(page, 'html.parser')
        content = soup.body.find("div", {'id': 'content'})

        issue_title = content.find("h3").text.split("(")[0].strip()
        dt_list = content.dl.find_all("dt")
        dd_list = content.dl.find_all("dd")
        arxiv_base = "https://arxiv.org/abs/"

        assert len(dt_list) == len(dd_list)

        for i in range(len(dt_list)):
            paper = {}
            paper_number = dt_list[i].text.strip().split(":")[1][:11]
            paper['main_page'] = arxiv_base + paper_number
            paper['pdf'] = arxiv_base.replace('abs', 'pdf') + paper_number
            paper['title'] = dd_list[i].find("div", {"class": "list-title mathjax"}).text.replace("Title:\n", "").strip()
            paper['authors'] = dd_list[i].find("div", {"class": "list-authors"}).text.replace("Authors:\n", "").replace("\n", "").strip()
            paper['subjects'] = dd_list[i].find("div", {"class": "list-subjects"}).text.replace("Subjects: ", "").strip()
            paper['abstract'] = dd_list[i].find("p", {"class": "mathjax"}).text.replace("\n", " ").strip()

            inclu = 0
            for keyword in keyword_list:
                if keyword.lower() in paper['abstract'].lower() or keyword.lower() in paper['title'].lower():
                    inclu = 1
            for keyword_ex in keyword_ex_list:
                if (keyword_ex.lower() in paper['abstract'].lower()) == 1:
                    inclu = 0
            if inclu == 1:
                keyword_dict.append(paper)

    import datetime
    
    full_report = '# '+issue_title+'\n'
    full_report = full_report + 'Auto update Star Formation & Molecular Cloud papers at about 2:30am UTC (10:30am Beijing time) every weekday.'+'\n'
    full_report = full_report + '\n\n'
    full_report = full_report + '阅读 `Usage.md`了解如何使用此repo实现个性化的Arxiv论文推送' + '\n\n'
    full_report = full_report + 'See `Usage.md` for instructions on how to personalize the repo. ' + '\n'
    full_report = full_report + '\n\n'
    full_report = full_report + 'Keyword list: ' + str(keyword_list) + '\n'
    full_report = full_report + '\n\n'
    full_report = full_report + 'Excluded: ' + str(keyword_ex_list) + '\n'
    full_report = full_report + '\n\n'

    full_report = full_report + '### Today: ' + str(len(keyword_dict)) + 'papers \n\n'
    
    if len(keyword_dict) == 0:
        full_report = full_report + 'There is no result \n'

    for paper in keyword_dict:
        report = f"#### {paper['title']}\n - **Authors:** {paper['authors']}\n - **Subjects:** {paper['subjects']}\n - **Arxiv link:** {paper['main_page']}\n - **Pdf link:** {paper['pdf']}\n - **Abstract**\n {paper['abstract']}"
        full_report = full_report + report + '\n\n'
        
    full_report = full_report + '\n\n'
    full_report = full_report + 'by YinChihHsiang (Yin ZhiXiang). ' + '\n'
    full_report = full_report + '\n\n'
    full_report = full_report + datetime.datetime.now().strftime("%Y-%m-%d") + '\n'

    # full_report = full_report + '\n</details>'

    # create an md file using full_report, with the name of date, and upload it to github
    # create a date string
    
    filename = './Arxiv_Daily_Notice/'+datetime.datetime.now().strftime("%Y-%m-%d") + '-Arxiv-Daily-Paper.md'
    filename_readme = './README.md'
    print(filename)
    with open(filename, 'w+') as f:
        f.write(full_report)

    with open(filename_readme, 'w+') as f:
        f.write(full_report)

    # 邮件推送（用环境变量，适配GitHub Actions secrets）
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")
    yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD, host='smtp.qq.com')
    yag.send(to=EMAIL_RECEIVER, subject=issue_title + " | ArxivDaily", contents=full_report)
    
    now = datetime.datetime.now()
    current_hour = now.hour
    if current_hour==2: make_github_issue(title=issue_title, body=full_report,labels=keyword_list, 
    TOKEN=os.environ['TOKEN'])
    print("end")

if __name__ == '__main__':
    #     处理参数，实际只需要TOKEN
    parser = argparse.ArgumentParser(description='Get the TOKEN for github issue')
    parser.add_argument('-t','--token', help='The github TOKEN', required=True, default='Token Needed!')
    args = vars(parser.parse_args())
    # print(args['token'])
    # print(os.environ['TOKEN'])
    main(args)
