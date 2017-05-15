# -*- coding: utf-8 -*-
from openerp import http
import simplejson
import json
import urllib
import urllib2
import httplib
from openerp.modules.registry import RegistryManager


class accessController(http.Controller):

	@http.route('/getToken/getToken/', auth='public')
	def getCode(self, **kw):
		result = True
		kw = simplejson.loads(simplejson.dumps(kw).replace('+',''))
		if set(["code", "state"]).issubset(kw):
			code = kw.get("code")
			state = kw.get("state")
			print(code)
			print(state)
			state = json.loads(state)
			print(state.get("id"))
			response = self.getAccessToken(code, state)
		else:
%s		if result:
			return "授权成功！"
		else:
			return "授权失败请重试！"

	def getAccessToken(self,code,state):
		result = True
		#参数
		param = {
			"grant_type": "authorization_code",
			"client_id": state.get("appkey"),
			"redirect_uri": state.get("redirect_uri"),
			"code": code,
			"client_secret": state.get("appsecret"),
			"state": state.get("id")
			}
		print(param)
		data = urllib.urlencode(param)
		# 请求头部
		# 建立连接发送请求
		# JD
		# url = "https://oauth.jd.com/oauth/token?"
		# YZ
		url = "https://open.koudaitong.com/oauth/token?"
		req = urllib2.Request(url, data)
		#获得response
		response = urllib2.urlopen(req)
		#response.read() 返回一个json格式字符串，在将其转化为dict
		tokenResult = json.loads(response.read())
		print(tokenResult)
		#根据id更新
		registry = RegistryManager.get("odoo9")
		with registry.cursor() as cr:
			try:
				cr.execute('update channel_base set "accessToken" = %s, "haveRight" = %s where id = %s',(tokenResult.get("access_token"),'t',state.get("id")))
				cr.commit()
			except Exception, e:
				result = False
				raise e
		return result

