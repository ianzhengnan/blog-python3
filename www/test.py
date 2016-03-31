
import orm as orm
import sys

from models import User, Blog, Comment

import asyncio

def testUser(loop):
    yield from orm.create_pool(loop,user='www-data', password='www-data', db='awesome')

    u = User(name='Ian', email='test1@qq.com', passwd='1234567', image='about:blank')

    yield from u.save()

# test
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testUser(loop))
    loop.close()
    if loop.is_closed():
        sys.exit(0)