import g4f, asyncio
import nest_asyncio

nest_asyncio.apply()

async def AI(befoneContant, content):
	#print(role, content)
	flag = 1
	while flag == 1:
		try:
			response = g4f.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=[
					{"role": "user", "content":f"中文的話請用繁體中文做回覆,可以使用Markdown語法做一些特別回覆，並且請你以角色的視角給予些許表情符號、emoji回應，不用每一則訊息都回應表情符號，格式化的回應如下<Reactions>[🤮,❌,❤,❓,⭕]</Reactions>,回應一定要使用Reactions的HTML標籤包覆，任何的表情符號、emoji都可以使用，數量沒有限定，如果沒有要做回應請給我<Reactions>[None]</Reactions>，如果有回應表情符號、emoji則不需要回應<Reactions>[None]</Reactions>"},
					{"role": "assistant", "content": "> # 我了解了\n> 這樣就可以使用Markdown語法做回覆了呢！\n<Reactions>[🆗]</Reactions>"},
					{"role": "user", "content": befoneContant},
					{"role": "assistant", "content": "我了解了，那現在開始我就不會提及我們在進行角色扮演遊戲的事情，並且直接使用我所扮演的角色的視角進行交談，並且不用特別複誦使用者所說的事項。<Reactions>[None]</Reactions>"},
					{"role": "user", "content": "主人：~~嗨嗨~~"},
					{"role": "assistant", "content": "## 安安♡~。<Reactions>[None]</Reactions>"},
					{"role": "user", "content": content}
				]
			)
			flag = 0
		except:
			flag = 1
	
	return response
	

if __name__ == "__main__":
	print(AI("user", "早安~"))
	input("Press enter key to continue...")