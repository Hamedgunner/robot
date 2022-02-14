from re import findall
from rubika import Bot
import time

bot = Bot("bbsjcknmjfkedlrqumjcoyseqaoqdavd")
target = "g09ZBX07aadd1e1ac73551905a824ed6"

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
	

# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گزاشتن لینک در گروه ممنوع میباشد .\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 کاربر [ @"+user+" ] \n (3/3) اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "!off" and msg.get("author_object_guid") in admins :
							sleeped = True
							bot.sendMessage(target, "bot is turned off", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("!del") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +"پیام مورد نظر با موفقیت حذف شد", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "پیام مورد نظر با موفقیت حذف شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("!ban") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("!add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ کاربر محدود میباشد", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))

						
						elif msg.get("text") == "دستورات":
							bot.sendMessage(target, "🌀 admins : \n 🔆 (!add ID) افزودن کاربر با آی دی \n 🚫 (!ban ID) حذف کاربر با آی دی یا ریپلای کردن روی پیام آن \n 🚷 (!slowmode / !offslowmode) روشن کن حالت آرام ده ثانیه ای یا غیرفعال کردن آن \n ⚠️ (اخطار) اخطار دادن به کاربر با ریپلای کردن روی پیام آن \n 🤖 (!on / !off) روشن کردن ربات یا خاموش کردن آن \n", message_id=msg.get("message_id"))
						
						elif msg.get("text") == "قوانین":
							rules = open("rules.txt","r",encoding='utf-8').read()
							bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							
						elif msg.get("text").startswith("!updaterules") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("!updaterules")))
								bot.sendMessage(target, "✅  قوانین بروزرسانی شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text") == "!slowmode" and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
						elif msg.get("text") == "!offslowmode" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ امکان اخطار دادن به مدیران وجود ندارد!", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ امکان اخطار دادن به مدیران وجود ندارد!", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))



						elif msg.get("text") == "!lock" and msg.get("author_object_guid") in admins :
							bot.setMembersAccess(target, ["AddMember"])
							bot.sendMessage(target, "🔒 گروه قفل شد", message_id=msg.get("message_id"))

						elif msg.get("text") == "!unlock" and msg.get("author_object_guid") in admins :
							bot.setMembersAccess(target, ["SendMessages","AddMember"])
							bot.sendMessage(target, "🔓 گروه اکنون باز است", message_id=msg.get("message_id"))

					else:
						if msg.get("text") == "!on" and msg.get("author_object_guid") in admins :
							sleeped = False
							bot.sendMessage(target, "bot is turned on", message_id=msg.get("message_id"))

				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"کاربر {user} به دلیل رعایت نکردن قوانین از گروه با موفقیت حذف شد.", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
					
					elif data["type"]=="AddedGroupMembers":
						user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"کاربر {user} با موفقیت به گروه افزوده شد.", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
					
					elif data["type"]=="LeaveGroup":
						user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"خدانگهدار {user} 👋 ", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
						
					elif data["type"]=="JoinedGroupByLink":
						user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f" کاربر {user} به گروه Chit Chat خوش اومدی \n لطفا قوانین رو رعایت کن.", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
