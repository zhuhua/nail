Nail make up mobile app
====

##接口地址 http://115.28.134.4/

##用户部分

###注册接口
	/api/user/register POST
	参数
		mobile 手机
		password 密码
		checkcode 验证码

###登陆
	/api/user/login POST
	参数 
		mobile 手机
		password 密码
		返回登陆token

###获取个人信息
	/api/user/profile GET Header [Authorization: <token>]
	
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
