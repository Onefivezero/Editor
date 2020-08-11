









def chatterboxer(user_input):
	if(user_input[0:7] == "merhaba":
		return "Merhaba"
	elif(user_input[-5, -1] == "kapat"):
		return "Hoscakal"
	elif(user_input[0:5] == "E0602"):
		return "Hoscakal"
	else:
		return "???"



if __name__ == "__main__":
	while(1):
		x = input()
		print(chatterboxer(x))
		if(x == "kapat"):
			break