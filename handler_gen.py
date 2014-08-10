import xmltodict
print dir(xmltodict)
x = xmltodict.parse(file("Protocol.xml").read())
handler = file("handler.py", "w+")
#print x
handler.write("class Handler(object):\n");
for msg in x['protocol']['msg']:
    if '@server' in msg and msg['@server'] == 'true':
        func = msg['@name']
        if 'param' in msg and isinstance(msg['param'],list):
            params = [param['@name'] for param in msg['param']]
        elif 'param' in msg:
            params = [msg['param']['@name']]
        else:
            params = []
        handler.write("    def %s(%s):\n        pass\n\n" % (func, ", ".join(['self'] + params)))
handler.close()
