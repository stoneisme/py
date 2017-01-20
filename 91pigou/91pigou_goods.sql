CREATE TABLE `91pigou_goods` (
  `goods_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '商品编号',
  `cat_id` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '商品分类',
  `goods_name` varchar(120) NOT NULL DEFAULT '' COMMENT '商品名称',
  `goods_price` decimal(10,2) DEFAULT '0.00' COMMENT '商品单价',
  `goods_unit` varchar(10) DEFAULT '' COMMENT '单价单位',
  `goods_ratio` smallint(5) DEFAULT '0' COMMENT '商品数量',
  `goods_desc` text NOT NULL COMMENT '商品描述',
  `goods_img` varchar(255) NOT NULL DEFAULT '' COMMENT '商品图片',
  `add_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `last_update` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最后更新时间',
  PRIMARY KEY (`goods_id`),
  KEY `cat_id` (`cat_id`),
  KEY `last_update` (`last_update`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8


CREATE TABLE `91pigou_goods_skus` (
  `sku_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '编号',
  `goods_id` mediumint(8) unsigned NOT NULL DEFAULT '0' COMMENT '商品编号',
  `sku_name` varchar(120) NOT NULL DEFAULT '' COMMENT '商品名称',
  `sku_sale_price` decimal(10,2) DEFAULT '0.00' COMMENT '商品单价',
  `sku_sale_unit` varchar(10) DEFAULT '' COMMENT '单价单位',
  `sku_ratio` smallint(5) DEFAULT '0' COMMENT '商品数量',
  `sku_desc` text NOT NULL COMMENT '商品描述',
  `sku_img` varchar(255) NOT NULL DEFAULT '' COMMENT '商品图片',
  `sku_tags` varchar(60) DEFAULT '' COMMENT '商品标签',
  `sku_integral` int(11) DEFAULT '0',
  `sku_give_integral` int(11) DEFAULT '0',
  `add_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '添加时间',
  `last_update` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最后更新时间',
  PRIMARY KEY (`sku_id`),
  KEY `goods_id` (`goods_id`),
  KEY `last_update` (`last_update`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
