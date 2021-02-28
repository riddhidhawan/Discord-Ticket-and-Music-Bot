import discord
import os

from replit import db
from keep_alive import keep_alive

# from keepAlive import keep_alive

client=discord.Client()

def add_to_queue(name,id):
  # Expand user database
  Udata=dict()
  if "Udata" in db.keys():
    Udata=db["Udata"]
  Udata[id]=name
  db["Udata"]=Udata
  #adding to Queue
  Q=[]
  if "Q" in db.keys():
    Q=db["Q"]
  if id not in Q:
    Q.append(id)
    db["Q"]=Q
    return ("Successfully added <@%s> to queue"%str(id))
  else :
    return("<@%s> you are already in the queue"%str(id))


def del_from_queue(id):
  if "Q" in db.keys():
    Q=db["Q"]
    if id in Q:
      Q.remove(id)
      db["Q"]=Q
      return ("<@%s> you have been removed from the queue"%str(id))
    else:
      return ("<@%s> you have not joined the queue"%str(id))
  else:
    return "Queue hasn't been created yet"

def dispQ():
  Q=[]
  nameQ=[]
  if "Q" in db.keys() :
    Q=db["Q"]
  if "Udata" in db.keys():
    Udata=db["Udata"]
    for i in Q:
      nameQ.append(Udata.get(str(i),0))
  if len(Q)>0:
    res='''**__Current Queue is:__** \n`'''
    for i in range(len(nameQ)):
      res+=str(i+1)+'. '+nameQ[i]+'\n'
    res+="`"
    return res
  else:
    return "Queue is empty"

def remove(string):
  
  try:
    print(string)
    index=int(string[1].split(' ',1)[0])-1
   
    name=(string[1].split(' ',1))[1]
    print(name)
   
    Q=[]
    if "Q" in db.keys():    
      Q=db["Q"]
      print(Q[int(index)])  
      if "Udata" in db.keys():
          Udata = db["Udata"]
          print(Udata)
          if(Udata.get(str(Q[int(index)]))==name):
            del Q[int(index)]
            db["Q"]=Q
            
            return "Deletion Successful"
          else:
            return "Delete unsuccessful. Check index and name"

    else:
      return("Queue has not yet been created")
  except:
      return("Remove failed. Check that the format of your command is of the format \"rem position name\" ")
  
def callNext(id):
  Q=[]
  if "Q" in db.keys():
    Q=db["Q"]
    if len(Q)>0:
      next=Q[0]
      Q.remove(Q[0])
      db["Q"]=Q
      currentStat={}
      if "currentStat" in db.keys():
            currentStat=db["currentStat"]
      check=currentStat.get(str(id),None)
      if check==None:
        currentStat[id]=next
        db["currentStat"]=currentStat
        return (("<@%s> you have been assigned to "%str(next))+"<@%s>"%str(id))
      else:
        print("user put on hold")
        hold(id,check)
        currentStat[id]=next
        db["currentStat"]=currentStat
        return ((("<@%s> has been put on hold\n")%str(check))+("<@%s> you have been assigned to "%str(next))+"<@%s>"%str(id))

    else:
      return "Queue is currently empty."
  else:
    return "Queue has not been created yet"
  
def hold(admin,id):
  holdQ=[]
  if "holdQ" in db.keys():
    holdQ=db["holdQ"]
  if id not in holdQ:
    holdQ.append(id)
  db["holdQ"]=holdQ
  if "currentStat" in db.keys():
    currentStat=db["currentStat"]
    del currentStat[str(admin)]
    db["currentStat"]=currentStat
    print(currentStat)


def dispHold():
  holdQ={}
  if "holdQ" in db.keys():
    holdQ=db["holdQ"]
  nameQ=[]
  for i in holdQ:
    nameQ.append(db["Udata"].get(str(i)))
  if len(holdQ)>0:
    result="```People on hold currently:\n"
    for i in len(range(nameQ)):    
      result+=str(i)+". "+nameQ[i]+'\n'
    result+="\n"
    return result
  else:
    return "Hold queue is currently empty"
  
