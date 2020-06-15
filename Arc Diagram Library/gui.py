import os, sys

sys.path.append("./atlastk")
sys.path.append("../atlastk")

import atlastk as Atlas

head = '''
	<title>Arc Diagram Tools</title>
'''

body = '''
	<p>text tead;lfgkja ;lasdfkj </p>
'''

def acConnect(dom):
	dom.setLayout("", body )

callbacks = {
	"": acConnect,
}
	
Atlas.launch(callbacks, None, head)
