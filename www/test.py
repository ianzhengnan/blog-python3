#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import orm as orm
import sys

from models import User, Blog, Comment

import asyncio

def testUser(loop):
    yield from orm.create_pool(loop,user='www-data', password='www-data', db='awesome')

    u = User(name='Doris.Yuan', email='doris.yuan@qq.com', passwd='908765', image='about:blank')

    yield from u.save()

def testFetchAll(loop):
    yield from orm.create_pool(loop,user='www-data', password='www-data', db='awesome')

    users = yield from User.findAll()
    print(users)

def testFetch(loop):
    yield from orm.create_pool(loop,user='www-data', password='www-data', db='awesome')

    user = yield from User.find('0014594017812288fb6d21306ba4f06a182e3f96e906e27000')
    print(user)

# test
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testUser(loop))
    loop.close()
    if loop.is_closed():
        sys.exit(0)