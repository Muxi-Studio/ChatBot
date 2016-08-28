# coding: utf-8
def replace_word(text):
	words = {'心理学院':'华中师范大学田家炳楼',
			'9号楼':'华中师范大学9号教学楼',
			'9号教学楼':'华中师范大学9号教学楼',
			'8号楼':'华中师范大学8号教学楼',
			'8号教学楼':'华中师范大学8号教学楼',
			'图书馆':'华中师范大学图书馆'
	}
	for i in words:
		text = text.replace(i,words[i])
	return text