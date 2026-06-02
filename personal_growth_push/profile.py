from __future__ import annotations

USER_PROFILE = {
    "name": "Kovan",
    "gender": "male",
    "birthday": "2006-09-14",
    "height_cm": 178,
    "weight_kg": 80,
    "goal": "90 days body recomposition: reduce to about 75 kg, gain strength, build English and news habits.",
}

WEEKDAY_KEYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)

TRAINING_PLAN = {
    "monday": {
        "title": "Push",
        "focus": "卧推主项、肩推稳定、胸肩三头容量。全程保留 1-2 次余力，不做硬顶。",
        "exercises": [
            {"name": "杠铃卧推", "sets": 4, "reps": "5-6", "load": "70kg 起", "rest": "2-3 min", "note": "每组肩胛后缩下沉，最后一组不要失败。"},
            {"name": "上斜哑铃卧推", "sets": 3, "reps": "8-10", "load": "中等重量", "rest": "90 sec", "note": "顶端不要撞铃，控制下放。"},
            {"name": "哑铃推肩", "sets": 4, "reps": "6-8", "load": "22.5kg 附近", "rest": "2 min", "note": "肋骨收住，避免腰椎代偿。"},
            {"name": "双杠臂屈伸或窄距卧推", "sets": 3, "reps": "8-10", "load": "自重/轻中等", "rest": "90 sec", "note": "肘部轨迹稳定，胸口不塌。"},
            {"name": "哑铃飞鸟", "sets": 3, "reps": "12-15", "load": "15kg 附近", "rest": "75 sec", "note": "动作幅度宁可略小，也不要肩前顶。"},
            {"name": "侧平举", "sets": 4, "reps": "12-20", "load": "轻中等", "rest": "60 sec", "note": "用肩带动，不用斜方肌耸肩。"},
            {"name": "绳索下压", "sets": 3, "reps": "10-15", "load": "中等", "rest": "60 sec", "note": "最后 2 次接近吃力即可。"},
        ],
    },
    "tuesday": {
        "title": "Pull",
        "focus": "引体向上质量、划船力量、硬拉技术入门。背部动作先稳住躯干再发力。",
        "exercises": [
            {"name": "引体向上", "sets": 4, "reps": "6-10", "load": "自重", "rest": "2 min", "note": "能稳定 10 次后加 2.5kg 负重。"},
            {"name": "杠铃划船", "sets": 4, "reps": "6-8", "load": "60kg 起", "rest": "2 min", "note": "背角固定，杠铃拉向下腹。"},
            {"name": "硬拉技术组", "sets": 3, "reps": "5", "load": "70-80kg", "rest": "2-3 min", "note": "刚开始阶段只练路径和背部张力。"},
            {"name": "坐姿划船", "sets": 3, "reps": "10-12", "load": "中等", "rest": "90 sec", "note": "顶峰夹背 1 秒。"},
            {"name": "高位下拉", "sets": 3, "reps": "10-12", "load": "中等", "rest": "90 sec", "note": "肘向下走，不要只用手拉。"},
            {"name": "面拉", "sets": 3, "reps": "15-20", "load": "轻", "rest": "60 sec", "note": "保护肩后束和肩袖。"},
            {"name": "哑铃弯举", "sets": 3, "reps": "10-12", "load": "中等", "rest": "60 sec", "note": "手腕中立，避免甩动。"},
        ],
    },
    "wednesday": {
        "title": "Legs",
        "focus": "深蹲做组能力、股四头容量、后链基础。今天不追重量，追每组深度一致。",
        "exercises": [
            {"name": "杠铃深蹲", "sets": 4, "reps": "6-8", "load": "75-80kg", "rest": "2-3 min", "note": "每组速度稳定，核心先收紧再下蹲。"},
            {"name": "罗马尼亚硬拉", "sets": 3, "reps": "8-10", "load": "60-70kg", "rest": "2 min", "note": "髋向后推，感受腘绳肌拉伸。"},
            {"name": "腿举", "sets": 3, "reps": "10-12", "load": "中等偏重", "rest": "90 sec", "note": "膝盖跟随脚尖方向。"},
            {"name": "保加利亚分腿蹲", "sets": 3, "reps": "8-10/侧", "load": "自重或哑铃", "rest": "90 sec", "note": "先用稳定动作换训练量。"},
            {"name": "腿弯举", "sets": 3, "reps": "10-15", "load": "中等", "rest": "75 sec", "note": "不要借助惯性甩起。"},
            {"name": "站姿提踵", "sets": 4, "reps": "12-18", "load": "中等", "rest": "60 sec", "note": "底部停顿，顶端收缩。"},
            {"name": "平板支撑", "sets": 3, "reps": "45-60 sec", "load": "自重", "rest": "60 sec", "note": "骨盆微后倾，腰不塌。"},
        ],
    },
    "thursday": {
        "title": "Cardio Recovery",
        "focus": "恢复、心肺、活动度。强度控制在能完整说话的区间。",
        "exercises": [
            {"name": "Zone 2 有氧", "sets": 1, "reps": "35-45 min", "load": "跑步机/椭圆机/单车", "rest": "-", "note": "心率大约 120-145，出汗但不硬撑。"},
            {"name": "髋踝活动度", "sets": 3, "reps": "8-10/动作", "load": "自重", "rest": "短休", "note": "深蹲踝背屈、髋外旋、腘绳肌动态拉伸。"},
            {"name": "肩胛稳定", "sets": 3, "reps": "12-15", "load": "弹力带", "rest": "60 sec", "note": "面拉、外旋、肩胛俯卧撑任选。"},
            {"name": "轻核心", "sets": 3, "reps": "10-12", "load": "自重", "rest": "60 sec", "note": "死虫或鸟狗，追求控制。"},
        ],
    },
    "friday": {
        "title": "Upper",
        "focus": "上肢综合容量。卧推和划船维持强度，肩臂用泵感补量。",
        "exercises": [
            {"name": "杠铃卧推容量组", "sets": 4, "reps": "8", "load": "62.5-67.5kg", "rest": "2 min", "note": "比周一轻，动作更干净。"},
            {"name": "引体向上", "sets": 4, "reps": "6-9", "load": "自重", "rest": "2 min", "note": "每组留 1 次余力。"},
            {"name": "哑铃推肩", "sets": 3, "reps": "8-10", "load": "20-22.5kg", "rest": "90 sec", "note": "不要为了重量牺牲轨迹。"},
            {"name": "杠铃划船", "sets": 3, "reps": "8-10", "load": "55-60kg", "rest": "90 sec", "note": "顶峰收缩，不要耸肩。"},
            {"name": "哑铃飞鸟", "sets": 3, "reps": "12-15", "load": "12.5-15kg", "rest": "75 sec", "note": "胸肌拉伸清楚即可。"},
            {"name": "侧平举 + 绳索下压", "sets": 3, "reps": "15 + 12", "load": "轻中等", "rest": "60 sec", "note": "超级组，节省时间。"},
            {"name": "弯举", "sets": 3, "reps": "10-12", "load": "中等", "rest": "60 sec", "note": "手臂补量，不要练到肘痛。"},
        ],
    },
    "saturday": {
        "title": "Lower",
        "focus": "硬拉技术优先、下肢后链和臀腿补强。今天的目标是稳，不是冲极限。",
        "exercises": [
            {"name": "硬拉", "sets": 5, "reps": "3", "load": "70-80kg", "rest": "2-3 min", "note": "每次从地面重新建立张力。"},
            {"name": "暂停深蹲", "sets": 3, "reps": "5", "load": "60-65kg", "rest": "2 min", "note": "底部停 1 秒，练控制和深度。"},
            {"name": "臀推", "sets": 3, "reps": "8-10", "load": "中等偏重", "rest": "90 sec", "note": "顶端收臀，不要腰椎过伸。"},
            {"name": "腿弯举", "sets": 3, "reps": "10-15", "load": "中等", "rest": "75 sec", "note": "后链补量。"},
            {"name": "箭步蹲", "sets": 3, "reps": "10/侧", "load": "自重或哑铃", "rest": "90 sec", "note": "步幅稳定，膝盖别内扣。"},
            {"name": "提踵", "sets": 4, "reps": "12-18", "load": "中等", "rest": "60 sec", "note": "全幅度。"},
            {"name": "卷腹或悬垂举腿", "sets": 3, "reps": "10-15", "load": "自重", "rest": "60 sec", "note": "控制骨盆，不甩腿。"},
        ],
    },
    "sunday": {
        "title": "Rest",
        "focus": "完全休息或轻松散步。恢复也是训练的一部分。",
        "exercises": [
            {"name": "轻松步行", "sets": 1, "reps": "6000-9000 steps", "load": "低强度", "rest": "-", "note": "保持日常活动，不额外制造疲劳。"},
            {"name": "睡眠目标", "sets": 1, "reps": "7.5-9 h", "load": "-", "rest": "-", "note": "今晚优先睡眠和补水。"},
        ],
    },
}

