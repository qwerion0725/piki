import os
import shutil
import time
import tornado.web

from setting import settings

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie('wiki_moseeker_com_user')
        user = None
        if user_id is not None:
            cur = self.db.cursor()
            cur.execute("select id,realname,email from piki_user where id=:id",{'id':int(user_id)})
            user = cur.fetchone()
            cur.close()
        return  user

    def get(self):
        if self.current_user:
            self.redirect(self.reverse_url('/'))
        else:
            self.render('login.html')
    def write_file(self,filename,content):
        path = settings['doc_path'] + filename 
        if os.path.exists(path):
            shutil.move(path,path+time.strftime("%Y%m%d%H%M"))
        doc_file = open(path,'w')
        doc_file.write(content)
        doc_file.close()

    def get(self):
        getattr(self,'get_')() 

    def post(self):
        getattr(self,'post_')() 

