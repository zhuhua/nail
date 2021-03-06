Nail make up mobile app
====

##接口地址 http://115.28.134.4/

##用户部分

###注册接口(停用，由登录代替)
	/api/user/register POST
	参数
		mobile 手机
		checkcode 验证码
		
###获取验证码
	/api/user/checkcode POST
	参数 
		mobile 手机
		返回 无 （验证码由短信发送至手机）

###登陆
	/api/user/login POST
	参数 
		mobile 手机
		password 密码(获取的验证码)
		返回登陆token

###获取个人信息
	/api/user/profile GET Header [Authorization: <token>]
	返回 用户对象
	{
	    "reg_time": 注册时间
	    "mobile": 手机号
	    "nick": 昵称
	    "avatar": 头像
	    "id": ID
	}
	
###更新个人信息
	/api/user/profile POST Header [Authorization: <token>]
	参数 
		nick 昵称
	
###修改密码
	/api/user/passwd POST Header [Authorization: <token>]
	参数 
		old_pwd 原密码
		password 新密码
	
###更新头像
	/api/user/avatar POST Header [Authorization: <token>]
	参数 
		file 图片文件
		
###添加常用地址
	/api/user/address POST Header [Authorization: <token>]
	参数 
		location 位置
		detail 详细地址
		is_default 是否为默认地址 1 是 0 否
	返回 地址对象列表
	[{
	    "id": ID,
	    "user_id": 用户ID,
	    "location": 位置,
	    "detail": 详细地址,
	    "create_time":,
	    "is_default": 0 是否为默认地址 1 是 0 否
	}]
		
###常用地址列表
	/api/user/addresses GET Header [Authorization: <token>]
	返回 地址对象列表
	[
	    {
            "create_time": "2015-03-18 16:50:27",
            "detail": "\u5317\u5927\u8857222222222",
            "id": 7,
            "is_default": 1,
            "location": "\u6210\u90fd\u5e02",
            "user_id": 3
            }
	]
###获取默认地址
    /api/user/address/default GET Header [Authorization: <token>]
    返回 地址对象
    {
    "create_time": "2015-03-18 16:50:27",
    "detail": "\u5317\u5927\u8857222222222",
    "id": 7,
    "is_default": 1,
    "location": "\u6210\u90fd\u5e02",
    "user_id": 3
    }
    
###设定默认地址
    /api/user/address/default POST Header [Authorization: <token>]
    参数 
        address_id 设定为默认地址的ID
     返回 地址对象列表
	[
	    {
            "create_time": "2015-03-18 16:50:27",
            "detail": "\u5317\u5927\u8857222222222",
            "id": 7,
            "is_default": 1,
            "location": "\u6210\u90fd\u5e02",
            "user_id": 3
            }
	]   
###删除常用地址
	/api/user/address/<地址ID> POST Header [Authorization: <token>]
	返回 地址对象列表
	[
	    {
            "create_time": "2015-03-18 16:50:27",
            "detail": "\u5317\u5927\u8857222222222",
            "id": 7,
            "is_default": 1,
            "location": "\u6210\u90fd\u5e02",
            "user_id": 3
            }
	]	
###添加收藏
	/api/user/favorite POST Header [Authorization: <token>]
	参数 
		type 类型 1 美甲师 2 美甲作品
		object_id 美甲师或美甲作品id
		
###收藏列表
	/api/user/favorites GET Header [Authorization: <token>]
	参数 
		type 类型 1 美甲师 2 美甲作品
		page 页码 可选 默认 1
		page_size 页大小 可选 默认 10
	返回美甲师或者美甲对象列表
	[
            {
                "artisan_id": 28000006,
                "brief": "asdf",
                "category_id": 1,
                "counts": {
                    "sale": 0
                },
                "create_time": "2015-01-23 16:19:32",
                "id": 19,
                "images": [],
                "name": "adfads",
                "price": 1111.0,
                "sale": 0,
                "status": 0,
                "tag_price": 11.0,
                "tags": [
                   
                ],
                "version": "2015-01-27 09:20:54"
            },
            {
                "artisan_id": 28000006,
                "brief": "阿斯顿发生的",
                "category_id": 1,
                "counts": {
                    "sale": 0
                },
                "create_time": "2015-02-06 17:03:20",
                "id": 28,
                "images": [],
                "name": "333333333333",
                "price": 222.0,
                "sale": 0,
                "status": 0,
                "tag_price": 222.0,
                "tags": [
                    "圣诞节",
                    "特价款"
                ],
                "version": "2015-02-06 09:03:20"
            }
        ]
		
