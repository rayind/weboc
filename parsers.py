# -*- coding:utf-8 -*-
import xmltodict
class BinaryParser(object):
    def __init__(self, protocol):
        pass

class XmlParser(object):
    def __init__(self, protocol, handler):
        self.handler = handler
        self.protocol = protocol

    def parse(self, xml_string):
        xml = xmltodict.parse(xml_string)
        func_name = xml.keys()[0]
        muted = xml[func_name].get('@muted', 0)
        self.handler.muted = int(muted)
        func = getattr(self.handler, func_name)
        params = [xml[func_name][param]['#text'] if "#text" in xml[func_name][param] else xml[func_name][param]
                  for param in self.protocol.get_params(func_name)]
        func(*params)
