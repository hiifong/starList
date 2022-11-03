'''
Readme Development Metrics With waka time progress
'''
import re
import base64
import traceback
import json


START_COMMENT = '<!--START:starList-->'
END_COMMENT = '<!--END:starList-->'
listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"


def readJsonFile(path):
    # print("开始")
    start = 0
    markdown = '| 序号 | 仓库 | 描述 | 更新时间 | Star | Fork | 语言 | 许可证 |\n' + \
                '|:----:| ---- | ---- | ---- | ---- | ---- | ---- | ---- |\n'
    with open(path, "r", encoding='utf-8') as f:
        starList = list(f.readlines())
        for l in starList:
            for obj in json.loads(l):
                start += 1
                license = ''
                desc = ''
                lang = ''
                if obj["description"] == None:
                    desc = '无'
                else:
                    desc = obj["description"][0:200:]
                if obj["language"] == None:
                    lang = '无'
                else:
                    lang = obj["language"]
                if obj["license"] == None:
                    license = '无'
                else:
                    license = obj["license"]["name"]
                # | 序号 | 仓库 | 描述 | 更新时间 | Star | Fork | 语言 | 许可证 |
                markdown += '| ' + str(start) + ' | ' + '[' + obj["name"] + '](' + obj["html_url"] + ')' + ' | ' + desc.replace('|','').replace('\\', '') + ' | ' + \
                    obj["updated_at"][0:9] + ' | ' + str(obj["stargazers_count"]) + ' | ' + str(obj["forks_count"]) + ' | ' + \
                    lang + ' | ' + license + ' |\n'
    f.close()
    return markdown


def decode_readme(data: str):
    '''Decode the contents of old readme'''
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, 'utf-8')


def generate_new_readme(stats: str, readme: str):
    '''Generate a new Readme.md'''
    star_list_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
    return re.sub(listReg, star_list_in_readme, readme)


if __name__ == '__main__':
    try:
        contents = ''
        with open('README.md', encoding='utf-8') as f:
            contents = str(f.readlines())
        f.close()
        markdown = readJsonFile('list.json')
        # rdmd = decode_readme(contents)
        if markdown !=  None:
            new_readme = generate_new_readme(stats=markdown, readme=contents)
            print(new_readme)
            print(type(new_readme))
            if new_readme != '':
                try:
                    with open('README.md', "w+", encoding='utf-8') as f:
                        f.writelines(new_readme.strip('[\'').strip('\']'))
                except:
                    print("写入README失败！")
                print("Readme updated")
    except Exception as e:
        traceback.print_exc()
        print("Exception Occurred " + str(e))
