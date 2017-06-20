---
title: '"Impossible" foreign key violations with MySQL'
published: 2013-01-23T09:20:00-0400
---

Ever had the experience with MySQL where it complains that a foreign key
constraint has been violated and you know that's not possible?

For example:

<img alt="wat?" src="/static/posts/2013/1/23/error.png" />

But...nonsense!  How could this be??  After all, look at the foreign key
definitions in the MySQL console!

    mysql> show create table products_product\G
    *************************** 1. row ***************************
           Table: products_product
    Create Table: CREATE TABLE `products_product` (
      ...
      PRIMARY KEY (`id`),
      KEY `products_product_56ae2a2a` (`slug`),
      KEY `products_product_39b65067` (`comparisongroup_id`),
      KEY `products_product_312b966` (`connector_type_id`)
    ) ENGINE=MyISAM AUTO_INCREMENT=430 DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)

    mysql> show create table products_accessory\G
    *************************** 1. row ***************************
           Table: products_accessory
    Create Table: CREATE TABLE `products_accessory` (
      ...
      PRIMARY KEY (`id`),
      KEY `products_accessory_a190c07e` (`accessory_of_id`),
      KEY `products_accessory_bb420c12` (`product_id`),
      CONSTRAINT `product_id_refs_id_17d77a3c3b53148e` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
      CONSTRAINT `accessory_of_id_refs_id_17d77a3c3b53148e` FOREIGN KEY (`accessory_of_id`) REFERENCES `products_product` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)

    mysql>

What's wrong with that?  Nothing, right?  Not so fast.  Take a look at the
engine type for each table:

    mysql> show create table products_product\G
    *************************** 1. row ***************************
           Table: products_product
    Create Table: CREATE TABLE `products_product` (
      ...
    ) ENGINE=MyISAM AUTO_INCREMENT=430 DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)

    mysql> show create table products_accessory\G
    *************************** 1. row ***************************
           Table: products_accessory
    Create Table: CREATE TABLE `products_accessory` (
      ...
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)

Foreign keys constraints cannot be made between MyISAM and InnoDB tables.  It's
an easy mistake to make.  This is especially true if you regularly download
database dumps from production servers to bootstrap local dev setups.  You may
not have realized that the production server was using an older version of
MySQL and that your dev setup is using a newer version.  Before MySQL version
5.5.5, the default engine was MyISAM.  After and including version 5.5.5, it
was switched to InnoDB.

One easy fix for this is to add the following to your `/etc/mysql/my.cnf` file:

    default-storage-engine = MyISAM

or this:

    default-storage-engine = InnoDB

Whatever you need to get the configurations lined-up.

This happened to me a couple of times recently.  It's another good argument for
keeping your local dev setup as close to the production setup as possible.
