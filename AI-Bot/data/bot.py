# -*- coding: utf-8 -*-

from discord.ext import tasks
from discord.ext import commands
from Fnc.GPT import *
from datetime import *

import discord
import asyncio
import json
import pytz

intents		= discord.Intents.default()
intents.message_content = True
intents.members = True

config		= open("data/json/DC_config.json", "r", encoding="utf-8")
conf		= json.load(config)
bot_ID		= conf["bot_ID"]
Master_ID	= conf["Master_ID"]
Token		= conf["DC_key"]

class MyBot(commands.Bot):
	
	def __init__(self, command_prefix, intent):
		commands.Bot.__init__(self, command_prefix=command_prefix, intents=intent)
		
	
	async def on_ready(self):
		self.message1 = f"正在使用身分: {self.user}({self.user.id})"
		self.message2 = f"正在使用身分: {self.user}({self.user.id})"
		print(self.message1)
		self.changeActivity.start()
		self.add_commands()
	
	async def on_message(self, message):
		#排除自己的訊息，避免陷入無限循環
		if str(message.author).find(str(self.user)) != -1:
			return
		#設定是否已回覆旗標
		send = True

		#列印接收到的訊息
		print(f"[{Get_Time()}] Get Message from {str(message.guild)}.{str(message.channel)}.{str(message.author.display_name)}: {str(message.content)}")
		
		#判斷有無回覆訊息
		if message.reference is not None:
			#獲取被回覆的訊息
			ctx = await message.channel.fetch_message(message.reference.message_id)
		
			#如果被回覆的對象是此機器人
			if str(ctx.author).find(str(self.user)) != -1:
				await self.cmd(message, f"{self.ID_To_Name(message.content)}")
				send = False
	
		#指令程序
		if ((message.content.find(bot_ID) != -1) or (self.is_Mention(message.content))) and (send == True):
	
			await self.cmd(message, self.ID_To_Name(message.content))
			send = False

	async def Reaction(self, message, Str):
		Str = Str.split("<Reactions>")[-1]
		Str = Str.split("</Reactions>")[0]
		Str = Str.split("[")[-1]
		Str = Str.split("]")[0]
		#print(Str)
		if Str.find("None") == -1:
			if Str.find(",") != -1:
				emojiList = Str.split(",")
				for emoji in emojiList:
					try:
						await message.add_reaction(emoji)
					except:
						pass
			else:
				try:
					await message.add_reaction(Str)
				except:
					pass


	#指令讀取
	async def cmd(self, ctx, cmd):
		
		if cmd.find("Replace ") != -1:					#測試功能:取代訊息
			if ctx.reference is not None:
				message = await ctx.channel.fetch_message(ctx.reference.message_id)
				print(f"[{Get_Time()}] Replace message of {str(ctx.guild)}.{str(ctx.channel)}: {message.content}")
				if len(message.content) > 0:
					await self.sender(ctx, message.content)
				if message.attachments:
					FileName	= f"./data/file/file.{message.attachments[0].url.split('/')[-1].split('.')[-1]}"
					res2 = requests.post(message.attachments[0].url)
					with open(FileName, mode='wb') as f:
						f.write(res2.content)
					await self.FileSender(ctx, FileName)
				try:
					await message.delete()
				except:
					print("沒有權限")
			else:
				print(f"[{Get_Time()}] Replace message of {str(ctx.guild)}.{str(ctx.channel)}: {cmd.split('Replace ')[1]}")
				await ctx.channel.send(cmd.split("Replace ")[1])
				if ctx.attachments:
					FileName	= f"./data/file/file.{ctx.attachments[0].url.split('/')[-1].split('.')[-1]}"
					res2 = requests.post(ctx.attachments[0].url)
					with open(FileName, mode='wb') as f:
						f.write(res2.content)
					await self.FileSender(ctx, FileName)
			try:
				await ctx.delete()
			except:
				print("沒有權限")
		
		
		elif cmd.find("CMD") != -1:					#測試功能:CMD
			import os
			async with ctx.channel.typing():
				os.system(cmd.split("CMD ")[-1])
			msg = await ctx.reply(f"Used command: {cmd.split('CMD ')[-1]}")
			print(f"[{Get_Time()}] Reply message to {str(ctx.guild)}.{str(ctx.channel)}.{ctx.author.display_name}: {msg.content}")
		elif cmd.find("Restart") != -1:					#測試功能:Restart
			await self.CloseSelf()
			msg = await ctx.reply(f"Restart{self.user}")
			print(f"[{Get_Time()}] Reply message to {str(ctx.guild)}.{str(ctx.channel)}.{ctx.author.display_name}: {msg.content}")
		else:								#連接GPT Free
			
			async with ctx.channel.typing():
				f = open("data/json/CharacterSet.json", "r", encoding="utf-8")
				Chara = json.load(f)

				ctxList = []

				#判斷有無回覆訊息
				if ctx.reference is not None:
					#獲取被回覆的訊息
					ctxRe = await ctx.channel.fetch_message(ctx.reference.message_id)
					ctxList.append(ctxRe)
					while ctxRe.reference is not None:
						ctxRe = await ctxRe.channel.fetch_message(ctxRe.reference.message_id)
						ctxList.append(ctxRe)

				text, usercontant = await self.ChangeText(ctx, f"{Chara['Character']}")

				GPTmsg = [f"{usercontant}"]
				GPTrole = ["user"]

				for ctxOut in ctxList:
					if ctxOut.author == self.user:
						GPTrole.append("assistant")
						Reaction = []
						ctxRe = await ctxOut.channel.fetch_message(ctxOut.reference.message_id)
						for Reactions in ctxRe.reactions:
							Reaction.append(Reactions.emoji)
						GPTmsg.append(f"{ctxOut.guild}.{ctxOut.channel}.{ctxOut.author}:{ctxOut.content}<Reactions>{str(Reaction)}</Reactions>")
					else:
						GPTrole.append("user")
						GPTmsg.append(f"{ctxOut.guild}.{ctxOut.channel}.{ctxOut.author}:{ctxOut.content}")

				GPTmsg.append(text)
				GPTrole.append("user")
				GPTmsg.append("## 安安♡~。<Reactions>[None]</Reactions>")
				GPTrole.append("assistant")
				
				GPTmsg.append("~~嗨嗨~~")
				GPTrole.append("user")
				GPTmsg.append("> # 我了解了\n> 這樣就可以使用Markdown語法做回覆了呢！\n<Reactions>[🆗]</Reactions>")
				GPTrole.append("assistant")
				GPTmsg.append("中文的話請用繁體中文做回覆,可以使用Markdown語法做一些特別回覆，不可以擅自猜測對方性別，不用復誦對方說的話，並且請你以角色的視角給予些許表情符號、emoji回應，不用每一則訊息都回應表情符號，格式化的回應如下<Reactions>[🤮,❌,❤,❓,⭕]</Reactions>,回應一定要使用Reactions的HTML標籤包覆，任何的表情符號、emoji都可以使用，數量沒有限定，如果沒有要做回應請給我<Reactions>[None]</Reactions>，如果有回應表情符號、emoji則不需要回應<Reactions>[None]</Reactions>")
				GPTrole.append("user")
				
				GPTMessage = [{"role": GPTrole[i], "content": GPTmsg[i]} for i in range(len(GPTmsg))]
				GPTMessage.reverse()
				GPTMessage.append({"role": "user", "content": "請直接回答無須標註身分"})
				Str = "0-0-0"
				Str = await GPT(GPTMessage)
				while Str.find("0-0-0") != -1:
					pass
				await self.Reaction(ctx, Str)
				if Str.find("Reactions") != -1 or (Str.find("[") != -1 and Str.find("]") != -1):
					Str = (Str.split("[")[0] + Str.split("]")[-1])
					Str = Str.replace("<Reactions>", "")
					Str = Str.replace("</Reactions>", "")

				try:
					msg = await ctx.reply(Str)

				except:
					f = open("data/json/CharacterSet.json", "r", encoding="utf-8")
					text, usercontant = await self.ChangeText(ctx, ctx, f"{Chara['Err']}")
					Str = "抱歉出了一些錯誤"
					while Str.find("0-0-0") != -1:
						pass
					msg = await ctx.reply(Str)

			print(f"[{Get_Time()}] Reply message to {str(ctx.guild)}.{str(ctx.channel)}.{ctx.author.display_name}: {msg.content}")

	async def ChangeText(self, ctx, text):
		if ctx.reference is not None:
			f = open("data/json/CharacterSet.json", "r", encoding="utf-8")
		
			msg = f"{json.load(f)['Reference']}"
			rectx = await ctx.channel.fetch_message(ctx.reference.message_id)
			msg = msg.replace("&reference;", str(self.ID_To_Name(rectx.content)))
			msg = msg.replace("&rauthor;", str(rectx.author.display_name))
		else:
			msg = ""
		contant = f"{ctx.guild}.{ctx.channel}.{ctx.author.display_name}：「{ctx.content}」"
		text = text.replace("&guild;", str(ctx.guild))
		text = text.replace("&channel;", str(ctx.channel))
		text = text.replace("&mauthor;", str(ctx.author.display_name))
		text = text.replace("&Master_ID;", str(Master_ID))
		text = text.replace("&bot_ID;", str(bot_ID))
		text = text.replace("--Search", "")
		text = text.replace("&ReferenceSTR;", str(self.ID_To_Name(msg)))
		text = text.replace("&Time;", str(Get_Time()))
		return text, contant

	async def CloseSelf(self):
		try:
			await self.close()
		except:
			pass
		finally:
			exit()
		
	#傳送訊息用
	async def sender(self, Message, Str):
		await Message.channel.send(Str)
		print(f"[{Get_Time()}] Send message to {str(Message.guild)}.{str(Message.channel)}: {Str}")

	#傳送檔案用
	async def FileSender(self, Message, File):
		print(f"[{Get_Time()}] Send file to {str(Message.guild)}.{str(Message.channel)}")
		await Message.channel.send(file=discord.File(File))

	#是否被文字提及
	def is_Mention(self, Message):
		My_Name = open("data/json/Name.json", "r", encoding="utf-8")
		data			=	json.load(My_Name)
		NameList		=	data["Name"]
		for i in range(len(NameList)):
			FindName	=	NameList[str(i)]
			if Message.find(FindName) != -1:
				return True
		return False


	#將代號或ID指向默認的名字
	def ID_To_Name(self, Message):
		My_Name = open("data/json/Name.json", "r", encoding="utf-8")
		data			=	json.load(My_Name)
		if Message.find("Rename") != -1:
			return Message
		return Message.replace(bot_ID, data["DefaultName"])
	
	#更改機器人狀態
	@tasks.loop(seconds=5.0)
	async def changeActivity(self):
		f = open("data/json/Stetas.json", "r", encoding="utf-8")
		data			=	json.load(f)
		State			=	data["State"]
		await self.change_presence(activity=discord.Activity(name=State, type=0))
		
	utc = timezone.utc
	times = [
		time(hour=0, tzinfo=utc),
		time(hour=8, tzinfo=utc),
		time(hour=16, tzinfo=utc)
	]
	#Reflash CharacterAI
	@tasks.loop(time=times)
	async def Reflash_CharacterAI(self):
		await self.Reflash_Character()
		await self.CloseSelf()
		
	def add_commands(self):
		@self.command(name="status", pass_context=True)
		async def status(ctx):
			print(ctx)


def bot1():
	# Your code here
	bot = MyBot(command_prefix="/", intent=intents)
	bot.run(Token)

	

#獲取時間
def Get_Time():
  
	dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
	dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

	#timezone_TW = pytz.timezone('ROC')
	#now = datetime.now(timezone_TW)
	return dt2.strftime("%Y-%m-%d %H:%M:%S")


bot1()