def unhold(admin,index)  :
  holdQ=[]
  if "holdQ" in db.keys():
    holdQ=db["holdQ"]
    unholdId=(holdQ[index])
    currentStat={}
    if "currentStat" in db.keys():
      currentStat=db["currentStat"]
      check=currentStat.get(str(admin),None)
      result=""
      if check is None:
        currentStat[str(admin)]=unholdId
        result=(("<@%s> you're issue has been taken off hold and you have been assigned to "%str(unholdId))+("<@%s>"%str(admin)))
      else:
        hold(admin,check)
        currentStat[str(admin)]=unholdId
        result=(("<@%s> you have been put on hold \n")+("<@%s> you're issue has been taken off hold and you have been assigned to "%str(unholdId))+("<@%s>"%str(admin)))
      del holdQ[index]
      db["holdQ"]=holdQ
      db["currentStat"]=currentStat
      return result

def solved(admin):
  currentStat=db["currentStat"]
  check=currentStat.get(str(admin),None)
  if check is not None:
      del currentStat[str(admin)]
      return("Issue has been resolved as solved.")
  else:
    return("No current issue was assigned to you to be solved")
  db["currentStat"]=currentStat
# Now register an event
@client.event
async def on_ready():
    #now the bot is ready to run
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  msg=message.content
  name=message.author.name
  Uid=message.author.id
  if message.author==client.user:
    return
  
  
  if msg.startswith('*add'):
    currentQ=add_to_queue(name,Uid)
    await message.channel.send(currentQ)
  
  elif msg.startswith('*del'):
    resultQ=del_from_queue(Uid)
    await message.channel.send(resultQ)
  
  elif msg.startswith('*show'):
    await message.channel.send(dispQ())
    
  
  elif msg.startswith('*rem'):
    if(discord.utils.get(message.author.roles, name="admin")) is None and (discord.utils.get(message.author.roles, name="b3")) is None:
      await message.channel.send("You do not have sufficient permissions")      
      
    else:
      try:
        
        x=msg.split('*rem ',1)
        
        await message.channel.send(remove(x))

      except:
        await message.channel.send("remove failed")
      
  
  elif msg.startswith('*call next'):
    if(discord.utils.get(message.author.roles, name="admin")) is None and (discord.utils.get(message.author.roles, name="board")) is None:
      await message.channel.send("You do not have sufficient permissions")      
    else:
      await message.channel.send(callNext(Uid))
  
  elif msg.startswith("*display hold"):
    if(discord.utils.get(message.author.roles, name="admin")) is None and (discord.utils.get(message.author.roles, name="board")) is None:
      await message.channel.send("You do not have sufficient permissions")      
    else:
      await message.channel.send(dispHold())
  
  elif msg.startswith("*hold"):
    
    if "currentStat" in db.keys(): 
      user=db["currentStat"].get(str(Uid),None)
      if user is not None:
        hold(Uid,user)
        await message.channel.send("<@%s> put on hold"%user)
  elif msg.startswith('*BIG RED BUTTON'):
    print('ran')
    try:
      del db["Q"]
      del db["holdQ"]
      del db["currentStat"]
      await message.channel.send("All datas has been wiped clean")
    except:
      await message.channel.send("All datas has been wiped clean")
  
  elif msg.startswith('*unhold'):
    if(discord.utils.get(message.author.roles, name="admin")) is None and (discord.utils.get(message.author.roles, name="board")) is None:
      await message.channel.send("You do not have sufficient permissions")      
    else:
      index=int((msg.split('*unhold ',1))[1])-1
      await message.channel.send(unhold(Uid,index))
  elif msg.startswith('*solved'):
    if(discord.utils.get(message.author.roles, name="admin")) is None and (discord.utils.get(message.author.roles, name="board")) is None:
      await message.channel.send("You do not have sufficient permissions")      
    else:
      solved(Uid)
  # elif msg.startswith('*help'):
  #   helpMsg='''
  #   \t**PARTICIPANTS COMMANDS**
  #   `*add` - To add themselves to the queue
  #   `*del` - To remove themselves from the queue
  #   `*show` - To show the current queue

  #   **TECH SUPPORT COMMANDS**
  #   `*rem <index> <name>` - To remove someone from the queue
  #   `*call next` - Assigns the next person in queue to them
  #   `*hold` - To transfer the current doubt that they are solving to a on-hold list
  #   `*display hold` - To show a list of everyone currently on hold
  #   `*unhold <index>` - To pull someone from the hold list to try and resolve their doubts again
  #   '''
  #   await message.channel.send(helpMsg)
  elif msg.startswith('*initialise'):
    channel=(message.channel.id)
    db["channel"]=channel
    xyz=await message.channel.send('**Hey! :wave: I am Mr. Fixit, a ticketing bot with :heart: by our team at ISTE-VIT to solve all your doubts.**\n\nReact to this with:\n\n :tickets: - to be added to the queue\n\n:wastebasket: - To remove yourself from the queue\n\n:scroll: - To show the queue \n\n **See you around :smiley:**')
    await xyz.add_reaction('🎟️')
    await xyz.add_reaction('🗑️')
    await xyz.add_reaction('📜')
  
  elif msg.startswith('*admin'):
    xyz=await message.channel.send('''Mods, react to this with :\n\n :telephone: - To call the next person in queue \n\n:raised_back_of_hand: - To put the issue you are currently handling on hold\n\n:newspaper: - To show list of people on hold\n\n :green_heart: - Once you have solved a doubt \n\n **type **\n`rem <index> <name>` -  to remove someone from the queue \n\n`unhold <index>` to take someone who is on the hold list and start solving their doubt again \n\n **All the best :grin:** ''')
    await xyz.add_reaction('☎️')
    await xyz.add_reaction('🤚')
    await xyz.add_reaction('📰')
    await xyz.add_reaction('💚')

  # print(message.channel.id)

  
