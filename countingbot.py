import discord,json
import sys , os , discord , subprocess , io , random  ,time , glob,asyncio 
from math import factorial

client = discord.Client()
max_no = 0.0
highscore = 0.0
try:
    num_file=open('number.number',mode="r", encoding="utf-8")
    max_no=eval(num_file.read())
    num_file.close()
except:
    num_file=open('number.number',mode="w", encoding="utf-8")
    num_file.write(str(max_no))
    num_file.close()


f = io.open("num.json", mode="r", encoding="utf-8")
numfact = json.load(f)


def system_call(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return (output,err)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    statustxt = "Couting numbers +1"
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    global max_no,highscore,numfact
    num_file=open('number.number',mode="r", encoding="utf-8")
    max_no=eval(num_file.read())
    num_file.close()
    
    
    if message.author == client.user:
        return

    if(str(message.channel.name) == "counting"): 
        try:
            instr = str(message.content).replace('^','**')
            if('!' in message.content):
                try:
                    output = factorial(int(message.content[:-1]))
                except:
                    output = 0

            else:
                output = float(system_call(f'python -c "from math import *;print({instr})"')[0].decode().strip())
    
            print(output)
            if(output == max_no+1):
                if(max_no > highscore):
                    highscore = max_no
                    try:
                        cardno = highscore+1
                        embed=discord.Embed(title="Number fact", description=" ", color=0xf461ff)
                        embed.add_field(name=int(cardno), value=numfact[f'{int(cardno)}'], inline=False)
                        embed.set_footer(text="from Wikipedia")
                        await message.channel.send(embed=embed)
                    except KeyError:
                        pass
                max_no += 1
                num_file=open('number.number',mode="w", encoding="utf-8")
                num_file.write(str(max_no))
                num_file.close()

                if(max_no == 69 or max_no == 420 or max_no == 666):
                      await message.add_reaction('👀')

                await message.add_reaction('✅')

            else:
                await message.add_reaction('❎')
                await message.channel.send(f'**Wrong Number at {max_no}** by {message.author.mention} T_T')
                await message.channel.send(f'Start over from 1')
                embed=discord.Embed(description="Counting",color=0xff0000)
                embed.add_field(name="Failed at", value=int(max_no), inline=True)
                embed.add_field(name="Highscore", value=int(highscore), inline=True)
                embed.set_footer(text="Restart from 1")
                await message.channel.send(embed=embed)
                max_no = 0
                num_file=open('number.number',mode="w", encoding="utf-8")
                num_file.write(str(max_no))
                num_file.close()
        except ValueError:
            
            await message.channel.send(f'**Wrong Number at {max_no}** by {message.author.mention} T_T')
            await message.channel.send(f'Start over from 1')
            await message.add_reaction('❎')
            embed=discord.Embed(description="Counting",color=0xff0000)
            embed.add_field(name="Failed at", value=int(max_no), inline=True)
            embed.add_field(name="Highscore", value=int(highscore), inline=True)
            embed.set_footer(text="Restart from 1")
            await message.channel.send(embed=embed)
            max_no = 0

        

client.run('REM IS BAE')
