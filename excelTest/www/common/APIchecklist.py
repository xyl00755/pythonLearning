#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import logging
import configparser
from bs4 import BeautifulSoup


class APIchecklist():
    APIchecklist_html = """
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>潘多拉 ShowDoc</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <!-- <link href="/Public/bootstrap/css/bootstrap.min.css" rel="stylesheet"> -->
        <link href="http://apps.bdimg.com/libs/bootstrap/2.3.2/css/bootstrap.min.css" rel="stylesheet">
        <link href="/Public/css/showdoc.css?v=1.1" rel="stylesheet">
          <script type="text/javascript">
          var DocConfig = {
              host: window.location.origin,
              app: "/",
              pubile:"/Public",
          }

          DocConfig.hostUrl = DocConfig.host + "/" + DocConfig.app;
          </script>

          <!-- 百度统计代码 -->
    <!--      <script>
          var _hmt = _hmt || [];
          (function() {
            var hm = document.createElement("script");
            hm.src = "//hm.baidu.com/hm.js?7c83eafa274048290cb2f71f911e8e0f";
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
          })();
          </script>-->

          <script src="/Public/js/lang.zh-cn.js?v=21"></script>
      </head>
      <body>
    <link rel="stylesheet" href="/Public/css/item/show.css?1.1d.1thddde" />


    <div class="doc-head row" >
      <div class="left "><h2>潘多拉</h2></div>
      <div class="right">
        <ul class="inline pull-right">

          <li>
              <div class="btn-group ">
                <a class="btn btn-primary dropdown-toggle" data-toggle="dropdown" href="#">
                  项目              <span class="caret"></span>
                </a>
              <ul class="dropdown-menu">
              <!-- dropdown menu links -->
                <li><a href="#" id="share">分享</a></li>
                 <li><a href="/home/item/word/item_id/6836">导出</a></li>


                <li><a href="/home/item/index">更多项目</a></li>
              </ul>
          </li>

        </ul>
        </div>
      </div>
    </div>

    <div class="doc-body row">
      <!-- 左侧栏菜单 -->
        <div class="doc-left span3 bs-docs-sidebar pull-left">
            <form class="form-search text-center" action="/home/item/show/item_id/6836" method="post">
              <div class="input-append search-input-append">
                <i class="icon-blank"></i>
                <input type="text" name="keyword" class="search-query search-query-input" value="">
                <input type="hidden" name="item_id" value="6836">
                <button type="submit" class="btn"><i class="icon-search"></i></button>
              </div>
            </form>

          <ul class="nav nav-list bs-docs-sidenav">

            <!-- 一级目录的页面在前面 -->

            <li><a href="#"><i class="icon-chevron-right"></i>App 接口</a>
                <ul class="child-ul nav-list hide">
                  <!-- 二级目录的页面们 -->
                                <!-- 二级目录的子目录们（三级目录） -->
                    <li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>经销商优惠券/红包</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/48359" data-page-id="48359" >首页：获取品类图标</a></li><li><a href="/home/page/index/page_id/48889" data-page-id="48889" >我的丹露：获取丹露红包、经销商红包、经销商优惠券数量</a></li><li><a href="/home/page/index/page_id/48881" data-page-id="48881" >获取经销商红包最高支付比参数</a></li><li><a href="/home/page/index/page_id/48872" data-page-id="48872" >结算页展示某个经销商所用红包以供选择使用</a></li><li><a href="/home/page/index/page_id/48998" data-page-id="48998" >判断已领取的优惠券是否可用</a></li><li><a href="/home/page/index/page_id/48848" data-page-id="48848" >结算页可用经销商红包数量展示</a></li><li><a href="/home/page/index/page_id/48830" data-page-id="48830" >结算页获取商品优惠券</a></li><li><a href="/home/page/index/page_id/48818" data-page-id="48818" >已领取的经销商优惠券/红包数量</a></li><li><a href="/home/page/index/page_id/48811" data-page-id="48811" >已领取的经销商优惠券/红包</a></li><li><a href="/home/page/index/page_id/48983" data-page-id="48983" >领券中心</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>拆单支付</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/49856" data-page-id="49856" >查看已拆分订单</a></li><li><a href="/home/page/index/page_id/49854" data-page-id="49854" >拆分订单</a></li><li><a href="/home/page/index/page_id/49834" data-page-id="49834" >获取待拆分订单信息</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>联动支付</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                                              </ul>
                      </li>
                </ul>
              </li><li><a href="#"><i class="icon-chevron-right"></i>经销商红包\优惠券</a>
                <ul class="child-ul nav-list hide">
                  <!-- 二级目录的页面们 -->
                                <!-- 二级目录的子目录们（三级目录） -->
                    <li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>结算页改造</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47692" data-page-id="47692" >收货人地址列表查询</a></li><li><a href="/home/page/index/page_id/47739" data-page-id="47739" >收货人地址新增</a></li><li><a href="/home/page/index/page_id/47755" data-page-id="47755" >查询省份下拉列表</a></li><li><a href="/home/page/index/page_id/47761" data-page-id="47761" >查询城市下拉列表</a></li><li><a href="/home/page/index/page_id/47764" data-page-id="47764" >查询县区下拉列表</a></li><li><a href="/home/page/index/page_id/47776" data-page-id="47776" >查询指定地址的编辑是否在审批流程中</a></li><li><a href="/home/page/index/page_id/47787" data-page-id="47787" >收货人地址修改</a></li><li><a href="/home/page/index/page_id/47789" data-page-id="47789" >收货人地址删除</a></li><li><a href="/home/page/index/page_id/47793" data-page-id="47793" >收货人地址设置默认地址</a></li><li><a href="/home/page/index/page_id/47838" data-page-id="47838" >普通发票信息列表查询</a></li><li><a href="/home/page/index/page_id/48057" data-page-id="48057" >普通发票信息设置默认</a></li><li><a href="/home/page/index/page_id/48031" data-page-id="48031" >普通发票信息删除</a></li><li><a href="/home/page/index/page_id/48021" data-page-id="48021" >普通发票信息修改</a></li><li><a href="/home/page/index/page_id/47942" data-page-id="47942" >普通发票信息新增</a></li><li><a href="/home/page/index/page_id/48801" data-page-id="48801" >丹露红包查询接口</a></li><li><a href="/home/page/index/page_id/49058" data-page-id="49058" >是否需要大额红包验证</a></li><li><a href="/home/page/index/page_id/49068" data-page-id="49068" >获取用户激活手机及大额红包验证限额</a></li><li><a href="/home/page/index/page_id/49072" data-page-id="49072" >大额红包验证框获取图片验证码</a></li><li><a href="/home/page/index/page_id/49081" data-page-id="49081" >大额红包验证框图片验证码验证</a></li><li><a href="/home/page/index/page_id/49082" data-page-id="49082" >大额红包验证框发送短信</a></li><li><a href="/home/page/index/page_id/49084" data-page-id="49084" >大额红包验证框即时验证动态验证码</a></li><li><a href="/home/page/index/page_id/49085" data-page-id="49085" >大额红包验证框表单提交</a></li><li><a href="/home/page/index/page_id/49695" data-page-id="49695" >结算页下单接口</a></li><li><a href="/home/page/index/page_id/49803" data-page-id="49803" >下单后请求支付中转页</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>经销商红包\优惠劵抵扣明细</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47717" data-page-id="47717" >经销商红包抵扣明细查询接口</a></li><li><a href="/home/page/index/page_id/47723" data-page-id="47723" >经销商优惠劵抵扣明细查询接口</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>经销商支付比</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47930" data-page-id="47930" >获取最高支付比</a></li><li><a href="/home/page/index/page_id/47943" data-page-id="47943" >设置最高支付比</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>优惠券、红包</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/48134" data-page-id="48134" >查询地域</a></li><li><a href="/home/page/index/page_id/52317" data-page-id="52317" >条件查询推送</a></li><li><a href="/home/page/index/page_id/48309" data-page-id="48309" >条件查询经销商的优惠券、红包导出</a></li><li><a href="/home/page/index/page_id/48299" data-page-id="48299" >编辑优惠券、红包</a></li><li><a href="/home/page/index/page_id/48273" data-page-id="48273" >获取商品(由于前端界面不确定暂时留着)</a></li><li><a href="/home/page/index/page_id/48178" data-page-id="48178" >查询终端店类型</a></li><li><a href="/home/page/index/page_id/48150" data-page-id="48150" >根据类目编码查询品牌</a></li><li><a href="/home/page/index/page_id/48143" data-page-id="48143" >查询分类</a></li><li><a href="/home/page/index/page_id/48064" data-page-id="48064" >创建优惠券、红包、推送</a></li><li><a href="/home/page/index/page_id/47745" data-page-id="47745" >条件查询经销商的优惠券、红包</a></li><li><a href="/home/page/index/page_id/47626" data-page-id="47626" >优惠券、红包名称判重</a></li><li><a href="/home/page/index/page_id/52557" data-page-id="52557" >删除优惠券\红包</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>抢券/链接分享</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47622" data-page-id="47622" >抢券</a></li><li><a href="/home/page/index/page_id/47662" data-page-id="47662" >链接分享</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>红包/优惠券查询</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47878" data-page-id="47878" >终端店已领取红包/优惠券查询</a></li><li><a href="/home/page/index/page_id/49028" data-page-id="49028" >终端店多个经销商红包或优惠券</a></li><li><a href="/home/page/index/page_id/48214" data-page-id="48214" >终端店已领取红包/优惠券个数</a></li><li><a href="/home/page/index/page_id/47887" data-page-id="47887" >终端店可以领取红包/优惠券个数</a></li><li><a href="/home/page/index/page_id/47886" data-page-id="47886" >终端店可领 优惠券/红包展示</a></li><li><a href="/home/page/index/page_id/47885" data-page-id="47885" >买家名称或店铺名称联想</a></li><li><a href="/home/page/index/page_id/47884" data-page-id="47884" >商品名称联想</a></li><li><a href="/home/page/index/page_id/47882" data-page-id="47882" >商品详情优惠券或红包查询</a></li><li><a href="/home/page/index/page_id/47880" data-page-id="47880" >商品图片下显示是否有优惠券图标</a></li><li><a href="/home/page/index/page_id/47879" data-page-id="47879" >领券中心红包/经销商查询</a></li><li><a href="/home/page/index/page_id/49958" data-page-id="49958" >批量查询商品是否有可使用优惠券</a></li>                    </ul>
                      </li>
                </ul>
              </li><li><a href="#"><i class="icon-chevron-right"></i>拆单支付</a>
                <ul class="child-ul nav-list hide">
                  <!-- 二级目录的页面们 -->
                                <!-- 二级目录的子目录们（三级目录） -->
                    <li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>拆单开关</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47902" data-page-id="47902" >设置拆单开关</a></li>                    </ul>
                      </li><li class="third-child-catalog"><a href="#"><i class="icon-chevron-right"></i>订单拆分</a>
                        <ul class="child-ul nav-list hide">
                          <!-- 二级目录的页面们 -->
                          <li><a href="/home/page/index/page_id/47904" data-page-id="47904" >获取待拆分订单信息</a></li><li><a href="/home/page/index/page_id/47908" data-page-id="47908" >保存订单拆分信息</a></li><li><a href="/home/page/index/page_id/47920" data-page-id="47920" >获取拆分支付单信息 </a></li>                    </ul>
                      </li>
                </ul>
              </li>
          </ul>
        """

    def getAPIFirst(self):
         soup = BeautifulSoup(self.APIchecklist_html, "html.parser")
         #lt = soup.find_all("i",class_="icon-chevron-right")
         lt = soup.find("ul",class_="nav nav-list bs-docs-sidenav")
         apiList1=lt.find("li")
         print apiList1.find("a")

         apiFirstList=[]
         #for i in range(0,len(lt)):
             #apiFirstList.append(lt[i].find_parent("a"))
             #print lt[i].find_parent("a")

         return lt







if __name__ == '__main__':
	a=APIchecklist()
	a.getAPIFirst()