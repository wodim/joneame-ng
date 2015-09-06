# creates the posts tree

import MySQLdb as mysql
import re

connection = mysql.connect('localhost', 'joneame', 'joneame', 'joneame')
cursor = connection.cursor(mysql.cursors.DictCursor)

cursor.execute('SELECT * FROM posts order by post_id desc')
processed = 0
for post in cursor.fetchall():
    try:
        parent = re.search(r'^@([a-zA-Z_0-9\.]+),([0-9]+)\s', post['post_content']).groups()[1]
        print 'Parent for %d is %d' % (post['post_id'], int(parent))
        cursor.execute('UPDATE posts SET post_parent = %s WHERE post_id = %s', (int(parent), post['post_id']))
        cursor.execute('UPDATE posts SET post_parent = %s WHERE post_parent = %s', (int(parent), post['post_id']))
    except AttributeError: # no parent
        print '%d has no parent' % (post['post_id'],)
        pass

    processed += 1
    if processed % 25 == 0:
        print '%d posts processed' % (processed,)

connection.commit()
connection.close()