###删除收藏
	/api/user/favorite/delete POST Header [Authorization: <token>]
	参数 
		type 类型 1 美甲师 2 美甲作品
		object_id 美甲师或美甲作品id
	返回美甲师或者美甲对象列表
        [
                {
                "artisan_id": 28000006,
                "brief": "阿斯顿发生的",
                "category_id": 1,
                "counts": {
                    "sale": 0
                },
                "create_time": "2015-02-06 17:03:20",
                "id": 28,
                "images": [],
                "name": "333333333333",
                "price": 222.0,
                "sale": 0,
                "status": 0,
                "tag_price": 222.0,
                "tags": [
                    "圣诞节",
                    "特价款"
                ],
                "version": "2015-02-06 09:03:20"
                }
        ]

##美甲师部分

###获取美甲师列表
	/api/artisans GET 
	参数
		order_by 排序字段 可选  [ level 等级 默认，avg_price 均价， counts_sale 人气 ]
		sort asc|desc 可选 默认 desc 范围 [asc 正序, desc 倒序]
		page 页码 可选 默认 1
		page_size 页大小 可选 默认 10
		name 可选 如传入是以美甲师名字搜索
	返回 美甲师对象列表

###获取美甲师信息
	/api/artisan/<美甲师ID> GET
	返回 美甲师 对象
	{
	    "name": 姓名,
	    "level": 等级,
	    "mobile": 手机号,
	    "gender": 性别 1 男 0 女,
	    "serv_area": 服务区域,
	    "brief": 简介,
	    "cert_pro": 专业美甲师,
	    "create_time": 创建时间,
	    "last_login": 最近登录时间,
	    "avatar": 头像,
	    "counts": {
	            "sample": 0, 作品数量
	            "sale": 0, 销量
                    "communication_rank": 40, 沟通评分 [0,50] 显示时请除10再显示
                    "professional_rank": 24 , 专业评分 [0,50] 显示时请除10再显示
                    "punctual_rank": 8, 守时评分 [0,50] 显示时请除10再显示
                    "score": 9， 积分
                    "evaluate_count": 0, 评价数
	    },
	    "cert_pop": 明星美甲师,
	    "avg_price": 均价,
	    "id": 28000006
	}
	
###我的大咖
    /api/my_mecat GET
    参数：
        order_by 排序字段 可选  [ create_time 时间 默认，price 均价， sales 人气 ]
        sort asc|desc 可选 默认 desc 范围 [asc 正序, desc 倒序]
        page 页码 可选 默认 1
        page_size 页大小 可选 默认 10
    返回：美甲师对象列表
    [
    {
        "avatar": "/img/35b141fa2ccff01430674be337f04dd8.png",
        "avg_price": 0.0,
        "brief": "如果你看过电视里演的清代历史剧就不难注意到剧中的后妃、贵妇们的纤纤玉指，以及指尖的华贵甲饰。指尖一转，手指无不散发出尊贵、华丽的贵族气息。也许从那时起，中国的女人们就注定与美甲结下了不解之缘，也许从那时起，女人们就已通过指甲来展示自己的美丽与气质。时代在变迁，社会在发展，技术在革新，不变的是美，不变的是悠久的文化，艺术家们说：“民族的，就是世界的。”中国的美甲技术发展到今天，我们是否还应记得历史的沉积呢？中国的美甲应具有中国的民族特色，通过这款美甲的设计，用艺术的形式，寓识着美甲的历史发展，让我们还记得中国曾经有过的美甲辉煌，而我们这些现代的美甲师更有理由把历史与民族特点融入艺术创作中。",
        "cert_pop": 0,
        "cert_pro": 0,
        "counts": {
            "communication_rank": 47,
            "professional_rank": 50,
            "punctual_rank": 46,
            "sale": 0,
            "sample": 0,
            "score": 9
        },
        "create_time": "2015-01-12 15:06:46",
        "gender": 1,
        "id": 28000006,
        "last_login": "2015-02-09 13:11:17",
        "level": 4,
        "mobile": "13812345678",
        "name": "美甲师33333",
        "password": "7c4a8d09ca3762af61e59520943dc26494f8941b",
        "serv_area": "哈哈哈， 哈哈哈"
    }
    ]
###删除我的大咖
    /api/my_mecat/delete  POST  Header [Authorization: <token>]
    参数
        artisan_id
    返回
        美甲师对象列表
