# 智能财务OpenAPI接口

## 工程介绍
### 接口介绍
- FAST接口集成了**识别+结构化+分类**的功能。
- 不过结构化那一步，目前存在比较明显的适配问题，需要进行更大规模的样本测试，因此暂时参考意义不大（7.28）。

### 特性说明
- 支持华为、百度、有道、旷视等多个厂商
- 支持对识别图片的结果进行结构化输出并自动归类
- 全面支持并使用REST
- 最大的优势：相较于各个厂商复杂的鉴权设置，本项目提供了统一与开放的接口
- 最大的劣势：由于使用的是其他厂商的ocr接口，因此项目成果受限于厂商的技术能力
- [ ] 稳健智能的分类
- [ ] 样本测试与汇总分析

### 返回说明
```text
- ocr_result        # OCR识别的结果
    - words         # 从第三方API返回结果中解析出的文字数组
    - raw           # 如果请求参数带有verbose，则会包含该字段，指原第三方API返回结果
- classified_algos  # 分别使用微信、支付宝的详情、流水解析算法得到的结果
- classified_result # 对算法结果进行比较，得出的最终分类结果
- called_surplus    # 该接口的当日使用剩余（零点重置，部分除外）
```


## 使用方法
### 使用方法一（小白推荐）

访问： [智能财务OpenAPI接口](https://nanchuan.site:666/docs)

- 在 `fast` 下，选择一个接口（不推荐旷视）

- 点击 `Try It Out` 按钮

- 选择一张图片上传

- 点击 `Execute`

- 查看或下载 `response` 里的内容。

### 【推荐】使用方法二（post脚本测试）

- 要求：会requests就可以

- 下载： [post脚本](https://gitee.com/MarkShawn2020/shenyao-OCR/blob/master/scripts/post_demo.py)

### 使用方法三（源代码开发）

- 要求：熟悉git、python、fastapi、命令行

- 访问：[shenyao-OCR](https://gitee.com/MarkShawn2020/shenyao-OCR)

## 开发者使用说明
### 初次安装
```bash
git clone https://gitee.com/MarkShawn2020/shenyao-OCR
cd shenyao-OCR
pip install -r requirements.txt --ignore-installed --user
```

### 更新安装
```bash
git add -A
git commit -m "backup"
git pull
```
最后如果提示有一些文件冲突，自己在IDE里查阅，该删的删该调的调就好

### 开发者文档参考
- 华为: https://support.huaweicloud.com/api-ocr/ocr_03_0047.html
- 百度: https://ai.baidu.com/ai-doc/OCR/zk3h7xz52
- 旷视: https://console.faceplusplus.com.cn/documents/7776484


## 更新说明
### V0.8.1 2020-09-01 21:34:24
- 【<font color=red>BIG CHANGE</font>】对于有限制次数的接口，超出请求次数之后直接返回报错

### V0.8.0 2020-07-30 05:02:50
- 修复数据库被黑客扫描攻击的漏洞，更换了端口并加入了权限认证，现在应该没有问题了

### V0.7.4 2020-07-29 13:29:16
- 返回字段中加入了使用额度剩余
- 使用装饰器完成了对额度字段的位置纠正

### V0.7.3 2020-07-29 11:24:38
- 使用工厂函数修复了由于循环导致lazy match的bug，目前各大接口均正常运行
- 修改了配置结构，使之对于每一个api具有更好的扩展能力
- 加入了recommend api列表

### V0.7.2 2020-07-28 23:27:45
- 为了对接接口原名，重新整理了程序结构，使用工厂函数，程序的配置扩展能力大幅增强
- 目前所有的配置均在config/api.yaml内，通过api/api_fast函数进行统一读取，调用api/ocrs内的各大厂商api
- 基于此能力，扩充了百度通用识别与网络图片识别总共6个API，其他API保持不变

### V0.7.1 2020-07-28 19:33:05
- 修复了华为接口的bug
- 由于目前分类算法不够稳健，因此对所有接口加入了classify参数，默认为否，即不输出分类结果

### V0.7.0 2020-07-28 13:12:19
- 废弃了原命令行框架，全部fast接口封装
- 支持华为（2个）、百度（2个）、有道（1个）、旷视（1个）共6个接口
- 增加了一个post的脚本demo

### V0.6.1 2020-07-27 14:44:57
- 加入了 verbose参数，默认为否，改参数将包含第三方API识别的原生结果
- 删除了OCR接口对外的开放，减少对大家使用api的干扰
- 支持了多张图片的上传
- 修复了微信浮窗可能会遮住右上角“统计”关键字的问题

### V0.6.0
- 基于fastapi部署了系统的api系统，实现了restful化，避免对于python不熟悉的朋友浪费大量时间在sdk上

### V0.5.0
- 已经集成了识别+分类，在core.fast文件内

### V0.4.0
- 使用click进行进一步封装，直接使用`ocr`命令即可完成识别任务
- 支持识别后自动保存到本地`output.json`文件
- 支持程序中的出错逻辑判断

### V0.3.0
- 抛弃了华为的SDK，直接使用requests进行封装，API的一致性增强
- 账户信息独立存放至config/ACCOUNT.yaml，耦合度降低
- 使用flask团队出品的click对`main.py`进行了封装，易用性增强
