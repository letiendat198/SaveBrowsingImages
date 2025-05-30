from burp import IBurpExtender, IProxyListener, IHttpListener, IResponseInfo
from java.io import PrintWriter
from datetime import datetime

class BurpExtender(IBurpExtender, IProxyListener, IHttpListener, IResponseInfo):
    def registerExtenderCallbacks( self, callbacks):
        extName = "Save Images"
        # keep a reference to our callbacks object and add helpers
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        # set our extension name
        callbacks.setExtensionName(extName)

        # obtain our output streams
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)

        # register ourselves as a Proxy listener
        callbacks.registerHttpListener(self)

        # print extension name
        self._stdout.println(extName)

        return

    def processHttpMessage(self, toolflag, messageIsRequest, messageInfo):
        if (messageIsRequest == False):
            response = messageInfo.getResponse()
            request = messageInfo.getRequest()
            responseInfo = self._helpers.analyzeResponse(response)
            requestInfo = self._helpers.analyzeRequest(messageInfo)

            # Find out if image
            url = requestInfo.getUrl()
            params = requestInfo.getParameters()
            fileName = "-1"
            for param in params:
                if param.getName() == 'page':
                    fileName = param.getValue()
                    break
            self._stdout.println(url)
            inferredMime = responseInfo.getInferredMimeType()
            statedMime = responseInfo.getStatedMimeType()
            # Build list to compare against
            imageMimeTypes = ["JPEG", "PNG"]

            # Get response body
            bodyOffset = responseInfo.getBodyOffset()
            self._stdout.println(bodyOffset)
            # Build image request body
            imgData = response[bodyOffset:]
            self._stdout.println(imgData)

            if (statedMime in imageMimeTypes) or (inferredMime in imageMimeTypes):
                # Build file path
                filePathBase = "D:/SaveBrowsingImages/Images/"
                # fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                fileExtension = "." + inferredMime.lower()
                # Write to file
                f = open(filePathBase + fileName + fileExtension, "wb")
                f.write(imgData)
                f.close()
        return
