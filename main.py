#!/usr/bin/env python
#  -*- coding: utf-8 -*-

#  这里是主函数^_^

import configparser
import os
import random
import json
import time
from post import Shuyi
from Message_Push.Wechat import WeChat as Wp

class config: #  配置文件操作，配置文件为config.ini
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.file = os.path.join(self.root_path , "config.ini")
        self.cfg.read(self.file, encoding='utf-8')
        self.sections = self.cfg.sections()

    def sections_check(self): #  检查sections
        IsNeeded = ['auth', 'User-Agent']
        if (('auth' in self.sections) & ('User-Agent' in self.sections)): #  包含auth和User-Agent
            print("config文件正常！")
            return 1
        else:
            print("config文件配置错误！\n config文件内缺少必须项！\n 请使用config.ini.example重新配置！")
            return 0

    def agent_check(self): #  检查User-Agent是否与auth数量一致，若非一致则进行调整
        auth = self.cfg.items('auth')
        agt = self.cfg.items('User-Agent')
        if auth > agt:
            for i in range(len(auth) - len(agt)):
                r = random.randint(1,len(agt))
                agt.append(agt(r))
            print("User-Agent修正完成！")
            return 1
        print("User-Agent数目正常！")
        return 1
    
    def config_check(self): #  检查config.ini文件
        self.sections_check()
        self.agent_check()
        return 1
    
    def WeChat_Push(self): #  微信推送相关数据
        Inform = [self.cfg.get('CorporationID', 'CORPID')]
        Inform.append(self.cfg.get('AppID', 'AGENTID'))
        Inform.append(self.cfg.get('Secret', 'CORPSECRET'))
        Inform.append(self.cfg.get('User', 'TOUSER'))
        return Inform
    
    def user_num(self): #  返回用户数量
        return len(self.cfg.items('auth'))
    
    def auth(self, i): #  返回auth_key
        key = self.cfg.options('auth')
        value = self.cfg.get('auth', key[i])
        return value
    
    def agent(self, i): #  返回User-Agent_key
        key = self.cfg.options('User-Agent')
        value = self.cfg.get('User-Agent', key[i])
        return value
    
class header:
    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.file = os.path.join(self.root_path, "headers.json")

    def headers_check(self): #  检测headers.json文件
        example = os.path.join(self.root_path, 'example', "headers.json.example")
        print(os.path.exists(example))
 
        print("已应用headers.json模板！")
        return 1

    def get_json_data(self, auth, agent): #  获取json数据
        example = os.path.join(self.root_path, 'example', "headers.json.example")
        with open(example, 'r') as exp:
            exp = exp.read()
            j = json.loads(exp) #  加载json文件
            j["auth"] = auth #  修改auth
            j["User-Agent"] = agent #  修改User-Agent
        return j #  返回修改后的内容
  
    def write_json_data(self, auth, agent): #  写入json文件
        with open(self.file, 'w') as headers: #  使用写模式
            j = self.get_json_data(auth, agent)
            json.dump(j, headers)
 
if __name__ == '__main__':
    cfg = config()
    cfg.config_check() #  检查config.ini
    hd = header()
    for i in range(cfg.user_num()):
        auth = cfg.auth(i)
        agent = cfg.agent(i)
        hd.write_json_data(auth, agent)
        sy = Shuyi()
        res = sy.post()
        print(res.text)
        Inform = cfg.WeChat_Push()
        print(Inform)
        print(type(Inform[2]))
        WeChatpush = Wp(Inform)
        rsp = WeChatpush.send_data(res.text)
        print(rsp)
        r=random.randint(60,100)
        print(f"已完成第{i + 1}个用户签到，等待{r}秒")
        time.sleep(random.randint(60,100))