##美甲作品部分

###获取标签列表
	/api/tags GET
	返回 标签对象列表
	{
	    "id": ID
	    "name": 标签名
	}
	
###获取分类列表
	/api/categories GET
	返回 分类对象列表
	{
	    "id": ID
	    "name": 名称
	}

###获取作品列表
	/api/samples
	参数
		category_id 类别ID 可选 [ 1:美甲 2:美睫 3:手足护理 4:空气净化 默认 '' 所有分类商品 ]
		order_by 排序字段 可选 默认 create_time  [ price 价格， counts_sale 销量 ]
		sort asc|desc 可选 默认 desc 范围 [asc 正序, desc 倒序]
		page 页码 可选 默认 1
		page_size 页大小 可选 默认 10
		artisan_id 可选 如传入则取得该美甲师的作品
		tag 可选 参数值[标签接口得到的name]
	返回 美甲作品对象列表

###获取作品详情
	/api/sample/<作品ID>
	{
	    "status": 状态 0 正常 1删除 ,
	    "name": 名称,
	    "tags": 标签,
	    "price": 价格,
	    "brief": 作品简介,
	    "counts": {
	        "sale": 0, 销量
	        "evaluate_count": 1, 评价数量 
	    },
	    "artisan_id": 美甲师Id,
	    "create_time": 创建时间,
	    "images":[
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
        ] 图片,
	    "category_id": 类别id,
	    "id": 12,
	    "is_fav": 是否收藏 0 未收藏 1，已经收藏,
	    "tag_price": 店面价
	}

##订单部分

###查看手艺人预约状态 接口 
    /api/appointment/status GET
    参数
        @param artisan_id: 手艺人ID
        @param appt_date: 预约日期 格式 2000-01-01
    返回
    数字表示一天中的时间， true表示可预约 false:表示不可预约
    {
    "10": true, 
    "11": false,
    "12": true,
    "13": true,
    "14": true,
    "15": true,
    "16": true,
    "17": true,
    "18": true,
    "19": true,
    "20": true,
    "21": true,
    }

###创建订单 接口
    /api/trade/create POST Header [Authorization: <token>]
    参数
        @param sample_id: 样品ID
        @param address: 服务地址
        @param appt_date: 预约日期 格式 2000-01-01
        @param appt_hour: 预约时间
        @param remark: 用户备注
    返回（订单详情对象）
    {
     服务地址
    "address": "\u706b\u536b31",
    手艺人头像
    "artisan_avatar": "/img/35b141fa2ccff01430674be337f04dd8.png",
    手艺人ID
    "artisan_id": 28000006,  
    手艺人名称
    "artisan_name": "\u7f8e\u7532\u5e0833333",
    买家头像
    "buyer_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
    买家昵称
    "buyer_name": "186", 
    订单封面
    "cover": '/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg',
    创建时间
    "create_time": "2015-02-09 14:49:04",
    是否显示给买家（即买家未删除）， 1 显示， 0 不显示
    "display_buyer": 1,
    是否显示给卖家（即卖家未删除）， 1 显示， 0 不显示
    "display_seller": 1,
    剩余过期时间（等待支付时间） 单位分钟
    "expire_remian": 30,
    订单ID
    "id": 12,
    是否评价 0 未评价 1 已评价 2 评价不可修改
    "is_reviewed": 0,
    订单号
    "order_no": "1423464544849774",
    订单实际消费价格
    "price": 222.0,
    买家备注
    "remark": "plkj",
    样品ID(商品)
    "sample_id": 28,
    样品名称(商品)
    "sample_name": "333333333333",
    样品标价(商品)
    "sample_price": 222.0,
    样品店面价(商品)
    "sample_tag_price": 222.0,
    样品描述
    "sample_brief": "\u963f\u65af\u987f\u53d1\u751f\u7684",
    订单状态  0'待支付',1'已支付', 2'已出发', 3'已到达', 4'已完成', 5'已取消', 6'已关闭', 7 '已过期'
    "status": 0,
    样品店面价(商品)
    "tag_price": 222.0,
    买家电话 
    "telephone": "18683591672",
    订单标题
    "title": "333333333333",
    交易号
    "trade_no": "1423464544849806",
    更新时间 
    "update_time": "2015-02-09 14:49:04",
    买家ID
    "user_id": 4
    }

###删除订单操作 接口：
    /api/order/delete POST Header [Authorization: <token>]
    参数
        @param order_id: 订单ID
        
    返回
     同 创建订单 接口
     
