nail
====

<h1>Nail make up mobile app</h1>

接口地址 http://115.28.134.4/

##用户部分

###注册接口
/api/user/register  
参数 
mobile 手机
password 密码
checkcode 验证码

###登陆
/api/user/login
参数 
mobile 手机
password 密码
返回登陆token

###获取个人信息
/api/user/profile
Http Header Token: <token>

##美甲师部分

###获取美甲师列表
/api/artisans
参数
order_by 排序字段 可选
sort asc|desc 可选 默认 asc
page 页码 可选 默认 1
dis_size 页大小 可选 默认 10
name 可选 如传入是以美甲师名字搜索

###获取美甲师信息
/api/artisan
参数 id

##美甲作品部分

###获取作品列表
/api/samples
参数
order_by 排序字段 可选
sort asc|desc 可选 默认 asc
page 页码 可选 默认 1
dis_size 页大小 可选 默认 10
artisan_id 可选 如传入则取得该美甲师的作品

###获取作品详情
/api/sample
参数 id

```python
dict(a=1, b=2)
```