MEAL_ROTATION = [
    [
        {"name": "早餐", "items": "燕麦 60g + 牛奶 250ml + 全蛋 2 个 + 希腊酸奶 150g", "protein": 38, "carbs": 58, "fat": 18},
        {"name": "午餐", "items": "米饭 220g + 鸡胸/鸡腿去皮 180g + 西兰花 + 橄榄油 8g", "protein": 52, "carbs": 78, "fat": 18},
        {"name": "训练前", "items": "香蕉 1 根 + 乳清半勺 + 黑咖啡", "protein": 18, "carbs": 38, "fat": 4},
        {"name": "训练后", "items": "乳清 1 勺 + 贝果/面包 1 个", "protein": 32, "carbs": 48, "fat": 3},
        {"name": "晚餐", "items": "三文鱼/瘦牛肉 170g + 土豆 250g + 沙拉", "protein": 46, "carbs": 50, "fat": 20},
    ],
    [
        {"name": "早餐", "items": "全麦吐司 2 片 + 鸡蛋 2 个 + 蛋清 2 个 + 苹果", "protein": 40, "carbs": 55, "fat": 20},
        {"name": "午餐", "items": "意面 100g 干重 + 牛肉末 160g + 番茄酱 + 蔬菜", "protein": 55, "carbs": 75, "fat": 17},
        {"name": "训练前", "items": "米饼 3 片 + 乳清半勺", "protein": 18, "carbs": 35, "fat": 5},
        {"name": "训练后", "items": "低脂巧克力奶 350ml + 香蕉", "protein": 33, "carbs": 45, "fat": 3},
        {"name": "晚餐", "items": "虾仁/鱼肉 200g + 红薯 250g + 炒青菜", "protein": 42, "carbs": 48, "fat": 21},
    ],
    [
        {"name": "早餐", "items": "无糖豆浆 400ml + 鸡蛋 2 个 + 玉米 1 根 + 酸奶", "protein": 39, "carbs": 60, "fat": 17},
        {"name": "午餐", "items": "米饭 200g + 瘦猪里脊 180g + 菌菇青菜", "protein": 50, "carbs": 76, "fat": 18},
        {"name": "训练前", "items": "燕麦能量杯：燕麦 35g + 乳清半勺", "protein": 20, "carbs": 36, "fat": 5},
        {"name": "训练后", "items": "乳清 1 勺 + 米饭团/饭团 1 个", "protein": 32, "carbs": 50, "fat": 3},
        {"name": "晚餐", "items": "鸡胸 180g + 荞麦面 80g 干重 + 拌蔬菜", "protein": 45, "carbs": 52, "fat": 20},
    ],
    [
        {"name": "早餐", "items": "蛋白奶昔 + 燕麦 50g + 蓝莓 + 花生酱 10g", "protein": 42, "carbs": 54, "fat": 19},
        {"name": "午餐", "items": "鸡肉卷饼 2 个 + 生菜番茄 + 低脂酱", "protein": 53, "carbs": 80, "fat": 16},
        {"name": "训练前", "items": "香蕉 + 酸奶 150g", "protein": 17, "carbs": 40, "fat": 4},
        {"name": "训练后", "items": "乳清 1 勺 + 白米饭 150g", "protein": 31, "carbs": 48, "fat": 3},
        {"name": "晚餐", "items": "牛排 160g + 南瓜/土豆 250g + 蔬菜", "protein": 45, "carbs": 45, "fat": 22},
    ],
    [
        {"name": "早餐", "items": "鸡蛋 2 个 + 蛋清 3 个 + 米饭 150g + 番茄", "protein": 41, "carbs": 52, "fat": 18},
        {"name": "午餐", "items": "咖喱鸡胸 180g + 米饭 230g + 青菜", "protein": 54, "carbs": 82, "fat": 17},
        {"name": "训练前", "items": "全麦面包 2 片 + 蜂蜜少量", "protein": 16, "carbs": 42, "fat": 5},
        {"name": "训练后", "items": "乳清 1 勺 + 橙汁/水果", "protein": 32, "carbs": 44, "fat": 2},
        {"name": "晚餐", "items": "鳕鱼 220g + 牛油果 50g + 红薯 220g + 沙拉", "protein": 44, "carbs": 46, "fat": 22},
    ],
    [
        {"name": "早餐", "items": "酸奶碗：希腊酸奶 250g + 燕麦 50g + 香蕉半根 + 坚果 10g", "protein": 40, "carbs": 58, "fat": 18},
        {"name": "午餐", "items": "牛肉饭：瘦牛肉 170g + 米饭 210g + 蔬菜", "protein": 52, "carbs": 78, "fat": 19},
        {"name": "训练前", "items": "米饼 3 片 + 低脂奶", "protein": 18, "carbs": 38, "fat": 4},
        {"name": "训练后", "items": "乳清 1 勺 + 贝果半个 + 水果", "protein": 31, "carbs": 47, "fat": 3},
        {"name": "晚餐", "items": "鸡腿去皮 200g + 土豆泥 220g + 蔬菜", "protein": 45, "carbs": 48, "fat": 20},
    ],
    [
        {"name": "早餐", "items": "全麦三明治：鸡胸 120g + 鸡蛋 1 个 + 生菜 + 牛奶", "protein": 42, "carbs": 56, "fat": 17},
        {"name": "午餐", "items": "日式照烧鱼/鸡 190g + 米饭 220g + 海带豆腐汤", "protein": 53, "carbs": 80, "fat": 16},
        {"name": "训练前", "items": "水果 + 乳清半勺", "protein": 18, "carbs": 36, "fat": 4},
        {"name": "训练后", "items": "乳清 1 勺 + 麦片 45g", "protein": 33, "carbs": 46, "fat": 4},
        {"name": "晚餐", "items": "瘦牛/鸡胸 180g + 荞麦/杂粮饭 + 大份蔬菜", "protein": 45, "carbs": 45, "fat": 22},
    ],
]
