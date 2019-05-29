    @classmethod
    def click_element(cls, page, xpath, adj_x=None, adj_y=None):
        # Get windows form container's lef-top position
        if page == 'Smartbar' or page == 'Sidebar':
            dlg = cls.mainWin.child_window(title="AdxTaskPane", control_type="Pane", found_index=0)
            dlg_left = int(dlg.rectangle().left) + 8
            dlg_top = int(dlg.rectangle().top) + 6
        else:
            dlg = cls.mainWin.child_window(auto_id="lblTitle", control_type="Text")
            dlg_left = int(dlg.rectangle().left)
            dlg_top = int(dlg.rectangle().top)

        #print(dlg.rectangle())

        # Establish local debug web sockets (debug interface provided by Essetial Objects) to get web element relative postion
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.getBoundingClientRect()"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'"))
        msg_left = temp.replace('JS', js + '.left')
        msg_top = temp.replace('JS', js + '.top')
        msg_width = temp.replace('JS', js + '.width')
        msg_height = temp.replace('JS', js + '.height')

        print('Sent: ' + msg_left)
        ws.send(msg_top)
        result =  ws.recv()
        print("Received-top: '%s'" % result)
        ele_top =  result[result.find('"description":"') + 15 : result.find('"}}}')]

        ws.send(msg_left)
        result =  ws.recv()
        print("Received-left: '%s'" % result)
        ele_left =  result[result.find('"description":"') + 15 : result.find('"}}}')]

        ws.send(msg_width)
        result =  ws.recv()
        print("Received-width: '%s'" % result)
        ele_width =  result[result.find('"description":"') + 15 : result.find('"}}}')]

        ws.send(msg_height)
        result =  ws.recv()
        print("Received-height: '%s'" % result)
        ele_height =  result[result.find('"description":"') + 15 : result.find('"}}}')]
        ws.close()
        
        # offset windows form container's title bar width/height (-10 for x / +22 for y)
        offset_x = float(ele_left) + 0.5 * float(ele_width) - 10
        offset_y = float(ele_top) + 0.5 * float(ele_height) + 22 # 22 pixel is the height of title bar

        if adj_x != None:
            mouse.press(coords=(int(offset_x) + adj_x + dlg_left, int(offset_y) + adj_y + dlg_top))
            time.sleep(0.1)
            mouse.release(coords=(int(offset_x) + adj_x + dlg_left, int(offset_y) + adj_y + dlg_top))
        else:
            #use mouse press/release to handle click missing issue
            mouse.press(coords=(int(offset_x) + dlg_left, int(offset_y) + dlg_top))
            time.sleep(0.1)
            mouse.release(coords=(int(offset_x) + dlg_left, int(offset_y) + dlg_top))
           
    @classmethod
    def set_element_text(cls, page, xpath, text):
        App.click_element(page, xpath)
        time.sleep(1)
        text = text.replace(' ', '{SPACE}')
        SendKeys('^a{DELETE}')
        SendKeys(text)           
        
    # Use java script to get web element infomation for assertions
    @classmethod
    def get_elements_text(cls, page, xpath):
        res = []
        length = cls.get_elements_length(page, xpath)
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText"
        for i in range(length):
            js = js_temp.replace('XPATH', '(' + xpath.replace('"', '\\"') + ')[' + str(i + 1) + ']')
            msg = temp.replace('JS', js)
            print('Sent: ' + msg)
            ws.send(msg)
            result = ws.recv()
            print("Received: '%s'" % result)
            res.append(json.loads(result)['result']['result']['value'])
        ws.close()
        return res

    @classmethod
    def get_element_title(cls, page, xpath):  
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.title"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'"))
        msg = temp.replace('JS', js)
        print('Sent: ' + msg)
        ws.send(msg)
        result =  ws.recv()
        print("Received: '%s'" % result)
        ws.close()
        result = json.loads(result)
        res =  result['result']['result']['value']
        return res

    @classmethod
    def get_element_value(cls, page, xpath):
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)" \
                  ".singleNodeValue.value"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'"))
        msg = temp.replace('JS', js)
        print('Sent: ' + msg)
        ws.send(msg)
        result = ws.recv()
        print("Received: '%s'" % result)
        ws.close()
        res = json.loads(result)['result']['result']['value']
        return res

    @classmethod
    def get_element_attribute_names(cls, page, xpath):
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)" \
                  ".singleNodeValue.getAttributeNames().join(',')"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'"))
        msg = temp.replace('JS', js)
        print('Sent: ' + msg)
        ws.send(msg)
        result = ws.recv()
        print("Received: '%s'" % result)
        ws.close()
        res = json.loads(result)['result']['result']['value']
        attrs = res.split(',')
        return attrs

    @classmethod
    def get_element_attribute_value(cls, page, xpath, attribute_name):
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)" \
                  ".singleNodeValue.getAttribute('" + attribute_name + "')"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'"))
        msg = temp.replace('JS', js)
        print('Sent: ' + msg)
        ws.send(msg)
        result = ws.recv()
        print("Received: '%s'" % result)
        ws.close()
        res = json.loads(result)['result']['result']['value']
        return res

    @classmethod
    def get_element_outerhtml(cls, page, xpath):
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.outerHTML"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'"))
        msg = temp.replace('JS', js)
        print('Sent: ' + msg)
        ws.send(msg)
        result =  ws.recv()
        print("Received: '%s'" % result)
        ws.close()
        result = json.loads(result)
        res =  result['result']['result']['value']
        return res
        
   @classmethod
    def wait_exists(cls, page, xpath, timeout=30):
        ws = create_connection(App.get_ws_url(page))
        temp = '{"id":1, "method":"Runtime.evaluate","params":{"expression":"JS"}}'
        js_temp = "document.evaluate('XPATH', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength"
        js = js_temp.replace('XPATH', xpath.replace('"', '\\"').replace("'", "\\\\'")) # one replacement
        msg = temp.replace('JS', js)
        for i in range(int(timeout)):
            print('Sent: ' + msg)
            ws.send(msg)
            result = ws.recv()
            print("Received: '%s'" % result)
            res = json.loads(result)['result']['result']['value']
            if int(res) > 0:
                ws.close()
                return True
            else:
                time.sleep(1)
        ws.close()
        return False
