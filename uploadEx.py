class uploadEx():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        if constants.SAE_ENV:
            pass
        else:
            work_dir = os.getcwd()
            upload_dir = work_dir.replace('\\','/') + "/static/upload/"
            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)
            self.upload_dir = upload_dir

        self.posted = web.input(_unicode=False)
        # print self.posted
    
    def GET(self):
        try:
            action = self.posted['action']
        except:
            return ""
        if action == "config":
            return self.config()
        
        if action == "uploadimage":
            return self.uploadFile()
                
    def POST(self):
        try:
            action = self.posted['action']
        except:
            return ""
        print "[debug]:action in upload,POST:", action
        if action == "uploadimage":
            return self.uploadFile()

        elif action == "uploadify":
            return self.uploadify()

            
            
    def config(self):
        rawdata = open("pages/config.json").read()
        repl = re.compile("/\*.*?\*/")
        data = re.sub(repl,"",rawdata)
        
#         ret = {
#             "imageUrl": "http://localhost/uploadEx?action=uploadimage",
#             "imagePath": "/static/upload/",
#             "imageFieldName": "upload",
#             "imageMaxSize": 2048,
#             "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
#         }
        
#         ret = json.dumps(ret)
        return data
        
    def uploadify(self):
        filename = self.posted['Filename']
        originalFileName = filename
        try:
            if filename.split(".")[-1].lower() not in ["jpg","bmp","png","gif","tif"]:
                ret = {"state": "FAIL", "reason": "仅接受jpg格式图片"}
                return json.dumps(ret)

        except Exception,e:
            ret = {"state": "FAIL", "reason": e}
            return json.dumps(ret)


        fileType = filename.split(".")[-1]
        filename = "%d_%s.%s"%(88,str(time()),fileType)
        fakefile = StringIO.StringIO(self.posted['Filedata'])
        fp = open(self.upload_dir+filename,"wb")
        fp.write(self.posted['Filedata'])
        image = Image.open(fakefile)
        width, height = image.size
        if width > height:
            newWidth = 360
            newHeight = 360*height/width
        else:
            newHeight = 480
            newWidth = 480*width/height
        image.thumbnail((newWidth,newHeight),Image.ANTIALIAS)
        thumb_filename = filename.replace(fileType,"")[:-1]+"_thumb."+fileType
        image.save(self.upload_dir+thumb_filename)
        prefix = "/static/upload/"
        oriImgUrl = prefix+filename
        thumbUrl = prefix+thumb_filename
        ret = {
            "state": "SUCCESS",
            "url": oriImgUrl,
            "thumb": thumbUrl,
            "original": originalFileName,
            "type": fileType,
        }
        ret = json.dumps(ret)
        print "[debug]:return in uploaditty,",ret
        return ret
        
    def uploadFile(self):
        try:
                x = web.input(upload={})
                filename = x['upload'].filename
                originalFileName = filename
                try:
                    if filename.split(".")[-1].lower() not in ["jpg","bmp","png","gif","tif"]:
                        raise Exception,"仅接受jpg格式图片"
                except:
                    raise Exception,"仅接受jpg格式图片"

                fileType = filename.split(".")[-1]
                filename = "%d_%s.%s"%(88,str(time()),fileType)
                data = x['upload'].file.read()
                if constants.SAE_ENV:
                    bucket = Bucket('upload')
                    bucket.put()
                    
                    bucket.put_object(filename, data)
                    
                    strBuf = StringIO.StringIO(data)
                    image = Image.open(strBuf,"r")
                    width, height = image.size
                    if width > height:
                        newWidth = 128
                        newHeight = 128*height/width
                    else:
                        newHeight = 128
                        newWidth = 128*width/height
                    image.thumbnail((newWidth,newHeight),Image.ANTIALIAS)  
                    #image.resize((newWidth,newHeight),Image.ANTIALIAS)  
                    thumb_filename = filename.replace(fileType,"")[:-1]+"_128x128."+fileType
                    s = StringIO.StringIO()
                    image.save(s,"jpeg")
                    bucket.put_object(thumb_filename, s.read())
                    
                else:
                    fout = open(self.upload_dir + filename,'wb')
                    fout.write(data)
                    fout.close()
                    #thumb_filepath = mImage.make_thumb(self.upload_dir + filename)
                    #thumb_filename = os.path.basename(thumb_filepath)
                    
                    image = Image.open(self.upload_dir + filename)  
                    width, height = image.size
                    if width > height:
                        newWidth = 360
                        newHeight = 360*height/width
                    else:
                        newHeight = 480
                        newWidth = 480*width/height
                    image.thumbnail((newWidth,newHeight),Image.ANTIALIAS)
                    thumb_filename = filename.replace(fileType,"")[:-1]+"_128x128."+fileType
                    image.save(self.upload_dir+thumb_filename)
                prefix = "/static/upload/"
                oriImgUrl= prefix+filename
                thumbUrl = prefix+thumb_filename
#                 ret = json.dumps([0,oriImgUrl])
                ret = {
                    "state": "SUCCESS",
                    "url": oriImgUrl,
                    "title": filename,
                    "original": originalFileName,
                    "type":fileType,
                    "size":len(data)
                }
                ret = json.dumps(ret);
                return ret
                
        except Exception,e:
            import traceback
            traceback.print_exc()
            if constants.LOG_LEVEL > 0:
                security.log(str(e))
            return json.dumps([1,e])
                
    def genRenderBySubContent(self,content):
        header = render.header()
        navibar = render.navibar(self.username,self.gid,"stocks")
        return render.frame(header,navibar,content)