# creates the posts tree

import MySQLdb as mysql
import re

connection = mysql.connect('localhost', 'joneame', 'joneame', 'joneame')
cursor = connection.cursor(mysql.cursors.DictCursor)

cursor.execute('SELECT * FROM posts WHERE post_parent IS NULL ORDER BY post_id DESC')
processed = 0
for post in cursor.fetchall():
    try:
        parent = re.search(r'^@([a-zA-Z_0-9\.]+),([0-9]+)\s', post['post_content']).groups()[1]
        parent = int(parent)
        print 'Parent for %d is %d' % (post['post_id'], parent)
        cursor.execute('UPDATE posts SET post_parent = %s WHERE post_id = %s', (parent, post['post_id']))
        cursor.execute('UPDATE posts SET post_parent = %s WHERE post_parent = %s', (parent, post['post_id']))
    except AttributeError: # no parent
        print '%d has no parent' % (post['post_id'],)
        cursor.execute('UPDATE posts SET post_parent = %s WHERE post_id = %s', (0, post['post_id']))
        pass

    processed += 1
    if processed % 25 == 0:
        print '%d posts processed' % (processed,)

connection.commit()
connection.close()