###用户交易操作 接口：
    /api/user/trade POST Header [Authorization: <token>]
    参数
        @param order_no: 订单号
        @param action: 交易操作 arrived, 用户确认手艺人已经到达; finish, 用户确认交易结束, cancel, 用户取消交易
        @param price: 实际费用 （可选）
    返回
     同 创建订单 接口
     
###订单详情 接口：
    /api/order GET Header [Authorization: <token>]
    参数
        @param order_no: 订单号
	@param with_log：是否显示流转日志 不传不显示  True显示
    {
    "address": "\u706b\u536b31",
    "artisan_avatar": "/img/35b141fa2ccff01430674be337f04dd8.png",
    "artisan_id": 28000006,
    "artisan_name": "\u7f8e\u7532\u5e0833333",
    "buyer_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
    "buyer_name": "18683591672",
    "cover": null,
    "create_time": "2015-03-11 23:29:02",
    "display_buyer": 1,
    "display_seller": 1,
    "expire_remian": 0,
    "id": 2,
    "is_reviewed": 1,
    "order_log": [
        {
            "create_time": "2015-03-11 23:29:02", 时间
            "id": 2,
            "order_id": 2,
            "trader_action": 0, (0 创建订单, 1， 用户支付, 2 手艺人出发, 3，手艺人到达, 4，交易完成 , 5，用户取消交易, 6，关闭交易,7，交易过期)
            "trader_id": 3, 交易发起者ID
            "trader_type": "USER" 交易发起者类型
        },
        {
            "create_time": "2015-03-12 18:00:02",
            "id": 12,
            "order_id": 2,
            "trader_action": 1,
            "trader_id": 3,
            "trader_type": "USER"
        },
        {
            "create_time": "2015-03-12 18:04:37",
            "id": 17,
            "order_id": 2,
            "trader_action": 2,
            "trader_id": 28000006,
            "trader_type": "ARTISAN"
        },
        {
            "create_time": "2015-03-12 18:05:00",
            "id": 24,
            "order_id": 2,
            "trader_action": 3,
            "trader_id": 3,
            "trader_type": "USER"
        },
        {
            "create_time": "2015-03-12 18:05:14",
            "id": 30,
            "order_id": 2,
            "trader_action": 4,
            "trader_id": 3,
            "trader_type": "USER"
        }
    ],
    "order_no": "1426087742571880",
    "price": 222.0,
    "remark": "1426087742.48",
    "sample_id": 28,
    "sample_name": "333333333333",
    "sample_price": 222.0,
    "sample_tag_price": 222.0,
    "status": 4,
    "tag_price": 222.0,
    "telephone": "18683591672",
    "title": "333333333333",
    "trade_no": "1426087742571978",
    "update_time": "2015-03-12 18:05:14",
    "user_id": 3
}
    
