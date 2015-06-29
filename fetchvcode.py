import web
from classes import vcode
import StringIO


class fetchvcode():
    def __init__(self):
        '''
        Constructor
        '''
        pass;
    
    def GET(self):
        vcodeimg = vcode.create_validate_code()
        print vcodeimg[1]
        buf = StringIO.StringIO()
        # vcodeimg[0].save(buf)
        img = vcodeimg[0]
        img.save(buf, format="JPEG")
        web.ctx.session.vcode = vcodeimg[1]
        print "vcode in session : %s" % web.ctx.session.vcode
        data = buf.getvalue()
        buf.close()
        return data