@client.event
async def on_reaction_add(reaction,user):
  print(reaction.emoji)
  if (client.user!=user):
    await reaction.remove(user)
    channel = client.get_channel(815574991524593704)
    if reaction.emoji=='🎟️':
      
      await channel.send(add_to_queue(user.name,user.id))
    if reaction.emoji=='🗑️':
      resultQ=del_from_queue(user.id)
      await channel.send(resultQ)
      
    if reaction.emoji=='📜': 
      await channel.send(dispQ())
    if reaction.emoji=='☎️':
      if(discord.utils.get(user.roles, name="admin")) is None and (discord.utils.get(user.roles, name="board")) is None:
        await channel.send("<@%s> you do not have sufficient permissions to call the next person"%str(user.id))
      else:
        await channel.send(callNext(user.id))
    if reaction.emoji=='🤚':
      if(discord.utils.get(user.roles, name="admin")) is None and (discord.utils.get(user.roles, name="board")) is None:
        await channel.send("<@%s> you do not have sufficient permissions to call the next person"%str(user.id))
      else:
        issue=db["currentStat"].get(str(user.id),None)
        if issue is not None:
          hold(user.id,issue)
          await channel.send("<@%s> put on hold"%issue)
    if reaction.emoji=='📰':
      if(discord.utils.get(user.roles, name="admin")) is None and (discord.utils.get(user.roles, name="board")) is None:
        await channel.send("<@%s> you do not have sufficient permissions"%str(user.id))
      else:
         await channel.send(dispHold())
    if reaction.emoji=='💚':
      if(discord.utils.get(user.roles, name="admin")) is None and (discord.utils.get(user.roles, name="board")) is None:
        await channel.send("<@%s> you do not have sufficient permissions to call the next person"%str(user.id))
      else:
        await channel.send(solved(user.id))
keep_alive()
client.run(os.getenv('TOKEN'))