###用户订单列表 接口
    /api/orders GET Header [Authorization: <token>]
    参数
        @param status: 
        订单状态（不选为全部）订单状态  'wait_pay''待支付',unfinished（待完成), finished'已完成', other('已取消', '已关闭', '已过期')
        @param page: 
        @param page_size: 
    返回
    [
    {
    详情同 创建订单 接口
        "address": "\u706b\u536b28",
        "artisan_id": 28000006,
        "artisan_name": "\u7f8e\u7532\u5e0833333",
        "buyer_name": "186",
        "cover": "{'url': u'/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg', 'create_time': datetime.datetime(2015, 2, 9, 13, 33, 55), 'id': 86L, 'obj_id': u'e5d604c0ffbb39165fa3f59821907bc6'}",
        "create_time": "2015-02-09 13:34:12",
        "display_buyer": 1,
        "display_seller": 1,
        "id": 1,
        "is_reviewed": 0,
        "order_no": "1423460052979827",
        "price": 222.0,
        "remark": "plkj",
        "sample_id": 28,
        "sample_name": "333333333333",
        "sample_price": 222.0,
        "sample_tag_price": 222.0,
        "status": 1,
        "tag_price": 222.0,
        "telephone": "18683591672",
        "title": "333333333333",
        "trade_no": "1423460052979975",
        "update_time": "2015-02-09 14:05:43",
        "user_id": 4
    },
    {
        "address": "\u706b\u536b29",
        "artisan_id": 28000006,
        "artisan_name": "\u7f8e\u7532\u5e0833333",
        "buyer_name": "186",
        "cover": "{'url': u'/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg', 'create_time': datetime.datetime(2015, 2, 9, 13, 33, 55), 'id': 87L, 'obj_id': u'a0a1133a1ed84fb31f2e0757c5ec0355'}",
        "create_time": "2015-02-09 13:34:44",
        "display_buyer": 1,
        "display_seller": 1,
        "id": 2,
        "is_reviewed": 0,
        "order_no": "1423460084080167",
        "price": 222.0,
        "remark": "plkj",
        "sample_id": 29,
        "sample_name": "444444444444",
        "sample_price": 222.0,
        "sample_tag_price": 222.0,
        "status": 2,
        "tag_price": 222.0,
        "telephone": "18683591672",
        "title": "444444444444",
        "trade_no": "1423460084080306",
        "update_time": "2015-02-09 14:18:18",
        "user_id": 4
    },
    {
        "address": "\u706b\u536b29",
        "artisan_id": 28000006,
        "artisan_name": "\u7f8e\u7532\u5e0833333",
        "buyer_name": "186",
        "cover": "{'url': u'/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg', 'create_time': datetime.datetime(2015, 2, 9, 13, 33, 55), 'id': 87L, 'obj_id': u'a0a1133a1ed84fb31f2e0757c5ec0355'}",
        "create_time": "2015-02-09 13:37:29",
        "display_buyer": 1,
        "display_seller": 1,
        "id": 3,
        "is_reviewed": 0,
        "order_no": "1423460249596449",
        "price": 222.0,
        "remark": "plkj",
        "sample_id": 29,
        "sample_name": "444444444444",
        "sample_price": 222.0,
        "sample_tag_price": 222.0,
        "status": 5,
        "tag_price": 222.0,
        "telephone": "18683591672",
        "title": "444444444444",
        "trade_no": "1423460249596617",
        "update_time": "2015-02-09 14:08:02",
        "user_id": 4
    }
    ]
    
##评价部分

###添加评价
    /api/evaluate/add POST Header [Authorization: <token>]
    参数
    communication_rank 沟通评分 [1,5]
    content 评价内容
    file 图片列表(multipart 直接上传多个文件)
    object_id 评价样品ID
    professional_rank 专业评分 [1,5]
    punctual_rank 守时评分 [1,5]
    rating 评价品级 0 好评 1， 中评 2 差评
    order_no 评价来源订单号
    返回
    {
        "author_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg", 评价者头像
        "author_id": 4, 评价者
        "author_mobile": "18683591672", 评价者手机号
        "communication_rank": 2, 沟通评分 [1,5]
        "content": "drgdfg", 评价内容
        "create_time": "2015-02-10 11:47:59", 评价时间
        "id": 1,
         "images": [
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
        ],评价者 上传图片
        "is_block": 0, 是否屏蔽 0 不屏蔽 1 屏蔽（管理员禁止显示）
        "is_valid": 1, 是否有效 1,有效 2, 无效（用户自己删除）
        "object_id": "28", 评价样品ID
        "object_name": "333333333333",评价样品名称
        "object_type": "sample", 评价类型
        "professional_rank": 2,专业评分 [1,5]
        "punctual_rank": 5,守时评分 [1,5]
        "rating": 1 评价品级 0 好评 1， 中评 2 差评
    }
    
###修改评价
    /api/evaluate/edit POST Header [Authorization: <token>]
    参数
    communication_rank 沟通评分 [1,5]
    content 评价内容
    file 图片列表(multipart 直接上传多个文件)
    order_no 评价订单号
    professional_rank 专业评分 [1,5]
    punctual_rank 守时评分 [1,5]
    rating 评价品级 0 好评 1， 中评 2 差评
    
    返回
    {
        "author_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg", 评价者头像
        "author_id": 4, 评价者
        "author_mobile": "18683591672", 评价者手机号
        "communication_rank": 2, 沟通评分 [1,5]
        "content": "drgdfg", 评价内容
        "create_time": "2015-02-10 11:47:59", 评价时间
        "id": 1,
         "images": [
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
        "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
        ],评价者 上传图片
        "is_block": 0, 是否屏蔽 0 不屏蔽 1 屏蔽（管理员禁止显示）
        "is_valid": 1, 是否有效 1,有效 2, 无效（用户自己删除）
        "object_id": "28", 评价样品ID
        "object_name": "333333333333",评价样品名称
        "object_type": "sample", 评价类型
        "professional_rank": 2,专业评分 [1,5]
        "punctual_rank": 5,守时评分 [1,5]
        "rating": 1 评价品级 0 好评 1， 中评 2 差评
    }
    
