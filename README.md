# scrapy-woaiwojia_2th

#### 抓取内容

>我爱我家·杭州 https://hz.5i5j.com/ershoufang/

#### 网页分析

* 静态网页常规请求，每页30条数据，1000页以上
* 防爬检查Cookie，Referer, ip频率
* spider分为两个，一个一次性爬取所有页面，一个用于更新上次爬取节点后的房源

#### 抓取结果展示

![](https://github.com/Bigbenen/scrapy-woaiwojia_2th/blob/master/a.png)

#### 分析结果小试牛刀

>二手房源信息还是比较有价值的，在此尝试用matplotlib对`房源数量`和`均价`做了简单的图表分析，有没有发现二者此消彼长的对应关系呢，哈哈。

二手房挂牌数量/均价趋势图
![](https://github.com/Bigbenen/scrapy-woaiwojia_2th/blob/master/20190215.jpg)

