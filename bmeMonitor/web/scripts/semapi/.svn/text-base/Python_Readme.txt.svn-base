====================当前版本信息====================
当前版本：Beta1.1.18

发布日期：2014-04-03

====================================================

====================修改历史====================


================================================

************************************************中文*****************************************************
发布介绍:

此客户端库,目前支持百度商业推广API V3版本2014年4月3号前发布的功能。 
使用示例请参考*Example.py。本客户端库旨在提供调用封装以及代理类生成，并不提供客户端业务逻辑。 
使用过程中如果遇到任何问题，请联系apihelp@baidu.com并在标题注明《Baidu API Client V3使用过程问题求助》


注意事项:

1. 相关工具安装
Python SDK有json和WebService两种使用方式，推荐使用json方式。
使用json方式调用Python SDK需要安装requests插件，下载地址：http://www.python-requests.org/en/latest/user/install/#install 
 
使用WebService方式使用Python SDK需要安装WebService解析工具——SUDS 
下载地址：https://fedorahosted.org/suds/
安装步骤：将SUDS安装到PYTHONPATH 



2. 如何使用Python SDK json方式

如何初始化Service？ 
使用者获取具体的service对象方法是：


       service = sms_v3_RankService()
sms_v3_RankService的三段分别代表产品线缩写、版本号、服务名 
此时会从baidu-api.properties里加载默认用户信息，包括url、username、password、token、target、accessToken等。
若想重新设置这些参数，可以执行以下方法：


       service.setUsername("xxx")
       service.setPassword("xxx")
       service.setToken("xxx")
如何调用API进行请求 ? 
使用获取的service对象调用其指定方法，如

       request = {"keyWords":["鲜花","团购"],"device":0,"region":1000,"page":0,"display":0}
       res = service.getPreview(request)
       printJsonResponse(res)
       print PreviewUtil.decode(res["body"]["previewInfos"][0]["data"])
res中保存了这次调用返回结果，可以调用printJsonResponse方法打印结果，用户也可以类似上例自定义方法获取结果。

3. 如何使用Python SDK WebService方式
如何初始化Service？ 
使用者获取具体的cliente对象方法是：


       apiSDKSoapClient = ApiSDKSoapClient('sms','v3','AccountService')
ApiSDKSoapClient的三个参数分别为产品线缩写、版本号、服务名


       client = apiSDKSoapClient.newSoapClient()
此时会从baidu-api.properties里加载默认用户信息，包括url、username、password、token、target、accessToken等。
若想重新设置这些参数，可以在newSoapClient()之前执行以下方法：


       apiSDKSoapClient.setUsername("xxx")
       apiSDKSoapClient.setPassword("xxx")
       apiSDKSoapClient.setToken("xxx")
如何调用API进行请求 ? 
使用获取的client对象调用其指定方法，如

       client.service.getAccountInfo()
该方法为Request请求不带参数的方法，若Request请求中带参数，则应通过suds的工厂创建请求对象，如

       request = client.factory.create('updateAccountInfoRequest')
       accountInfoType = client.factory.create('updateAccountInfoRequest.accountInfoType')
       excludeIp  = ['192.168.2.3','10.10.10.16']
       accountInfoType.excludeIp  = excludeIp
       request.accountInfoType=accountInfoType
       client.service.updateAccountInfo(request.accountInfoType)
如何取得调用结果 ? 


       res = client.last_received()
       printSoapResponse(res)
res中保存了这次调用返回结果，可以调用printSoapResponse方法打印结果，用户也可以自定义方法获取结果。

4. 本客户端库的运行环境 ?

       python 2.7+
5. 服务器证书 ?

如果想通过程序下载报告，可以导入证书VeriSign_G5.crt到开发环境

------------------------------------------------------------------------------------------------------------------
Copyright 2014 Baidu.com Inc.
Baidu API Team