###样品评价列表
    /api/evaluates GET
    参数
    sample_id 样品ID
    rating 0 好评 1， 中评 2 差评  不传全部
    page  
    page_size
    
    返回评价列表   
     {
    "evaluates": [
       
        {
            "author_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
            "author_id": 4,
            "author_mobile": "18683591672",
            "communication_rank": 5,
            "content": "1423536316378362",
            "create_time": "2015-03-19 11:19:26",
            "id": 44,
            "images": [
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
            ],
            "is_block": 0,
            "is_valid": 1,
            "object_id": "28",
            "object_name": "333333333333",
            "object_type": "sample",
            "professional_rank": 5,
            "punctual_rank": 5,
            "rating": 0
        },
        {
            "author_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
            "author_id": 4,
            "author_mobile": "18683591672",
            "communication_rank": 5,
            "content": "1423536316378362",
            "create_time": "2015-03-19 11:18:26",
            "id": 43,
            "images": [
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
            ],
            "is_block": 0,
            "is_valid": 1,
            "object_id": "28",
            "object_name": "333333333333",
            "object_type": "sample",
            "professional_rank": 5,
            "punctual_rank": 5,
            "rating": 0
        },
        ...
    ],
    "total": 11
    "good": 7,
    "normal": 0,
    "bad": 4
    }
    
###手艺人样品评价列表
    /api/evaluates/artisan GET
    参数
    artisan_id 手艺人ID
    rating 0 好评 1， 中评 2 差评  不传全部
    page  
    page_size
    
    返回评价列表   
    "evaluates": [
       
        {
            "author_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
            "author_id": 4,
            "author_mobile": "18683591672",
            "communication_rank": 5,
            "content": "1423536316378362",
            "create_time": "2015-03-19 11:19:26",
            "id": 44,
            "images": [
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
            ],
            "is_block": 0,
            "is_valid": 1,
            "object_id": "28",
            "object_name": "333333333333",
            "object_type": "sample",
            "professional_rank": 5,
            "punctual_rank": 5,
            "rating": 0
        },
        {
            "author_avatar": "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
            "author_id": 4,
            "author_mobile": "18683591672",
            "communication_rank": 5,
            "content": "1423536316378362",
            "create_time": "2015-03-19 11:18:26",
            "id": 43,
            "images": [
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg",
                "/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg"
            ],
            "is_block": 0,
            "is_valid": 1,
            "object_id": "28",
            "object_name": "333333333333",
            "object_type": "sample",
            "professional_rank": 5,
            "punctual_rank": 5,
            "rating": 0
        },
        ...
    ],
    "total": 11
    "good": 7,
    "normal": 0,
    "bad": 4
    }
###banner 列表接口
    /api/banners GET
    参数 无
    返回 banner 对象列表
    [
    {
        banner 图片
        "cover": "/img/667b5b4a2addc4696602b498a73c0d04.jpg", 
        "detail": [
            {
                "description": "00活动内容描述00",
                "image": "/img/243f6827fe80944b6bb26e80e175c713.jpg",
                "serial_number": 0
            },
            {
                "description": "11活动内容描述11",
                "image": "/img/174509341416b35b7cf23cf41b04906c.jpg",
                "serial_number": 1
            }
        ],
        
        "id": 1,
        活动名称
        "name": "banner-1",
        排序字段
        "serial_number": 0,
        内部或外部跳转地址
        "url": "http://photo.cankaoxiaoxi.com/roll10/2015/0324/717027.shtml"
    },
    {
        "cover": "/img/667b5b4a2addc4696602b498a73c0d04.jpg",
        "detail": [
            {
                "description": "00活动内容描述00",
                "image": "/img/243f6827fe80944b6bb26e80e175c713.jpg",
                "serial_number": 0
            },
            {
                "description": "11活动内容描述11",
                "image": "/img/174509341416b35b7cf23cf41b04906c.jpg",
                "serial_number": 1
            }
        ],
        "id": 2,
        "name": "banner-2",
        "serial_number": 1,
        "url": "http://photo.cankaoxiaoxi.com/roll10/2015/0324/717027_2.shtml"
    }
    ]
##html内容

###banner 详情接口
    /api/banner/<banner ID> GET
###关于我们
    /api/about_us GET
###服务范围
    /api/service_areas GET
###用户协议
    /api/user_agreement GET