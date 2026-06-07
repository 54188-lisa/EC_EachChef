#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EC_EachChef - 智能菜谱助手

一个基于Gradio的菜谱搜索应用，支持：
- 🥗 菜谱分类浏览（西餐、中餐、特色菜）
- 🧅 食材标签筛选（所选食材必须是菜谱食材的子集）
- 🔧 工具标签筛选
- 📊 用户偏好学习和智能推荐
- 💰 食材采购记录和成本计算
- 🔥 热量计算和营养信息
- 📅 时令菜谱推荐
"""

import os
import random
from datetime import datetime
import gradio as gr
import pandas as pd

# 用户偏好数据
USER_PREFERENCES = {
    "favorites": [],  # 收藏的菜谱ID
    "view_history": [],  # 浏览历史
    "cooked_history": []  # 烹饪记录
}

# 新增菜谱上下文存储
NEW_RECIPE_CONTEXT = {
    "current_draft": None,
    "saved_recipes": []
}

RECIPES_DATA = {
    "chinese": [
        {
            "id": "c1",
            "name": "宫保鸡丁",
            "category": "chinese",
            "ingredients": ["鸡肉", "花生米", "干辣椒", "花椒", "葱姜蒜"],
            "tools": ["炒锅", "铲子", "刀", "砧板"],
            "cost": 15.5,
            "calories": 320,
            "difficulty": "中等",
            "cook_time": "20分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "经典川菜，鸡肉嫩滑，花生酥脆，麻辣鲜香",
            "steps": ["鸡肉切丁腌制", "花生米炸熟", "爆香调料", "翻炒鸡肉", "加入花生米"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=kung%20pao%20chicken%20chinese%20dish%20delicious&image_size=square_hd"
        },
        {
            "id": "c2",
            "name": "鱼香肉丝",
            "category": "chinese",
            "ingredients": ["猪肉丝", "木耳", "胡萝卜", "青椒", "葱姜蒜"],
            "tools": ["炒锅", "铲子", "刀", "砧板"],
            "cost": 12.0,
            "calories": 280,
            "difficulty": "中等",
            "cook_time": "25分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "川菜经典，酸甜微辣，口感丰富",
            "steps": ["肉丝腌制", "配菜切丝", "调制鱼香汁", "快速翻炒"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=yu%20xiang%20shredded%20pork%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c3",
            "name": "麻婆豆腐",
            "category": "chinese",
            "ingredients": ["豆腐", "肉末", "豆瓣酱", "花椒粉", "葱花"],
            "tools": ["炒锅", "铲子", "刀", "砧板"],
            "cost": 8.5,
            "calories": 240,
            "difficulty": "简单",
            "cook_time": "15分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "川菜代表，麻辣鲜香，下饭神器",
            "steps": ["豆腐切块焯水", "炒香肉末", "加入豆瓣酱", "炖煮豆腐"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=mapo%20tofu%20chinese%20dish%20spicy&image_size=square_hd"
        },
        {
            "id": "c4",
            "name": "糖醋里脊",
            "category": "chinese",
            "ingredients": ["猪里脊", "淀粉", "番茄酱", "白糖", "醋"],
            "tools": ["炒锅", "炸锅", "铲子", "刀"],
            "cost": 18.0,
            "calories": 450,
            "difficulty": "较难",
            "cook_time": "30分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "酸甜可口，外酥里嫩",
            "steps": ["里脊肉切条", "裹粉油炸", "调制糖醋汁", "裹汁翻炒"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sweet%20and%20sour%20pork%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c5",
            "name": "红烧肉",
            "category": "chinese",
            "ingredients": ["五花肉", "冰糖", "酱油", "料酒", "葱姜"],
            "tools": ["炒锅", "炖锅", "铲子", "刀"],
            "cost": 25.0,
            "calories": 520,
            "difficulty": "中等",
            "cook_time": "60分钟",
            "season": ["秋季", "冬季"],
            "description": "经典家常菜，肥而不腻，入口即化",
            "steps": ["五花肉焯水", "煸炒出油", "炒糖色", "炖煮入味"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=braised%20pork%20belly%20chinese%20dish%20hong%20shao%20rou&image_size=square_hd"
        },
        {
            "id": "c6",
            "name": "清蒸鱼",
            "category": "chinese",
            "ingredients": ["鲈鱼", "葱姜", "料酒", "蒸鱼豉油", "红椒"],
            "tools": ["蒸锅", "盘子", "刀"],
            "cost": 28.0,
            "calories": 220,
            "difficulty": "简单",
            "cook_time": "15分钟",
            "season": ["春季", "夏季"],
            "description": "清淡鲜美，原汁原味",
            "steps": ["鱼处理干净", "葱姜铺底", "蒸制", "淋热油和豉油"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=steamed%20fish%20chinese%20dish%20fresh&image_size=square_hd"
        },
        {
            "id": "c7",
            "name": "番茄炒蛋",
            "category": "chinese",
            "ingredients": ["番茄", "鸡蛋", "葱花", "盐", "糖"],
            "tools": ["炒锅", "铲子", "碗"],
            "cost": 6.0,
            "calories": 180,
            "difficulty": "简单",
            "cook_time": "10分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "家常必备，酸甜可口",
            "steps": ["番茄切块", "鸡蛋打散", "炒蛋盛出", "炒番茄", "混合翻炒"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=tomato%20scrambled%20eggs%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c8",
            "name": "青椒土豆丝",
            "category": "chinese",
            "ingredients": ["土豆", "青椒", "大蒜", "盐", "醋"],
            "tools": ["炒锅", "铲子", "刀", "砧板"],
            "cost": 5.0,
            "calories": 150,
            "difficulty": "简单",
            "cook_time": "12分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "脆爽可口，下饭小菜",
            "steps": ["土豆切丝浸泡", "青椒切丝", "爆香大蒜", "快速翻炒"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=shredded%20potato%20with%20green%20pepper%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c9",
            "name": "蒜蓉西兰花",
            "category": "chinese",
            "ingredients": ["西兰花", "大蒜", "盐", "蚝油"],
            "tools": ["炒锅", "铲子", "蒸锅"],
            "cost": 8.0,
            "calories": 120,
            "difficulty": "简单",
            "cook_time": "8分钟",
            "season": ["春季", "秋季"],
            "description": "营养健康，清爽可口",
            "steps": ["西兰花切块焯水", "爆香大蒜", "翻炒调味"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=garlic%20broccoli%20chinese%20vegetable%20dish&image_size=square_hd"
        },
        {
            "id": "c10",
            "name": "老鸭汤",
            "category": "chinese",
            "ingredients": ["老鸭", "冬瓜", "姜片", "料酒", "枸杞"],
            "tools": ["炖锅", "砂锅", "刀"],
            "cost": 45.0,
            "calories": 380,
            "difficulty": "中等",
            "cook_time": "120分钟",
            "season": ["夏季", "冬季"],
            "description": "滋补养生，汤鲜味美",
            "steps": ["老鸭焯水", "砂锅炖煮", "加入冬瓜枸杞"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=duck%20soup%20chinese%20traditional%20soup&image_size=square_hd"
        },
        {
            "id": "c11",
            "name": "回锅肉",
            "category": "chinese",
            "ingredients": ["五花肉", "蒜苗", "豆瓣酱", "甜面酱", "葱姜蒜"],
            "tools": ["炒锅", "铲子", "刀"],
            "cost": 20.0,
            "calories": 420,
            "difficulty": "中等",
            "cook_time": "25分钟",
            "season": ["春季", "秋季", "冬季"],
            "description": "川菜经典，肥而不腻",
            "steps": ["五花肉煮至八成熟", "切片", "爆香调料", "翻炒入味"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=twice%20cooked%20pork%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c12",
            "name": "酸菜鱼",
            "category": "chinese",
            "ingredients": ["草鱼", "酸菜", "泡椒", "葱姜蒜", "干辣椒"],
            "tools": ["炒锅", "煮锅", "刀"],
            "cost": 32.0,
            "calories": 340,
            "difficulty": "较难",
            "cook_time": "40分钟",
            "season": ["冬季"],
            "description": "酸辣开胃，鱼肉鲜嫩",
            "steps": ["鱼处理切片", "炒香酸菜泡椒", "加水煮沸", "下鱼片"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sour%20soup%20fish%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c13",
            "name": "水煮牛肉",
            "category": "chinese",
            "ingredients": ["牛肉片", "豆芽", "豆瓣酱", "花椒", "干辣椒"],
            "tools": ["炒锅", "煮锅", "刀"],
            "cost": 35.0,
            "calories": 450,
            "difficulty": "中等",
            "cook_time": "30分钟",
            "season": ["冬季"],
            "description": "麻辣鲜香，牛肉嫩滑",
            "steps": ["牛肉切片腌制", "炒香底料", "加水煮沸", "涮牛肉"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sichuan%20boiled%20beef%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c14",
            "name": "青椒肉丝",
            "category": "chinese",
            "ingredients": ["猪肉丝", "青椒", "葱姜蒜", "生抽", "料酒"],
            "tools": ["炒锅", "铲子", "刀"],
            "cost": 12.0,
            "calories": 260,
            "difficulty": "简单",
            "cook_time": "15分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "家常小炒，鲜香可口",
            "steps": ["肉丝腌制", "青椒切丝", "快速翻炒"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=shredded%20pork%20with%20green%20pepper%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c15",
            "name": "蚝油生菜",
            "category": "chinese",
            "ingredients": ["生菜", "蚝油", "大蒜", "生抽", "糖"],
            "tools": ["炒锅", "铲子"],
            "cost": 6.0,
            "calories": 100,
            "difficulty": "简单",
            "cook_time": "6分钟",
            "season": ["春季", "夏季", "秋季"],
            "description": "清淡爽口，营养健康",
            "steps": ["生菜焯水", "爆香大蒜", "加入蚝油调味"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=lettuce%20with%20oyster%20sauce%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c16",
            "name": "红烧排骨",
            "category": "chinese",
            "ingredients": ["排骨", "冰糖", "酱油", "料酒", "葱姜"],
            "tools": ["炒锅", "炖锅", "铲子"],
            "cost": 35.0,
            "calories": 480,
            "difficulty": "中等",
            "cook_time": "45分钟",
            "season": ["秋季", "冬季"],
            "description": "色泽红亮，肉质酥烂",
            "steps": ["排骨焯水", "炒糖色", "加入调料炖煮", "收汁"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=braised%20pork%20ribs%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c17",
            "name": "宫保虾球",
            "category": "chinese",
            "ingredients": ["虾仁", "花生米", "干辣椒", "花椒", "葱姜蒜"],
            "tools": ["炒锅", "铲子", "刀"],
            "cost": 32.0,
            "calories": 350,
            "difficulty": "中等",
            "cook_time": "20分钟",
            "season": ["春季", "夏季"],
            "description": "虾仁鲜嫩，花生酥脆",
            "steps": ["虾仁腌制", "花生米炸熟", "爆香调料", "翻炒虾仁"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=kung%20pao%20shrimp%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c18",
            "name": "酸辣土豆丝",
            "category": "chinese",
            "ingredients": ["土豆", "干辣椒", "大蒜", "醋", "盐"],
            "tools": ["炒锅", "铲子", "刀"],
            "cost": 4.0,
            "calories": 140,
            "difficulty": "简单",
            "cook_time": "10分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "酸辣爽口，下饭必备",
            "steps": ["土豆切丝浸泡", "爆香辣椒大蒜", "快速翻炒", "加醋"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sour%20and%20spicy%20shredded%20potato%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c19",
            "name": "清炒时蔬",
            "category": "chinese",
            "ingredients": ["青菜", "大蒜", "盐", "油"],
            "tools": ["炒锅", "铲子"],
            "cost": 5.0,
            "calories": 80,
            "difficulty": "简单",
            "cook_time": "6分钟",
            "season": ["春季", "夏季", "秋季"],
            "description": "清淡健康，原汁原味",
            "steps": ["青菜洗净", "爆香大蒜", "快炒青菜"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=stir%20fried%20vegetables%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c20",
            "name": "红烧茄子",
            "category": "chinese",
            "ingredients": ["茄子", "大蒜", "生抽", "蚝油", "糖"],
            "tools": ["炒锅", "铲子", "刀"],
            "cost": 6.0,
            "calories": 180,
            "difficulty": "中等",
            "cook_time": "15分钟",
            "season": ["夏季"],
            "description": "软糯入味，下饭神器",
            "steps": ["茄子切条", "煎至金黄", "加入调料炖煮"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=braised%20eggplant%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c21",
            "name": "蒜蓉粉丝蒸扇贝",
            "category": "chinese",
            "ingredients": ["扇贝", "粉丝", "大蒜", "生抽", "葱花"],
            "tools": ["蒸锅", "刀"],
            "cost": 38.0,
            "calories": 280,
            "difficulty": "中等",
            "cook_time": "12分钟",
            "season": ["春季", "夏季"],
            "description": "鲜美可口，宴客佳品",
            "steps": ["扇贝处理", "粉丝泡软", "蒜蓉调制", "蒸制"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=steamed%20scallops%20with%20garlic%20chinese%20dish&image_size=square_hd"
        },
        {
            "id": "c22",
            "name": "清蒸大闸蟹",
            "category": "chinese",
            "ingredients": ["大闸蟹", "姜片", "料酒", "醋", "姜丝"],
            "tools": ["蒸锅", "盘子"],
            "cost": 88.0,
            "calories": 320,
            "difficulty": "简单",
            "cook_time": "15分钟",
            "season": ["秋季"],
            "description": "蟹黄饱满，鲜美无比",
            "steps": ["螃蟹洗净", "蒸制", "准备姜醋"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=steamed%20hairy%20crab%20chinese%20dish&image_size=square_hd"
        }
    ],
    "western": [
        {
            "id": "w1",
            "name": "煎牛排",
            "category": "western",
            "ingredients": ["牛排", "橄榄油", "黄油", "大蒜", "迷迭香"],
            "tools": ["平底锅", "烤箱", "夹子", "温度计"],
            "cost": 68.0,
            "calories": 480,
            "difficulty": "较难",
            "cook_time": "15分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "外焦里嫩，肉香四溢",
            "steps": ["牛排擦干", "热锅煎制", "加黄油迷迭香", "静置"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=pan%20seared%20beef%20steak%20western%20dish&image_size=square_hd"
        },
        {
            "id": "w2",
            "name": "意大利肉酱面",
            "category": "western",
            "ingredients": ["牛肉末", "番茄", "洋葱", "大蒜", "意面"],
            "tools": ["炒锅", "煮锅", "铲子"],
            "cost": 22.0,
            "calories": 420,
            "difficulty": "中等",
            "cook_time": "30分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "经典意式料理，浓郁可口",
            "steps": ["炒香洋葱大蒜", "加入肉末", "加入番茄炖煮", "煮意面"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=spaghetti%20bolognese%20italian%20pasta&image_size=square_hd"
        },
        {
            "id": "w3",
            "name": "奶油蘑菇汤",
            "category": "western",
            "ingredients": ["蘑菇", "洋葱", "黄油", "奶油", "面粉"],
            "tools": ["汤锅", "搅拌机", "铲子"],
            "cost": 15.0,
            "calories": 380,
            "difficulty": "中等",
            "cook_time": "25分钟",
            "season": ["秋季", "冬季"],
            "description": "香浓丝滑，暖胃暖心",
            "steps": ["炒香洋葱蘑菇", "加面粉炒香", "加入牛奶奶油", "搅拌细腻"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cream%20of%20mushroom%20soup%20western&image_size=square_hd"
        },
        {
            "id": "w4",
            "name": "烤鸡翅",
            "category": "western",
            "ingredients": ["鸡翅", "蜂蜜", "生抽", "料酒", "蒜末"],
            "tools": ["烤箱", "烤盘", "刷子"],
            "cost": 20.0,
            "calories": 360,
            "difficulty": "简单",
            "cook_time": "30分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "香甜酥脆，老少皆宜",
            "steps": ["鸡翅腌制", "烤箱烘烤", "刷蜂蜜"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=honey%20baked%20chicken%20wings&image_size=square_hd"
        },
        {
            "id": "w5",
            "name": "凯撒沙拉",
            "category": "western",
            "ingredients": ["生菜", "鸡胸肉", "帕玛森芝士", "凯撒酱", "面包丁"],
            "tools": ["刀", "砧板", "沙拉碗"],
            "cost": 18.0,
            "calories": 320,
            "difficulty": "简单",
            "cook_time": "10分钟",
            "season": ["夏季"],
            "description": "清爽健康，营养均衡",
            "steps": ["生菜撕片", "鸡胸肉煎熟切片", "加入配料和酱料"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=caesar%20salad%20western%20healthy%20dish&image_size=square_hd"
        },
        {
            "id": "w6",
            "name": "法式煎蛋卷",
            "category": "western",
            "ingredients": ["鸡蛋", "牛奶", "黄油", "盐", "黑胡椒"],
            "tools": ["平底锅", "铲子", "碗"],
            "cost": 5.0,
            "calories": 220,
            "difficulty": "中等",
            "cook_time": "8分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "法式经典早餐，嫩滑可口",
            "steps": ["鸡蛋牛奶混合", "平底锅煎制", "卷成蛋卷"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=french%20omelette%20western%20breakfast&image_size=square_hd"
        },
        {
            "id": "w7",
            "name": "烤三文鱼",
            "category": "western",
            "ingredients": ["三文鱼", "柠檬", "橄榄油", "黑胡椒", "迷迭香"],
            "tools": ["烤箱", "烤盘", "刷子"],
            "cost": 45.0,
            "calories": 340,
            "difficulty": "简单",
            "cook_time": "15分钟",
            "season": ["夏季"],
            "description": "鲜嫩多汁，健康美味",
            "steps": ["三文鱼调味", "烤箱烘烤", "淋柠檬汁"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=baked%20salmon%20western%20dish&image_size=square_hd"
        },
        {
            "id": "w8",
            "name": "土豆泥",
            "category": "western",
            "ingredients": ["土豆", "黄油", "牛奶", "盐", "黑胡椒"],
            "tools": ["煮锅", "搅拌机", "勺子"],
            "cost": 8.0,
            "calories": 280,
            "difficulty": "简单",
            "cook_time": "20分钟",
            "season": ["秋季", "冬季"],
            "description": "绵密细腻，经典配菜",
            "steps": ["土豆煮熟", "压成泥", "加入黄油牛奶"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=mashed%20potatoes%20western%20side%20dish&image_size=square_hd"
        },
        {
            "id": "w9",
            "name": "披萨",
            "category": "western",
            "ingredients": ["披萨面团", "番茄酱", "芝士", "香肠", "蘑菇"],
            "tools": ["烤箱", "烤盘", "刷子"],
            "cost": 30.0,
            "calories": 520,
            "difficulty": "较难",
            "cook_time": "25分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "意式经典，芝士浓郁",
            "steps": ["面团发酵", "擀平", "涂番茄酱", "加配料和芝士", "烘烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=homemade%20pizza%20western%20food&image_size=square_hd"
        },
        {
            "id": "w10",
            "name": "汉堡",
            "category": "western",
            "ingredients": ["汉堡面包", "牛肉饼", "生菜", "番茄", "酱料"],
            "tools": ["平底锅", "烤箱"],
            "cost": 25.0,
            "calories": 480,
            "difficulty": "中等",
            "cook_time": "15分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "美式快餐，方便快捷",
            "steps": ["煎牛肉饼", "烤面包", "组装汉堡"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=hamburger%20western%20fast%20food&image_size=square_hd"
        },
        {
            "id": "w11",
            "name": "烤羊排",
            "category": "western",
            "ingredients": ["羊排", "迷迭香", "大蒜", "橄榄油", "盐"],
            "tools": ["烤箱", "烤盘"],
            "cost": 55.0,
            "calories": 460,
            "difficulty": "中等",
            "cook_time": "25分钟",
            "season": ["秋季", "冬季"],
            "description": "外焦里嫩，香气扑鼻",
            "steps": ["羊排腌制", "烤箱烘烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=grilled%20lamb%20chops%20western%20dish&image_size=square_hd"
        },
        {
            "id": "w12",
            "name": "焗烤蔬菜",
            "category": "western",
            "ingredients": ["西兰花", "胡萝卜", "土豆", "芝士", "黄油"],
            "tools": ["烤箱", "烤盘"],
            "cost": 18.0,
            "calories": 280,
            "difficulty": "简单",
            "cook_time": "25分钟",
            "season": ["秋季", "冬季"],
            "description": "芝士香浓，蔬菜软糯",
            "steps": ["蔬菜切块", "铺在烤盘", "撒芝士", "烘烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=roasted%20vegetables%20with%20cheese&image_size=square_hd"
        },
        {
            "id": "w13",
            "name": "黑椒牛柳",
            "category": "western",
            "ingredients": ["牛里脊", "黑胡椒", "洋葱", "黄油", "生抽"],
            "tools": ["平底锅", "铲子", "刀"],
            "cost": 42.0,
            "calories": 380,
            "difficulty": "中等",
            "cook_time": "15分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "黑椒香浓，牛肉嫩滑",
            "steps": ["牛柳切片腌制", "炒香洋葱", "翻炒牛肉"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=black%20pepper%20beef%20tenderloin%20western&image_size=square_hd"
        },
        {
            "id": "w14",
            "name": "蔬菜沙拉",
            "category": "western",
            "ingredients": ["生菜", "番茄", "黄瓜", "橄榄油", "沙拉酱"],
            "tools": ["碗", "刀"],
            "cost": 12.0,
            "calories": 180,
            "difficulty": "简单",
            "cook_time": "5分钟",
            "season": ["夏季"],
            "description": "清爽健康，低卡美味",
            "steps": ["蔬菜洗净切块", "加入沙拉酱拌匀"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=vegetable%20salad%20western%20healthy%20dish&image_size=square_hd"
        },
        {
            "id": "w15",
            "name": "意式番茄汤",
            "category": "western",
            "ingredients": ["番茄", "洋葱", "大蒜", "橄榄油", "盐"],
            "tools": ["汤锅", "搅拌机"],
            "cost": 10.0,
            "calories": 150,
            "difficulty": "简单",
            "cook_time": "20分钟",
            "season": ["夏季"],
            "description": "酸甜可口，开胃解腻",
            "steps": ["炒香洋葱大蒜", "加入番茄炖煮", "搅拌成泥"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=italian%20tomato%20soup%20western%20dish&image_size=square_hd"
        },
        {
            "id": "w16",
            "name": "烤蔬菜串",
            "category": "western",
            "ingredients": ["彩椒", "洋葱", "蘑菇", "橄榄油", "香草"],
            "tools": ["烤箱", "烤串签"],
            "cost": 15.0,
            "calories": 180,
            "difficulty": "简单",
            "cook_time": "20分钟",
            "season": ["夏季"],
            "description": "色彩丰富，健康美味",
            "steps": ["蔬菜切块穿串", "刷油调味", "烤箱烘烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=grilled%20vegetable%20skewers%20western%20dish&image_size=square_hd"
        },
        {
            "id": "w17",
            "name": "奶油焗饭",
            "category": "western",
            "ingredients": ["米饭", "奶油", "芝士", "培根", "蘑菇"],
            "tools": ["烤箱", "烤盘", "锅"],
            "cost": 22.0,
            "calories": 450,
            "difficulty": "中等",
            "cook_time": "25分钟",
            "season": ["秋季", "冬季"],
            "description": "芝士香浓，口感丰富",
            "steps": ["炒香培根蘑菇", "加入米饭奶油", "撒芝士焗烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cream%20baked%20rice%20western%20dish&image_size=square_hd"
        },
        {
            "id": "w18",
            "name": "炸鸡",
            "category": "western",
            "ingredients": ["鸡肉", "面粉", "面包糠", "盐", "胡椒"],
            "tools": ["炸锅", "碗"],
            "cost": 25.0,
            "calories": 520,
            "difficulty": "中等",
            "cook_time": "20分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "外酥里嫩，经典美味",
            "steps": ["鸡肉腌制", "裹粉油炸"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=fried%20chicken%20western%20crispy&image_size=square_hd"
        },
        {
            "id": "w19",
            "name": "法式洋葱汤",
            "category": "western",
            "ingredients": ["洋葱", "牛肉汤", "面包", "芝士", "黄油"],
            "tools": ["汤锅", "烤箱"],
            "cost": 18.0,
            "calories": 340,
            "difficulty": "中等",
            "cook_time": "30分钟",
            "season": ["冬季"],
            "description": "法式经典，温暖暖胃",
            "steps": ["洋葱炒至金黄", "加入牛肉汤炖煮", "面包芝士焗烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=french%20onion%20soup%20western%20classic&image_size=square_hd"
        },
        {
            "id": "w20",
            "name": "烤龙虾",
            "category": "western",
            "ingredients": ["龙虾", "黄油", "大蒜", "柠檬", "迷迭香"],
            "tools": ["烤箱", "烤盘", "剪刀"],
            "cost": 98.0,
            "calories": 420,
            "difficulty": "较难",
            "cook_time": "20分钟",
            "season": ["夏季"],
            "description": "鲜美无比，宴客首选",
            "steps": ["龙虾处理", "涂抹黄油蒜蓉", "烤箱烘烤"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=grilled%20lobster%20western%20seafood&image_size=square_hd"
        }
    ],
    "special": [
        {
            "id": "s1",
            "name": "寿司拼盘",
            "category": "special",
            "ingredients": ["寿司米", "海苔", "三文鱼", "金枪鱼", "黄瓜"],
            "tools": ["寿司帘", "刀", "竹制工具"],
            "cost": 35.0,
            "calories": 400,
            "difficulty": "较难",
            "cook_time": "40分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "日式经典，新鲜美味",
            "steps": ["煮寿司饭", "准备食材", "卷寿司", "切件装盘"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sushi%20platter%20japanese%20food&image_size=square_hd"
        },
        {
            "id": "s2",
            "name": "泰式冬阴功汤",
            "category": "special",
            "ingredients": ["虾", "蘑菇", "青柠", "香茅", "椰奶"],
            "tools": ["汤锅", "铲子"],
            "cost": 28.0,
            "calories": 260,
            "difficulty": "中等",
            "cook_time": "25分钟",
            "season": ["夏季"],
            "description": "酸辣鲜香，开胃爽口",
            "steps": ["爆香调料", "加入高汤", "煮虾和蘑菇", "加入椰奶"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=tom%20yum%20soup%20thai%20food%20spicy&image_size=square_hd"
        },
        {
            "id": "s3",
            "name": "墨西哥塔可",
            "category": "special",
            "ingredients": ["玉米饼", "牛肉末", "生菜", "番茄", "莎莎酱"],
            "tools": ["炒锅", "刀", "砧板"],
            "cost": 16.0,
            "calories": 340,
            "difficulty": "简单",
            "cook_time": "20分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "墨西哥风味，香辣可口",
            "steps": ["炒牛肉末", "准备配菜", "组装塔可"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=mexican%20tacos%20food%20colorful&image_size=square_hd"
        },
        {
            "id": "s4",
            "name": "印度咖喱鸡",
            "category": "special",
            "ingredients": ["鸡肉", "咖喱粉", "洋葱", "土豆", "椰奶"],
            "tools": ["炒锅", "炖锅", "铲子"],
            "cost": 22.0,
            "calories": 380,
            "difficulty": "中等",
            "cook_time": "35分钟",
            "season": ["秋季", "冬季"],
            "description": "浓郁咖喱香，配饭绝佳",
            "steps": ["炒香洋葱", "加入咖喱粉", "加入鸡肉土豆", "炖煮"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=indian%20curry%20chicken%20food&image_size=square_hd"
        },
        {
            "id": "s5",
            "name": "越南春卷",
            "category": "special",
            "ingredients": ["春卷皮", "虾仁", "米粉", "生菜", "薄荷"],
            "tools": ["碗", "砧板", "刀"],
            "cost": 12.0,
            "calories": 180,
            "difficulty": "中等",
            "cook_time": "15分钟",
            "season": ["夏季"],
            "description": "清爽开胃，越南特色",
            "steps": ["春卷皮浸泡", "准备馅料", "卷春卷", "蘸酱食用"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=vietnamese%20spring%20rolls%20fresh%20food&image_size=square_hd"
        },
        {
            "id": "s6",
            "name": "韩式拌饭",
            "category": "special",
            "ingredients": ["米饭", "牛肉", "蔬菜", "鸡蛋", "拌饭酱"],
            "tools": ["炒锅", "碗", "勺子"],
            "cost": 18.0,
            "calories": 420,
            "difficulty": "简单",
            "cook_time": "20分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "色彩丰富，营养均衡",
            "steps": ["准备食材", "煎蛋", "拌饭拌匀"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=korean%20bibimbap%20food%20colorful&image_size=square_hd"
        },
        {
            "id": "s7",
            "name": "日式拉面",
            "category": "special",
            "ingredients": ["拉面", "叉烧肉", "鸡蛋", "海带", "味噌"],
            "tools": ["煮锅", "汤锅", "碗"],
            "cost": 25.0,
            "calories": 450,
            "difficulty": "中等",
            "cook_time": "30分钟",
            "season": ["冬季"],
            "description": "浓郁汤底，筋道面条",
            "steps": ["熬制汤底", "煮面条", "组装拉面"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=japanese%20ramen%20noodles%20food&image_size=square_hd"
        },
        {
            "id": "s8",
            "name": "越南河粉",
            "category": "special",
            "ingredients": ["河粉", "牛肉", "牛骨", "香菜", "青柠"],
            "tools": ["煮锅", "汤锅"],
            "cost": 22.0,
            "calories": 320,
            "difficulty": "中等",
            "cook_time": "40分钟",
            "season": ["冬季"],
            "description": "清淡鲜美，牛肉香浓",
            "steps": ["熬制牛骨汤", "煮河粉", "组装河粉"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=vietnamese%20pho%20noodle%20soup&image_size=square_hd"
        },
        {
            "id": "s9",
            "name": "韩式炸鸡",
            "category": "special",
            "ingredients": ["鸡肉", "面粉", "面包糠", "韩式辣酱", "蜂蜜"],
            "tools": ["炸锅", "碗"],
            "cost": 28.0,
            "calories": 480,
            "difficulty": "较难",
            "cook_time": "30分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "外酥里嫩，甜辣可口",
            "steps": ["鸡肉腌制", "裹粉油炸", "刷酱"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=korean%20fried%20chicken%20food&image_size=square_hd"
        },
        {
            "id": "s10",
            "name": "泰国咖喱",
            "category": "special",
            "ingredients": ["鸡肉", "椰奶", "咖喱酱", "土豆", "胡萝卜"],
            "tools": ["炒锅", "炖锅"],
            "cost": 25.0,
            "calories": 360,
            "difficulty": "中等",
            "cook_time": "30分钟",
            "season": ["秋季", "冬季"],
            "description": "椰香浓郁，微辣开胃",
            "steps": ["炒香咖喱酱", "加入鸡肉", "加椰奶炖煮"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=thai%20curry%20chicken%20food&image_size=square_hd"
        },
        {
            "id": "s11",
            "name": "印度飞饼",
            "category": "special",
            "ingredients": ["面粉", "黄油", "盐", "水"],
            "tools": ["平底锅", "擀面杖"],
            "cost": 8.0,
            "calories": 320,
            "difficulty": "较难",
            "cook_time": "15分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "薄脆可口，层次分明",
            "steps": ["和面", "擀薄", "煎炸"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=indian%20naan%20bread%20food&image_size=square_hd"
        },
        {
            "id": "s12",
            "name": "日式天妇罗",
            "category": "special",
            "ingredients": ["虾", "蔬菜", "面粉", "鸡蛋", "天妇罗粉"],
            "tools": ["炸锅", "碗"],
            "cost": 32.0,
            "calories": 420,
            "difficulty": "较难",
            "cook_time": "20分钟",
            "season": ["夏季"],
            "description": "外酥里嫩，清淡不腻",
            "steps": ["食材处理", "裹粉", "油炸"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=japanese%20tempura%20food&image_size=square_hd"
        },
        {
            "id": "s13",
            "name": "韩式辣白菜",
            "category": "special",
            "ingredients": ["白菜", "辣椒粉", "大蒜", "生姜", "鱼露"],
            "tools": ["盆", "密封容器"],
            "cost": 10.0,
            "calories": 120,
            "difficulty": "中等",
            "cook_time": "30分钟+发酵",
            "season": ["秋季"],
            "description": "酸辣爽脆，开胃小菜",
            "steps": ["白菜腌制", "调制酱料", "涂抹发酵"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=korean%20kimchi%20food%20fermented&image_size=square_hd"
        },
        {
            "id": "s14",
            "name": "印尼炒饭",
            "category": "special",
            "ingredients": ["米饭", "虾仁", "鸡蛋", "酱油", "虾酱"],
            "tools": ["炒锅", "铲子"],
            "cost": 18.0,
            "calories": 380,
            "difficulty": "中等",
            "cook_time": "20分钟",
            "season": ["春季", "夏季", "秋季", "冬季"],
            "description": "风味独特，香气浓郁",
            "steps": ["炒香配料", "加入米饭翻炒", "调味"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=indonesian%20fried%20rice%20food&image_size=square_hd"
        },
        {
            "id": "s15",
            "name": "菲律宾阿多波",
            "category": "special",
            "ingredients": ["鸡肉", "酱油", "醋", "大蒜", "月桂叶"],
            "tools": ["炖锅", "铲子"],
            "cost": 20.0,
            "calories": 320,
            "difficulty": "简单",
            "cook_time": "40分钟",
            "season": ["秋季", "冬季"],
            "description": "酸甜咸香，菲律宾经典",
            "steps": ["鸡肉煎至金黄", "加入调料炖煮", "收汁"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=filipino%20adobo%20chicken%20food&image_size=square_hd"
        },
        {
            "id": "s16",
            "name": "马来咖喱",
            "category": "special",
            "ingredients": ["鸡肉", "椰奶", "咖喱叶", "香茅", "辣椒"],
            "tools": ["炒锅", "炖锅"],
            "cost": 26.0,
            "calories": 360,
            "difficulty": "中等",
            "cook_time": "35分钟",
            "season": ["秋季", "冬季"],
            "description": "椰香浓郁，香辣可口",
            "steps": ["爆香香料", "加入鸡肉", "加椰奶炖煮"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=malaysian%20curry%20chicken%20food&image_size=square_hd"
        },
        {
            "id": "s17",
            "name": "新加坡辣椒蟹",
            "category": "special",
            "ingredients": ["螃蟹", "辣椒", "番茄酱", "蛋", "姜"],
            "tools": ["炒锅", "铲子"],
            "cost": 58.0,
            "calories": 420,
            "difficulty": "较难",
            "cook_time": "30分钟",
            "season": ["夏季"],
            "description": "香辣浓郁，新加坡名菜",
            "steps": ["螃蟹处理", "爆香调料", "加入螃蟹翻炒"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=singapore%20chili%20crab%20food&image_size=square_hd"
        },
        {
            "id": "s18",
            "name": "摩洛哥炖菜",
            "category": "special",
            "ingredients": ["鸡肉", "鹰嘴豆", "胡萝卜", "洋葱", "香料"],
            "tools": ["炖锅", "铲子"],
            "cost": 28.0,
            "calories": 340,
            "difficulty": "中等",
            "cook_time": "60分钟",
            "season": ["冬季"],
            "description": "香料丰富，异域风味",
            "steps": ["炒香洋葱", "加入鸡肉和蔬菜", "慢炖入味"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=moroccan%20tagine%20chicken%20food&image_size=square_hd"
        },
        {
            "id": "s19",
            "name": "土耳其烤肉",
            "category": "special",
            "ingredients": ["羊肉", "洋葱", "大蒜", "孜然", "辣椒粉"],
            "tools": ["烤箱", "烤肉架"],
            "cost": 52.0,
            "calories": 460,
            "difficulty": "中等",
            "cook_time": "40分钟",
            "season": ["秋季", "冬季"],
            "description": "香气扑鼻，异域风味",
            "steps": ["羊肉腌制", "烤箱烘烤", "切片"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=turkish%20kebab%20food%20grilled&image_size=square_hd"
        },
        {
            "id": "s20",
            "name": "希腊沙拉",
            "category": "special",
            "ingredients": ["黄瓜", "番茄", "洋葱", "菲达芝士", "橄榄油"],
            "tools": ["碗", "刀"],
            "cost": 16.0,
            "calories": 280,
            "difficulty": "简单",
            "cook_time": "5分钟",
            "season": ["夏季"],
            "description": "清爽健康，地中海风味",
            "steps": ["蔬菜切块", "加入芝士和橄榄油"],
            "image": "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=greek%20salad%20food%20healthy&image_size=square_hd"
        }
    ]
}

INGREDIENT_PRICES = {
    "鸡肉": 28.0, "花生米": 15.0, "干辣椒": 8.0, "花椒": 35.0, "葱": 3.0,
    "姜": 5.0, "蒜": 6.0, "猪肉丝": 32.0, "木耳": 20.0, "胡萝卜": 4.0,
    "青椒": 5.0, "豆腐": 3.0, "肉末": 28.0, "豆瓣酱": 12.0, "花椒粉": 15.0,
    "葱花": 3.0, "猪里脊": 45.0, "淀粉": 8.0, "番茄酱": 10.0, "白糖": 6.0,
    "醋": 8.0, "五花肉": 35.0, "冰糖": 12.0, "酱油": 10.0, "料酒": 12.0,
    "鲈鱼": 45.0, "蒸鱼豉油": 15.0, "红椒": 6.0, "牛排": 120.0, "橄榄油": 80.0,
    "黄油": 40.0, "大蒜": 6.0, "迷迭香": 15.0, "牛肉末": 42.0, "番茄": 5.0,
    "洋葱": 4.0, "意面": 12.0, "蘑菇": 12.0, "奶油": 25.0, "面粉": 8.0,
    "鸡翅": 30.0, "蜂蜜": 35.0, "生抽": 10.0, "生菜": 5.0, "鸡胸肉": 25.0,
    "帕玛森芝士": 60.0, "凯撒酱": 20.0, "面包丁": 10.0, "寿司米": 15.0, "海苔": 20.0,
    "三文鱼": 80.0, "金枪鱼": 90.0, "黄瓜": 4.0, "虾": 60.0, "青柠": 8.0,
    "香茅": 12.0, "椰奶": 15.0, "玉米饼": 15.0, "莎莎酱": 18.0, "咖喱粉": 15.0,
    "土豆": 4.0, "鸡蛋": 6.0, "蚝油": 12.0, "老鸭": 55.0, "冬瓜": 3.0,
    "枸杞": 40.0, "牛奶": 8.0, "黑胡椒": 15.0, "柠檬": 5.0, "春卷皮": 18.0,
    "米粉": 8.0, "薄荷": 10.0, "牛肉": 45.0, "拌饭酱": 15.0, "叉烧肉": 40.0,
    "海带": 12.0, "味噌": 20.0, "盐": 3.0, "西兰花": 8.0, "蒜苗": 5.0,
    "甜面酱": 10.0, "草鱼": 30.0, "酸菜": 6.0, "泡椒": 10.0, "酱料": 15.0,
    "汉堡面包": 8.0, "牛肉饼": 25.0, "羊排": 60.0, "披萨面团": 10.0, "芝士": 50.0,
    "香肠": 20.0, "牛骨": 25.0, "香菜": 5.0, "韩式辣酱": 20.0, "面包糠": 10.0,
    "咖喱酱": 18.0, "天妇罗粉": 15.0, "河粉": 8.0, "排骨": 35.0, "虾仁": 65.0,
    "青菜": 4.0, "茄子": 5.0, "培根": 30.0, "彩椒": 6.0, "香草": 12.0,
    "月桂叶": 8.0, "鱼露": 15.0, "虾酱": 18.0, "鹰嘴豆": 12.0, "螃蟹": 85.0,
    "香料": 15.0, "扇贝": 45.0, "粉丝": 8.0, "大闸蟹": 120.0, "龙虾": 150.0,
    "菲达芝士": 55.0, "羊肉": 55.0, "孜然": 12.0, "辣椒粉": 8.0
}

INGREDIENT_CALORIES = {
    "鸡肉": 165, "花生米": 567, "干辣椒": 320, "花椒": 316, "葱": 30,
    "姜": 41, "蒜": 126, "猪肉丝": 271, "木耳": 25, "胡萝卜": 41,
    "青椒": 25, "豆腐": 70, "肉末": 280, "豆瓣酱": 180, "花椒粉": 300,
    "葱花": 30, "猪里脊": 155, "淀粉": 345, "番茄酱": 80, "白糖": 390,
    "醋": 30, "五花肉": 430, "冰糖": 390, "酱油": 60, "料酒": 150,
    "鲈鱼": 105, "蒸鱼豉油": 80, "红椒": 30, "牛排": 250, "橄榄油": 884,
    "黄油": 717, "大蒜": 126, "迷迭香": 130, "牛肉末": 280, "番茄": 18,
    "洋葱": 40, "意面": 350, "蘑菇": 26, "奶油": 300, "面粉": 345,
    "鸡翅": 190, "蜂蜜": 300, "生抽": 60, "生菜": 16, "鸡胸肉": 120,
    "帕玛森芝士": 450, "凯撒酱": 450, "面包丁": 350, "寿司米": 116, "海苔": 250,
    "三文鱼": 200, "金枪鱼": 180, "黄瓜": 15, "虾": 80, "青柠": 30,
    "香茅": 90, "椰奶": 300, "玉米饼": 250, "莎莎酱": 120, "咖喱粉": 350,
    "土豆": 77, "鸡蛋": 143, "蚝油": 110, "老鸭": 180, "冬瓜": 12,
    "枸杞": 250, "牛奶": 54, "黑胡椒": 250, "柠檬": 29, "春卷皮": 280,
    "米粉": 130, "薄荷": 70, "牛肉": 250, "拌饭酱": 180, "叉烧肉": 300,
    "海带": 15, "味噌": 105, "盐": 0, "西兰花": 34, "蒜苗": 25,
    "甜面酱": 150, "草鱼": 110, "酸菜": 25, "泡椒": 80, "酱料": 180,
    "汉堡面包": 250, "牛肉饼": 280, "羊排": 300, "披萨面团": 280, "芝士": 400,
    "香肠": 280, "牛骨": 15, "香菜": 20, "韩式辣酱": 150, "面包糠": 350,
    "咖喱酱": 200, "天妇罗粉": 350, "河粉": 130, "排骨": 260, "虾仁": 80,
    "青菜": 20, "茄子": 25, "培根": 300, "彩椒": 30, "香草": 150,
    "月桂叶": 150, "鱼露": 100, "虾酱": 180, "鹰嘴豆": 160, "螃蟹": 100,
    "香料": 300, "扇贝": 120, "粉丝": 345, "大闸蟹": 105, "龙虾": 90,
    "菲达芝士": 400, "羊肉": 280, "孜然": 350, "辣椒粉": 350
}


def get_all_recipes():
    all_recipes = []
    for category in RECIPES_DATA.values():
        all_recipes.extend(category)
    return all_recipes


def get_recipes_by_category(category):
    return RECIPES_DATA.get(category, [])


def search_by_ingredients(selected_ingredients):
    """食材标签筛选：所选食材必须是菜谱食材的子集"""
    if not selected_ingredients:
        return get_all_recipes()
    
    result = []
    selected_set = set(selected_ingredients)
    
    for category in RECIPES_DATA.values():
        for recipe in category:
            recipe_ingredients = set(recipe["ingredients"])
            # 所选食材必须是菜谱食材的子集
            if selected_set.issubset(recipe_ingredients):
                result.append(recipe)
    
    return result


def search_by_keyword(keyword):
    """关键词搜索"""
    if not keyword:
        return get_all_recipes()
    
    keyword = keyword.lower()
    result = []
    
    for category in RECIPES_DATA.values():
        for recipe in category:
            if keyword in recipe["name"].lower() or \
               keyword in recipe["description"].lower() or \
               any(keyword in ing.lower() for ing in recipe["ingredients"]):
                result.append(recipe)
    
    return result


def get_all_ingredients():
    """获取所有食材"""
    ingredients = set()
    for category in RECIPES_DATA.values():
        for recipe in category:
            ingredients.update(recipe["ingredients"])
    return sorted(list(ingredients))


def get_all_tools():
    """获取所有工具"""
    tools = set()
    for category in RECIPES_DATA.values():
        for recipe in category:
            tools.update(recipe["tools"])
    return sorted(list(tools))


def calculate_total_cost(ingredients):
    """计算食材总成本"""
    total = 0.0
    for ing in ingredients:
        total += INGREDIENT_PRICES.get(ing, 0)
    return round(total, 2)


def calculate_total_calories(ingredients):
    """计算总热量"""
    total = 0
    for ing in ingredients:
        total += INGREDIENT_CALORIES.get(ing, 0)
    return total


def get_seasonal_recipes(season):
    """获取时令菜谱"""
    result = []
    for category in RECIPES_DATA.values():
        for recipe in category:
            if season in recipe["season"]:
                result.append(recipe)
    return result


def toggle_favorite(recipe_id):
    """切换收藏状态"""
    if recipe_id in USER_PREFERENCES["favorites"]:
        USER_PREFERENCES["favorites"].remove(recipe_id)
    else:
        USER_PREFERENCES["favorites"].append(recipe_id)


def mark_cooked(recipe_id):
    """标记已烹饪"""
    if recipe_id not in USER_PREFERENCES["cooked_history"]:
        USER_PREFERENCES["cooked_history"].append(recipe_id)


def get_favorite_recipes():
    """获取收藏的菜谱"""
    result = []
    fav_ids = USER_PREFERENCES["favorites"]
    for category in RECIPES_DATA.values():
        for recipe in category:
            if recipe["id"] in fav_ids:
                result.append(recipe)
    return result


def get_cooked_recipes():
    """获取已烹饪的菜谱"""
    result = []
    cooked_ids = USER_PREFERENCES["cooked_history"]
    for category in RECIPES_DATA.values():
        for recipe in category:
            if recipe["id"] in cooked_ids:
                result.append(recipe)
    return result


def recommend_recipes():
    """智能推荐菜谱"""
    all_recipes = get_all_recipes()
    
    if USER_PREFERENCES["view_history"]:
        last_viewed_id = USER_PREFERENCES["view_history"][-1]
        last_viewed = None
        for category in RECIPES_DATA.values():
            for recipe in category:
                if recipe["id"] == last_viewed_id:
                    last_viewed = recipe
                    break
        
        if last_viewed:
            recommendations = []
            viewed_category = last_viewed["category"]
            for recipe in RECIPES_DATA.get(viewed_category, []):
                if recipe["id"] != last_viewed_id:
                    recommendations.append(recipe)
            if recommendations:
                return random.sample(recommendations, min(5, len(recommendations)))
    
    return random.sample(all_recipes, min(5, len(all_recipes)))


def generate_recipe_id(category):
    """生成新菜谱ID"""
    existing_ids = set()
    for recipe in RECIPES_DATA[category]:
        existing_ids.add(recipe["id"])
    
    prefix = category[0]
    counter = 1
    while f"{prefix}{counter}" in existing_ids:
        counter += 1
    
    return f"{prefix}{counter}"


def save_new_recipe(name, category, ingredients, tools, cost, calories, difficulty, cook_time, season, description, steps):
    """保存新菜谱到上下文和数据存储"""
    category_key = category.lower()
    if category_key not in RECIPES_DATA:
        category_key = "chinese"
    
    new_recipe = {
        "id": generate_recipe_id(category_key),
        "name": name,
        "category": category_key,
        "ingredients": [i.strip() for i in ingredients.split(",") if i.strip()],
        "tools": [t.strip() for t in tools.split(",") if t.strip()],
        "cost": float(cost) if cost else 0.0,
        "calories": int(calories) if calories else 0,
        "difficulty": difficulty,
        "cook_time": cook_time,
        "season": [s.strip() for s in season.split(",") if s.strip()],
        "description": description,
        "steps": [s.strip() for s in steps.split("\\n") if s.strip()],
        "image": f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={name}%20food%20dish&image_size=square_hd"
    }
    
    # 保存到上下文
    NEW_RECIPE_CONTEXT["current_draft"] = new_recipe
    NEW_RECIPE_CONTEXT["saved_recipes"].append(new_recipe)
    
    # 添加到主数据存储
    RECIPES_DATA[category_key].append(new_recipe)
    
    # 更新食材价格和热量字典（如果有新食材）
    for ing in new_recipe["ingredients"]:
        if ing not in INGREDIENT_PRICES:
            INGREDIENT_PRICES[ing] = 10.0  # 默认价格
        if ing not in INGREDIENT_CALORIES:
            INGREDIENT_CALORIES[ing] = 100  # 默认热量
    
    return f"✅ 菜谱「{name}」已成功保存！"


def get_new_recipes():
    """获取新增的菜谱"""
    return NEW_RECIPE_CONTEXT["saved_recipes"]


def format_recipe_card(recipe):
    """格式化菜谱卡片"""
    is_favorite = recipe["id"] in USER_PREFERENCES["favorites"]
    is_cooked = recipe["id"] in USER_PREFERENCES["cooked_history"]
    
    favorite_icon = "❤️" if is_favorite else "🤍"
    cooked_badge = "✅" if is_cooked else ""
    
    ingredients_html = "<div style='margin-bottom: 8px;'>"
    ingredients_html += "<span style='color: #666; font-size: 14px;'>食材：</span>"
    ingredients_html += ", ".join(recipe["ingredients"])
    ingredients_html += "</div>"
    
    tools_html = "<div style='margin-bottom: 8px;'>"
    tools_html += "<span style='color: #666; font-size: 14px;'>工具：</span>"
    tools_html += ", ".join(recipe["tools"])
    tools_html += "</div>"
    
    steps_html = "<div style='margin-top: 12px;'>"
    steps_html += "<span style='color: #666; font-size: 14px;'>步骤：</span>"
    steps_html += "<ol style='margin: 4px 0 0 20px; padding: 0;'>"
    for i, step in enumerate(recipe["steps"], 1):
        steps_html += f"<li style='font-size: 13px; line-height: 1.6; margin-bottom: 4px;'>{step}</li>"
    steps_html += "</ol></div>"
    
    js_event_options = '{"bubbles":true}'
    fav_action = f"toggle_favorite:{recipe['id']}"
    cook_action = f"mark_cooked:{recipe['id']}"
    
    return """
    <div style="border: 1px solid #e0e0e0; border-radius: 12px; padding: 16px; margin-bottom: 16px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; gap: 16px;">
            <img src="{}" alt="{}" style="width: 140px; height: 140px; object-fit: cover; border-radius: 8px;">
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin: 0 0 8px 0; color: #333; font-size: 18px;">{} {}</h3>
                        <span style="display: inline-block; padding: 2px 8px; background: #f0f0f0; border-radius: 12px; font-size: 12px; color: #666;">
                            {}
                        </span>
                        <span style="display: inline-block; padding: 2px 8px; background: #fff3e0; border-radius: 12px; font-size: 12px; color: #e65100; margin-left: 8px;">
                            ⏱️ {}
                        </span>
                    </div>
                    <button id="favorite-{}" style="background: none; border: none; font-size: 20px; cursor: pointer; padding: 0;" onclick="var el=document.querySelector('#action-input textarea');if(!el)el=document.querySelector('#action-input input');if(el){{el.value='{}';el.dispatchEvent(new Event('input',{}));}}">{}</button>
                </div>
                <p style="margin: 8px 0; color: #666; font-size: 14px; line-height: 1.5;">{}</p>
                {}
                {}
                <div style="display: flex; gap: 12px; margin-top: 8px;">
                    <span style="color: #666; font-size: 14px;">💰 ¥{}</span>
                    <span style="color: #666; font-size: 14px;">🔥 {}卡</span>
                </div>
                <div style="margin-top: 8px;">
                    <span style="color: #666; font-size: 14px;">时令：</span>
                    {}
                </div>
                {}
                <button id="cook-{}" style="margin-top: 12px; padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px;" onclick="var el=document.querySelector('#action-input textarea');if(!el)el=document.querySelector('#action-input input');if(el){{el.value='{}';el.dispatchEvent(new Event('input',{}));}}">
                    {}
                </button>
            </div>
        </div>
    </div>
    """.format(
        recipe['image'], recipe['name'],
        recipe['name'], cooked_badge,
        recipe['difficulty'], recipe['cook_time'],
        recipe['id'], fav_action, js_event_options, favorite_icon,
        recipe['description'], ingredients_html, tools_html,
        recipe['cost'], recipe['calories'],
        ", ".join(recipe['season']), steps_html,
        recipe['id'], cook_action, js_event_options,
        '已烹饪' if is_cooked else '标记已烹饪'
    )


def render_recipes(recipes):
    """渲染菜谱列表"""
    if not recipes:
        return "<div style='text-align: center; padding: 40px; color: #999;'>暂无匹配的菜谱</div>"
    
    html = ""
    for recipe in recipes:
        html += format_recipe_card(recipe)
    
    return html


def handle_action(action):
    """处理用户操作"""
    if action.startswith("toggle_favorite:"):
        recipe_id = action.split(":")[1]
        toggle_favorite(recipe_id)
    elif action.startswith("mark_cooked:"):
        recipe_id = action.split(":")[1]
        mark_cooked(recipe_id)
    elif action.startswith("view_recipe:"):
        recipe_id = action.split(":")[1]
        if recipe_id not in USER_PREFERENCES["view_history"]:
            USER_PREFERENCES["view_history"].append(recipe_id)


def create_gradio_ui():
    """创建Gradio界面 - 使用原生组件"""
    with gr.Blocks(title="EC_EachChef - 智能菜谱助手") as demo:
        gr.Markdown("# 🍳 EC_EachChef - 智能菜谱助手")
        gr.Markdown("发现美味，轻松烹饪！")
        
        # 状态存储
        current_recipe_id = gr.State(value=None)
        current_recipes_list = gr.State(value=get_all_recipes())
        
        with gr.Tabs():
            with gr.TabItem("📖 浏览菜谱"):
                with gr.Row():
                    category_radio = gr.Radio(
                        choices=["全部", "中餐", "西餐", "特色菜"],
                        label="选择分类",
                        value="全部"
                    )
                
                with gr.Row():
                    search_input = gr.Textbox(
                        placeholder="搜索菜谱名称、描述或食材...",
                        label="关键词搜索",
                        scale=2
                    )
                    search_btn = gr.Button("🔍 搜索", scale=1)
                
                # 菜谱选择区域
                recipe_selector = gr.Dropdown(
                    label="选择菜谱查看详情",
                    choices=[r['name'] for r in get_all_recipes()],
                    value=None
                )
                
                # 菜谱详情区域
                with gr.Column(visible=False) as recipe_detail:
                    detail_image = gr.Image(height=200, show_label=False)
                    detail_name = gr.Markdown()
                    detail_info = gr.Markdown()
                    detail_ingredients = gr.Markdown()
                    detail_tools = gr.Markdown()
                    detail_cost = gr.Markdown()
                    detail_season = gr.Markdown()
                    detail_desc = gr.Markdown()
                    with gr.Accordion("查看步骤", open=False):
                        detail_steps = gr.Markdown()
                    
                    with gr.Row():
                        favorite_btn = gr.Button("🤍 收藏", variant="secondary")
                        cooked_btn = gr.Button("标记已烹饪", variant="primary")
                    
                    action_status = gr.Markdown()
                
                # 辅助函数
                def get_recipe_by_name(name, recipes):
                    for r in recipes:
                        if r['name'] == name:
                            return r
                    return None
                
                def show_recipe_detail(name, recipes):
                    recipe = get_recipe_by_name(name, recipes)
                    if not recipe:
                        return [
                            gr.Column(visible=False), None, None, "", "", "", "", "", "", "", "",
                            "🤍 收藏", "标记已烹饪", ""
                        ]
                    
                    is_fav = recipe['id'] in USER_PREFERENCES['favorites']
                    is_cooked = recipe['id'] in USER_PREFERENCES['cooked_history']
                    fav_icon = "❤️ 已收藏" if is_fav else "🤍 收藏"
                    cooked_text = "✅ 已烹饪" if is_cooked else "标记已烹饪"
                    cooked_badge = "✅" if is_cooked else ""
                    
                    return [
                        gr.Column(visible=True),
                        recipe['id'],
                        recipe['image'],
                        f"### {recipe['name']} {cooked_badge}",
                        f"**难度:** {recipe['difficulty']} | **时间:** ⏱️ {recipe['cook_time']}",
                        f"**食材:** {', '.join(recipe['ingredients'])}",
                        f"**工具:** {', '.join(recipe['tools'])}",
                        f"**成本:** 💰 ¥{recipe['cost']} | **热量:** 🔥 {recipe['calories']}卡",
                        f"**时令:** {', '.join(recipe['season'])}",
                        f"**描述:** {recipe['description']}",
                        "**步骤:**\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe['steps'])]),
                        fav_icon,
                        cooked_text,
                        ""
                    ]
                
                def toggle_favorite_action(recipe_id, recipes):
                    if recipe_id:
                        toggle_favorite(recipe_id)
                        recipe = None
                        for r in recipes:
                            if r['id'] == recipe_id:
                                recipe = r
                                break
                        if recipe:
                            is_fav = recipe['id'] in USER_PREFERENCES['favorites']
                            fav_icon = "❤️ 已收藏" if is_fav else "🤍 收藏"
                            return f"{'已添加到收藏 ❤️' if is_fav else '已取消收藏'}", fav_icon
                    return "请先选择菜谱", "🤍 收藏"
                
                def mark_cooked_action(recipe_id, recipes):
                    if recipe_id:
                        mark_cooked(recipe_id)
                        recipe = None
                        for r in recipes:
                            if r['id'] == recipe_id:
                                recipe = r
                                break
                        if recipe:
                            is_cooked = recipe['id'] in USER_PREFERENCES['cooked_history']
                            cooked_text = "✅ 已烹饪" if is_cooked else "标记已烹饪"
                            return f"{'已标记为烹饪 ✅' if is_cooked else '已取消烹饪标记'}", cooked_text
                    return "请先选择菜谱", "标记已烹饪"
                
                def filter_by_category(cat):
                    if cat == "全部":
                        recipes = get_all_recipes()
                    else:
                        recipes = get_recipes_by_category(cat.lower())
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                def search_recipes(keyword):
                    recipes = search_by_keyword(keyword)
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                # 绑定事件
                category_radio.change(
                    fn=filter_by_category,
                    inputs=category_radio,
                    outputs=[current_recipes_list, recipe_selector]
                )
                
                search_btn.click(
                    fn=search_recipes,
                    inputs=search_input,
                    outputs=[current_recipes_list, recipe_selector]
                )
                
                search_input.submit(
                    fn=search_recipes,
                    inputs=search_input,
                    outputs=[current_recipes_list, recipe_selector]
                )
                
                recipe_selector.change(
                    fn=show_recipe_detail,
                    inputs=[recipe_selector, current_recipes_list],
                    outputs=[
                        recipe_detail, current_recipe_id, detail_image,
                        detail_name, detail_info, detail_ingredients, detail_tools,
                        detail_cost, detail_season, detail_desc, detail_steps,
                        favorite_btn, cooked_btn, action_status
                    ]
                )
                
                favorite_btn.click(
                    fn=toggle_favorite_action,
                    inputs=[current_recipe_id, current_recipes_list],
                    outputs=[action_status, favorite_btn]
                )
                
                cooked_btn.click(
                    fn=mark_cooked_action,
                    inputs=[current_recipe_id, current_recipes_list],
                    outputs=[action_status, cooked_btn]
                )
                
                # 新增菜谱表单
                with gr.Accordion("➕ 按模板新增菜谱", open=False):
                    gr.Markdown("### 📝 填写菜谱信息")
                    
                    with gr.Row():
                        new_recipe_name = gr.Textbox(label="菜谱名称", placeholder="请输入菜谱名称")
                        new_recipe_category = gr.Dropdown(
                            choices=["中餐", "西餐", "特色菜"],
                            label="分类",
                            value="中餐"
                        )
                    
                    with gr.Row():
                        new_recipe_difficulty = gr.Dropdown(
                            choices=["简单", "中等", "较难"],
                            label="难度",
                            value="中等"
                        )
                        new_recipe_cook_time = gr.Textbox(label="烹饪时间", placeholder="如：20分钟")
                    
                    with gr.Row():
                        new_recipe_cost = gr.Number(label="成本(元)", value=0.0)
                        new_recipe_calories = gr.Number(label="热量(卡)", value=0)
                    
                    new_recipe_ingredients = gr.Textbox(
                        label="食材（用逗号分隔）",
                        placeholder="鸡肉, 花生米, 干辣椒"
                    )
                    
                    new_recipe_tools = gr.Textbox(
                        label="工具（用逗号分隔）",
                        placeholder="炒锅, 铲子, 刀"
                    )
                    
                    new_recipe_season = gr.Textbox(
                        label="时令（用逗号分隔）",
                        placeholder="春季, 夏季, 秋季, 冬季"
                    )
                    
                    new_recipe_description = gr.Textbox(
                        label="描述",
                        placeholder="请描述这道菜的特点"
                    )
                    
                    new_recipe_steps = gr.Textbox(
                        label="步骤（每行一个步骤）",
                        placeholder="步骤1\n步骤2\n步骤3",
                        lines=4
                    )
                    
                    save_status = gr.Textbox(label="保存状态", interactive=False)
                    
                    with gr.Row():
                        save_recipe_btn = gr.Button("💾 保存菜谱", variant="primary")
                        reset_form_btn = gr.Button("🔄 重置表单")
                    
                    def handle_save_new(name, category, difficulty, cook_time, cost, calories, ingredients, tools, season, description, steps, recipes):
                        if not name:
                            return "❌ 请输入菜谱名称！", recipes, gr.Dropdown()
                        if not ingredients:
                            return "❌ 请输入食材！", recipes, gr.Dropdown()
                        if not steps:
                            return "❌ 请输入步骤！", recipes, gr.Dropdown()
                        
                        result = save_new_recipe(name, category, ingredients, tools, cost, calories, difficulty, cook_time, season, description, steps)
                        new_recipes = get_all_recipes()
                        return result, new_recipes, gr.Dropdown(choices=[r['name'] for r in new_recipes])
                    
                    def reset_new_form():
                        return ["", "中餐", "中等", "", 0.0, 0, "", "", "", "", "", ""]
                    
                    save_recipe_btn.click(
                        fn=handle_save_new,
                        inputs=[
                            new_recipe_name, new_recipe_category, new_recipe_difficulty,
                            new_recipe_cook_time, new_recipe_cost, new_recipe_calories,
                            new_recipe_ingredients, new_recipe_tools, new_recipe_season,
                            new_recipe_description, new_recipe_steps, current_recipes_list
                        ],
                        outputs=[save_status, current_recipes_list, recipe_selector]
                    )
                    
                    reset_form_btn.click(
                        fn=reset_new_form,
                        outputs=[
                            new_recipe_name, new_recipe_category, new_recipe_difficulty,
                            new_recipe_cook_time, new_recipe_cost, new_recipe_calories,
                            new_recipe_ingredients, new_recipe_tools, new_recipe_season,
                            new_recipe_description, new_recipe_steps, save_status
                        ]
                    )
            
            with gr.TabItem("🧅 食材筛选"):
                with gr.Row():
                    ingredient_checkboxes = gr.CheckboxGroup(
                        choices=get_all_ingredients(),
                        label="选择食材（所选食材必须是菜谱食材的子集）",
                        info="选中的食材将作为筛选条件，系统会显示所有可以用这些食材制作的菜谱"
                    )
                
                with gr.Row():
                    filter_btn = gr.Button("🔍 筛选菜谱")
                    clear_btn = gr.Button("🗑️ 清空选择")
                
                filter_recipe_selector = gr.Dropdown(
                    label="选择菜谱查看详情",
                    choices=[r['name'] for r in get_all_recipes()],
                    value=None
                )
                
                with gr.Column(visible=False) as filter_recipe_detail:
                    filter_detail_image = gr.Image(height=200, show_label=False)
                    filter_detail_name = gr.Markdown()
                    filter_detail_info = gr.Markdown()
                    filter_detail_ingredients = gr.Markdown()
                    filter_detail_tools = gr.Markdown()
                    filter_detail_cost = gr.Markdown()
                    filter_detail_season = gr.Markdown()
                    filter_detail_desc = gr.Markdown()
                    with gr.Accordion("查看步骤", open=False):
                        filter_detail_steps = gr.Markdown()
                    
                    with gr.Row():
                        filter_favorite_btn = gr.Button("🤍 收藏", variant="secondary")
                        filter_cooked_btn = gr.Button("标记已烹饪", variant="primary")
                    
                    filter_action_status = gr.Markdown()
                
                filter_current_recipe_id = gr.State(value=None)
                filter_current_recipes_list = gr.State(value=get_all_recipes())
                
                def filter_by_ingredients_action(selected):
                    recipes = search_by_ingredients(selected)
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                def show_filter_recipe_detail(name, recipes):
                    recipe = get_recipe_by_name(name, recipes)
                    if not recipe:
                        return [
                            gr.Column(visible=False), None, None, "", "", "", "", "", "", "", "",
                            "🤍 收藏", "标记已烹饪", ""
                        ]
                    
                    is_fav = recipe['id'] in USER_PREFERENCES['favorites']
                    is_cooked = recipe['id'] in USER_PREFERENCES['cooked_history']
                    fav_icon = "❤️ 已收藏" if is_fav else "🤍 收藏"
                    cooked_text = "✅ 已烹饪" if is_cooked else "标记已烹饪"
                    cooked_badge = "✅" if is_cooked else ""
                    
                    return [
                        gr.Column(visible=True),
                        recipe['id'],
                        recipe['image'],
                        f"### {recipe['name']} {cooked_badge}",
                        f"**难度:** {recipe['difficulty']} | **时间:** ⏱️ {recipe['cook_time']}",
                        f"**食材:** {', '.join(recipe['ingredients'])}",
                        f"**工具:** {', '.join(recipe['tools'])}",
                        f"**成本:** 💰 ¥{recipe['cost']} | **热量:** 🔥 {recipe['calories']}卡",
                        f"**时令:** {', '.join(recipe['season'])}",
                        f"**描述:** {recipe['description']}",
                        "**步骤:**\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe['steps'])]),
                        fav_icon,
                        cooked_text,
                        ""
                    ]
                
                filter_btn.click(
                    fn=filter_by_ingredients_action,
                    inputs=ingredient_checkboxes,
                    outputs=[filter_current_recipes_list, filter_recipe_selector]
                )
                
                clear_btn.click(
                    fn=lambda: ([], get_all_recipes(), gr.Dropdown(choices=[r['name'] for r in get_all_recipes()], value=None)),
                    outputs=[ingredient_checkboxes, filter_current_recipes_list, filter_recipe_selector]
                )
                
                ingredient_checkboxes.change(
                    fn=filter_by_ingredients_action,
                    inputs=ingredient_checkboxes,
                    outputs=[filter_current_recipes_list, filter_recipe_selector]
                )
                
                filter_recipe_selector.change(
                    fn=show_filter_recipe_detail,
                    inputs=[filter_recipe_selector, filter_current_recipes_list],
                    outputs=[
                        filter_recipe_detail, filter_current_recipe_id, filter_detail_image,
                        filter_detail_name, filter_detail_info, filter_detail_ingredients, filter_detail_tools,
                        filter_detail_cost, filter_detail_season, filter_detail_desc, filter_detail_steps,
                        filter_favorite_btn, filter_cooked_btn, filter_action_status
                    ]
                )
                
                filter_favorite_btn.click(
                    fn=toggle_favorite_action,
                    inputs=[filter_current_recipe_id, filter_current_recipes_list],
                    outputs=[filter_action_status, filter_favorite_btn]
                )
                
                filter_cooked_btn.click(
                    fn=mark_cooked_action,
                    inputs=[filter_current_recipe_id, filter_current_recipes_list],
                    outputs=[filter_action_status, filter_cooked_btn]
                )
            
            with gr.TabItem("✨ 智能推荐"):
                with gr.Row():
                    season_dropdown = gr.Dropdown(
                        choices=["春季", "夏季", "秋季", "冬季"],
                        label="选择季节",
                        value="春季"
                    )
                
                with gr.Row():
                    recommend_btn = gr.Button("🎲 随机推荐")
                    seasonal_btn = gr.Button("🌸 时令推荐")
                
                recommend_recipe_selector = gr.Dropdown(
                    label="选择菜谱查看详情",
                    choices=[],
                    value=None
                )
                
                with gr.Column(visible=False) as recommend_recipe_detail:
                    recommend_detail_image = gr.Image(height=200, show_label=False)
                    recommend_detail_name = gr.Markdown()
                    recommend_detail_info = gr.Markdown()
                    recommend_detail_ingredients = gr.Markdown()
                    recommend_detail_tools = gr.Markdown()
                    recommend_detail_cost = gr.Markdown()
                    recommend_detail_season = gr.Markdown()
                    recommend_detail_desc = gr.Markdown()
                    with gr.Accordion("查看步骤", open=False):
                        recommend_detail_steps = gr.Markdown()
                    
                    with gr.Row():
                        recommend_favorite_btn = gr.Button("🤍 收藏", variant="secondary")
                        recommend_cooked_btn = gr.Button("标记已烹饪", variant="primary")
                    
                    recommend_action_status = gr.Markdown()
                
                recommend_current_recipe_id = gr.State(value=None)
                recommend_current_recipes_list = gr.State(value=[])
                
                def get_random_recommendations():
                    recipes = recommend_recipes()
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                def get_seasonal_recommendations(season):
                    recipes = get_seasonal_recipes(season)
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                def show_recommend_recipe_detail(name, recipes):
                    recipe = get_recipe_by_name(name, recipes)
                    if not recipe:
                        return [
                            gr.Column(visible=False), None, None, "", "", "", "", "", "", "", "",
                            "🤍 收藏", "标记已烹饪", ""
                        ]
                    
                    is_fav = recipe['id'] in USER_PREFERENCES['favorites']
                    is_cooked = recipe['id'] in USER_PREFERENCES['cooked_history']
                    fav_icon = "❤️ 已收藏" if is_fav else "🤍 收藏"
                    cooked_text = "✅ 已烹饪" if is_cooked else "标记已烹饪"
                    cooked_badge = "✅" if is_cooked else ""
                    
                    return [
                        gr.Column(visible=True),
                        recipe['id'],
                        recipe['image'],
                        f"### {recipe['name']} {cooked_badge}",
                        f"**难度:** {recipe['difficulty']} | **时间:** ⏱️ {recipe['cook_time']}",
                        f"**食材:** {', '.join(recipe['ingredients'])}",
                        f"**工具:** {', '.join(recipe['tools'])}",
                        f"**成本:** 💰 ¥{recipe['cost']} | **热量:** 🔥 {recipe['calories']}卡",
                        f"**时令:** {', '.join(recipe['season'])}",
                        f"**描述:** {recipe['description']}",
                        "**步骤:**\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe['steps'])]),
                        fav_icon,
                        cooked_text,
                        ""
                    ]
                
                recommend_btn.click(
                    fn=get_random_recommendations,
                    outputs=[recommend_current_recipes_list, recommend_recipe_selector]
                )
                
                seasonal_btn.click(
                    fn=get_seasonal_recommendations,
                    inputs=season_dropdown,
                    outputs=[recommend_current_recipes_list, recommend_recipe_selector]
                )
                
                recommend_recipe_selector.change(
                    fn=show_recommend_recipe_detail,
                    inputs=[recommend_recipe_selector, recommend_current_recipes_list],
                    outputs=[
                        recommend_recipe_detail, recommend_current_recipe_id, recommend_detail_image,
                        recommend_detail_name, recommend_detail_info, recommend_detail_ingredients, recommend_detail_tools,
                        recommend_detail_cost, recommend_detail_season, recommend_detail_desc, recommend_detail_steps,
                        recommend_favorite_btn, recommend_cooked_btn, recommend_action_status
                    ]
                )
                
                recommend_favorite_btn.click(
                    fn=toggle_favorite_action,
                    inputs=[recommend_current_recipe_id, recommend_current_recipes_list],
                    outputs=[recommend_action_status, recommend_favorite_btn]
                )
                
                recommend_cooked_btn.click(
                    fn=mark_cooked_action,
                    inputs=[recommend_current_recipe_id, recommend_current_recipes_list],
                    outputs=[recommend_action_status, recommend_cooked_btn]
                )
            
            with gr.TabItem("❤️ 我的收藏"):
                favorites_recipe_selector = gr.Dropdown(
                    label="选择收藏菜谱查看详情",
                    choices=[r['name'] for r in get_favorite_recipes()],
                    value=None
                )
                refresh_favorites_btn = gr.Button("🔄 刷新")
                
                with gr.Column(visible=False) as favorites_recipe_detail:
                    favorites_detail_image = gr.Image(height=200, show_label=False)
                    favorites_detail_name = gr.Markdown()
                    favorites_detail_info = gr.Markdown()
                    favorites_detail_ingredients = gr.Markdown()
                    favorites_detail_tools = gr.Markdown()
                    favorites_detail_cost = gr.Markdown()
                    favorites_detail_season = gr.Markdown()
                    favorites_detail_desc = gr.Markdown()
                    with gr.Accordion("查看步骤", open=False):
                        favorites_detail_steps = gr.Markdown()
                    
                    with gr.Row():
                        favorites_favorite_btn = gr.Button("❤️ 已收藏", variant="secondary")
                        favorites_cooked_btn = gr.Button("标记已烹饪", variant="primary")
                    
                    favorites_action_status = gr.Markdown()
                
                favorites_current_recipe_id = gr.State(value=None)
                favorites_current_recipes_list = gr.State(value=get_favorite_recipes())
                
                def refresh_favorites_action():
                    recipes = get_favorite_recipes()
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                def show_favorites_recipe_detail(name, recipes):
                    recipe = get_recipe_by_name(name, recipes)
                    if not recipe:
                        return [
                            gr.Column(visible=False), None, None, "", "", "", "", "", "", "", "",
                            "❤️ 已收藏", "标记已烹饪", ""
                        ]
                    
                    is_fav = recipe['id'] in USER_PREFERENCES['favorites']
                    is_cooked = recipe['id'] in USER_PREFERENCES['cooked_history']
                    fav_icon = "❤️ 已收藏" if is_fav else "🤍 收藏"
                    cooked_text = "✅ 已烹饪" if is_cooked else "标记已烹饪"
                    cooked_badge = "✅" if is_cooked else ""
                    
                    return [
                        gr.Column(visible=True),
                        recipe['id'],
                        recipe['image'],
                        f"### {recipe['name']} {cooked_badge}",
                        f"**难度:** {recipe['difficulty']} | **时间:** ⏱️ {recipe['cook_time']}",
                        f"**食材:** {', '.join(recipe['ingredients'])}",
                        f"**工具:** {', '.join(recipe['tools'])}",
                        f"**成本:** 💰 ¥{recipe['cost']} | **热量:** 🔥 {recipe['calories']}卡",
                        f"**时令:** {', '.join(recipe['season'])}",
                        f"**描述:** {recipe['description']}",
                        "**步骤:**\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe['steps'])]),
                        fav_icon,
                        cooked_text,
                        ""
                    ]
                
                refresh_favorites_btn.click(
                    fn=refresh_favorites_action,
                    outputs=[favorites_current_recipes_list, favorites_recipe_selector]
                )
                
                favorites_recipe_selector.change(
                    fn=show_favorites_recipe_detail,
                    inputs=[favorites_recipe_selector, favorites_current_recipes_list],
                    outputs=[
                        favorites_recipe_detail, favorites_current_recipe_id, favorites_detail_image,
                        favorites_detail_name, favorites_detail_info, favorites_detail_ingredients, favorites_detail_tools,
                        favorites_detail_cost, favorites_detail_season, favorites_detail_desc, favorites_detail_steps,
                        favorites_favorite_btn, favorites_cooked_btn, favorites_action_status
                    ]
                )
                
                favorites_cooked_btn.click(
                    fn=mark_cooked_action,
                    inputs=[favorites_current_recipe_id, favorites_current_recipes_list],
                    outputs=[favorites_action_status, favorites_cooked_btn]
                )
            
            with gr.TabItem("📝 烹饪记录"):
                cooked_recipe_selector = gr.Dropdown(
                    label="选择已烹饪菜谱查看详情",
                    choices=[r['name'] for r in get_cooked_recipes()],
                    value=None
                )
                refresh_cooked_btn = gr.Button("🔄 刷新")
                
                with gr.Column(visible=False) as cooked_recipe_detail:
                    cooked_detail_image = gr.Image(height=200, show_label=False)
                    cooked_detail_name = gr.Markdown()
                    cooked_detail_info = gr.Markdown()
                    cooked_detail_ingredients = gr.Markdown()
                    cooked_detail_tools = gr.Markdown()
                    cooked_detail_cost = gr.Markdown()
                    cooked_detail_season = gr.Markdown()
                    cooked_detail_desc = gr.Markdown()
                    with gr.Accordion("查看步骤", open=False):
                        cooked_detail_steps = gr.Markdown()
                    
                    with gr.Row():
                        cooked_favorite_btn = gr.Button("🤍 收藏", variant="secondary")
                        cooked_cooked_btn = gr.Button("✅ 已烹饪", variant="primary")
                    
                    cooked_action_status = gr.Markdown()
                
                cooked_current_recipe_id = gr.State(value=None)
                cooked_current_recipes_list = gr.State(value=get_cooked_recipes())
                
                def refresh_cooked_action():
                    recipes = get_cooked_recipes()
                    return recipes, gr.Dropdown(choices=[r['name'] for r in recipes], value=None)
                
                def show_cooked_recipe_detail(name, recipes):
                    recipe = get_recipe_by_name(name, recipes)
                    if not recipe:
                        return [
                            gr.Column(visible=False), None, None, "", "", "", "", "", "", "", "",
                            "🤍 收藏", "✅ 已烹饪", ""
                        ]
                    
                    is_fav = recipe['id'] in USER_PREFERENCES['favorites']
                    is_cooked = recipe['id'] in USER_PREFERENCES['cooked_history']
                    fav_icon = "❤️ 已收藏" if is_fav else "🤍 收藏"
                    cooked_text = "✅ 已烹饪" if is_cooked else "标记已烹饪"
                    cooked_badge = "✅" if is_cooked else ""
                    
                    return [
                        gr.Column(visible=True),
                        recipe['id'],
                        recipe['image'],
                        f"### {recipe['name']} {cooked_badge}",
                        f"**难度:** {recipe['difficulty']} | **时间:** ⏱️ {recipe['cook_time']}",
                        f"**食材:** {', '.join(recipe['ingredients'])}",
                        f"**工具:** {', '.join(recipe['tools'])}",
                        f"**成本:** 💰 ¥{recipe['cost']} | **热量:** 🔥 {recipe['calories']}卡",
                        f"**时令:** {', '.join(recipe['season'])}",
                        f"**描述:** {recipe['description']}",
                        "**步骤:**\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe['steps'])]),
                        fav_icon,
                        cooked_text,
                        ""
                    ]
                
                refresh_cooked_btn.click(
                    fn=refresh_cooked_action,
                    outputs=[cooked_current_recipes_list, cooked_recipe_selector]
                )
                
                cooked_recipe_selector.change(
                    fn=show_cooked_recipe_detail,
                    inputs=[cooked_recipe_selector, cooked_current_recipes_list],
                    outputs=[
                        cooked_recipe_detail, cooked_current_recipe_id, cooked_detail_image,
                        cooked_detail_name, cooked_detail_info, cooked_detail_ingredients, cooked_detail_tools,
                        cooked_detail_cost, cooked_detail_season, cooked_detail_desc, cooked_detail_steps,
                        cooked_favorite_btn, cooked_cooked_btn, cooked_action_status
                    ]
                )
                
                cooked_favorite_btn.click(
                    fn=toggle_favorite_action,
                    inputs=[cooked_current_recipe_id, cooked_current_recipes_list],
                    outputs=[cooked_action_status, cooked_favorite_btn]
                )
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_ui()
    demo.launch(
        debug=True, 
        theme=gr.themes.Soft(),
        share=True
    )