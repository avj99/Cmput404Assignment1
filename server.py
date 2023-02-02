#  coding: utf-8 
import socketserver
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode("utf-8").strip()
        #self.data= self.data.decode("utf-8")
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        #get data and seperate it
        dataSplit= self.data.split()
        print("\n",dataSplit)
        dataRequest= dataSplit[0].split(" ")
        #print(dataRequest)
        typeDataRqst= dataRequest[0]
        #print(typeDataRqst)

        Datapath= dataSplit[1].split(" ")
        path= Datapath[0]
        #print(path)

        #request type checking
        if typeDataRqst=="GET":
            if path[:4] == "/../":
                textResponse= "HTTP/1.1 404 Not Found!\r\n"
            elif path[-4:]==".css":
                textResponse = self.getCss(path)
            elif path[-5:]==".html":
                textResponse= self.getHTML(path)
            elif path[-1:] == "/":
                textResponse= self.getIndex(path)
            else:
                textResponse = self.Redirect(path)
        else:
            #invalid 405 Error for anything other than a GET request
            textResponse= "HTTP/1.1 405 Method Not Allowed!\r\n" 

        #send the response from the returned textResponse
        self.request.sendall(bytearray(textResponse, 'utf-8'))
        return 


    def getCss(self,path):
        try:
            file= open("./www"+path)
            fileContent= file.read()
    #fileContent.close()
        except:
             textResponse = "HTTP/1.1 404 Not Found!\r\n"    
        
        if path[-8:]=="deep.css":
            textResponse= "HTTP/1.1 404 Not Found\r\n"
        elif path[-9:]=="/base.css":
            textResponse= "HTTP/1.1 200 OK Not FOUND!\r\nContent-Type: text/css\r\n\r\n{}".format(fileContent)
        else:
            textResponse = "HTTP/1.1 404 Not Found!\r\n"
        return(textResponse)

    def getHTML(self,path):
        try:
            file= open("./www"+path)
            fileContent= file.read()
        #fileContent.close()
        except:
            textResponse = "HTTP/1.1 404 Not Found!\r\n"
    
        if path[-11:]== "/index.html":
            textResponse=  "HTTP/1.1 200 OK Not FOUND!\r\nContent-Type: text/html\r\n\r\n{}".format(fileContent)
        else:
            textResponse = "HTTP/1.1 404 Not Found!\r\n"
        return(textResponse)

    def getIndex(self,path):

        try:
            file= open("./www"+path)
            fileContent= file.read()
            #fileContent.close()
        except:
            textResponse = "HTTP/1.1 404 Not Found!\r\n"

        if path[-1:] == "/":
            path += "index.html"
            file= open("./www"+path)
            fileContent= file.read()
            textResponse= "HTTP/1.1 200 OK Not FOUND!\r\nContent-Type: text/html\r\n\r\n{}".format(fileContent)
        else:
            textResponse = "HTTP/1.1 404 Not Found!\r\n"

        return(textResponse)
        
    def Redirect(self,path):
        try:
            file= open("./www"+path)
            fileContent= file.read()
        #fileContent.close()
        except:
            textResponse = "HTTP/1.1 404 Not Found!\r\n"
            
        if path[-5:]== "/deep":
            #print("hey1\n")
            path+="/"
            textResponse= "HTTP/1.1 301 Moved Permanently\r\nLocation: {}\r\n".format(path)
        elif path == "/":
            #print("hey2\n")
            path += "index.html"
            file= open("./www"+path)
            fileContent= file.read()
            textResponse= "HTTP/1.1 301 Moved Permanently\r\nLocation: {}\r\n".format(fileContent)
            print("\ test it worked\n")
        else:
            textResponse="HTTP/1.1 404 Not Found!\r\n"
        return textResponse

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
