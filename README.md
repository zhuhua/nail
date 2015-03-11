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
	返回 地址对象列表
	{
	    "id": ID,
	    "user_id": 用户ID,
	    "location": 位置,
	    "detail": 详细地址,
	    "create_time":
	}
		
###常用地址列表
	/api/user/addresses GET Header [Authorization: <token>]
		
###删除常用地址
	/api/user/address/<地址ID> POST Header [Authorization: <token>]
		
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
		
###删除收藏
	/api/user/favorite/delete POST Header [Authorization: <token>]
	参数 
		type 类型 1 美甲师 2 美甲作品
		object_id 美甲师或美甲作品id

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
	            "sale": 0 销量
	    },
	    "cert_pop": 明星美甲师,
	    "avg_price": 均价,
	    "id": 28000006
	}

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
		category_id 类别ID 可选 [ 1:美甲 2:美睫 3:手足护理 4:空气净化 默认1 ]
		order_by 排序字段 可选 默认 create_time  [ price 价格， counts_sale 销量 ]
		sort asc|desc 可选 默认 desc 范围 [asc 正序, desc 倒序]
		page 页码 可选 默认 1
		page_size 页大小 可选 默认 10
		artisan_id 可选 如传入则取得该美甲师的作品
		tag 可选 参数值[标签接口得到的name]
	返回 美甲作品对象列表

###获取作品详情
	/api/sample<作品ID>
	{
	    "status": 状态 0 正常 1删除 ,
	    "name": 名称,
	    "tags": 标签,
	    "price": 价格,
	    "brief": 作品简介,
	    "counts": {
	        "sale": 0 销量
	    },
	    "artisan_id": 美甲师Id,
	    "create_time": 创建时间,
	    "images": 图片,
	    "category_id": 类别id,
	    "id": 12,
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
    "cover": "{'url': u'/img/af7762b2aafc3e53077aa0a461b6c7cf.jpg', 'create_time': datetime.datetime(2015, 2, 9, 13, 33, 55), 'id': 86L, 'obj_id': u'e5d604c0ffbb39165fa3f59821907bc6'}",
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
    是否评价 0 未评价 1 已评价
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
    同 创建订单 接口
    
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
    /api/evaluate/add POST Header [Authorization: <token>]
    参数
    communication_rank 沟通评分 [1,5]
    content 评价内容
    image 图片列表(通过图片上传接口上传图片)
    object_id 评价样品ID
    professional_rank 专业评分 [1,5]
    punctual_rank 守时评分 [1,5]
    rating 评价品级 0 好评 1， 中评 2 差评
    order_no 评价来源订单号
    返回
    {
        "author_id": 4, 评价者
        "communication_rank": 2, 沟通评分 [1,5]
        "content": "drgdfg", 评价内容
        "create_time": "2015-02-10 11:47:59", 评价时间
        "id": 1,
        "is_block": 0, 是否屏蔽 0 不屏蔽 1 屏蔽（管理员禁止显示）
        "is_valid": 1, 是否有效 1,有效 2, 无效（用户自己删除）
        "object_id": "28", 评价样品ID
        "object_type": "sample", 评价类型
        "professional_rank": 2,专业评分 [1,5]
        "punctual_rank": 5,守时评分 [1,5]
        "rating": 1 评价品级 0 好评 1， 中评 2 差评
    }
    
###样品评价列表
    /api/evaluates GET
    参数
    sample_id 样品ID
    page
    page_size
    {
    "evaluates": [
       
        {
            "author_id": 4,
            "communication_rank": 4,
            "content": "drgdfg",
            "create_time": "2015-02-10 17:12:16",
            "id": 10,
            "is_block": 0,
            "is_valid": 1,
            "object_id": "28",
            "object_type": "sample",
            "professional_rank": 0,
            "punctual_rank": 1,
            "rating": 1
        },
        {
            "author_id": 4,
            "communication_rank": 4,
            "content": "drgdfg",
            "create_time": "2015-02-10 17:15:00",
            "id": 11,
            "is_block": 0,
            "is_valid": 1,
            "object_id": "28",
            "object_type": "sample",
            "professional_rank": 2,
            "punctual_rank": 5,
            "rating": 0
        }
    ],
    "total": 11
    }
