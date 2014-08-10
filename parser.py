class BinaryParser(object):
    def __init__(self, protocol):
        pass

class XmlParser(object):
    def __init__(self, protocol):
        pass

import xmltodict
class ProtocolReader(object):
    def __init__(self, protocol):
        self.protocol = {}
        x = xmltodict.parse(file("Protocol.xml").read())
        for msg in x['protocol']['msg']:
            if '@server' in msg and msg['@server'] == 'true':
                func = msg['@name']
                self.protocol[func] = {}
                if 'param' in msg and isinstance(msg['param'],list):
                    for param in msg['param']:
                        self.protocol[func][param['@name']] = self.parse_type(param['@type'])
                elif 'param' in msg:
                    self.protocol[func][msg['param']['@name']] = self.parse_type(msg['param']['@type'])
                else:
                    params = []

    def keys_list(self):
        return self.protocol.keys()

    def parse_type(self, param_type):
        param_type = param_type[:-2] if param_type[-2:] == "[]"else param_type
        if param_type in ["string", "ulong", "byte", "bool", "int", "Guid", "ushort", "short"]:
            param_type_res = param_type
        elif param_type in ["Card", "ControllableObject", "Group"]:
            param_type_res = "int"
        elif param_type in ["Player", "CardOrientation"]:
            param_type_res = 'byte'
        elif param_type in ["Version", "Color?"]:
            param_type_res = 'string'
        else:
            print param_type
            param_type_res = 'string'
        if param_type [-2:] == "[]":
            param_type_res += "[]"
        return param_type_res

    def get_type(self, command, param):
        if type(command) == int:
            command = self.protocol.keys()[command]
        command_info= protocol.get(command, None)
        if command_info:
            return command_info.get(param, None)
        return

p = ProtocolReader(file("Protocol.xml"))
#print p.protocol
