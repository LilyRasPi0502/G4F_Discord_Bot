import g4f, asyncio
import nest_asyncio
#import json

nest_asyncio.apply()

async def GPT(message):
	#print(message)
	response = ""
	while response == "":
		try:
			response = g4f.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=message
			)
		except:
			pass
			
	return response
	

if __name__ == "__main__":
	data = json.loads('{"role":["user","assistant","user"], "content":["早安老婆~","早安呀寶貝♡","老婆你今天想做甚麼呀?"]}')
	msg = [{"role": data["role"][i], "content": data["content"][i]} for i in range(len(data["role"]))]
	print(GPT(msg))
	#input("Press enter key to continue...")
