import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix=')', intents = intents)
from env import TOKEN


#signing in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{client.command_prefix}h'))


#main
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)



@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms :)')


#help
@client.command(aliases=['h'])
async def get_help(ctx):
    embed = discord.Embed(title="Help", description=f'Prefix: `{client.command_prefix}`', color=0xb2558d)
    embed.add_field(name=f"`{client.command_prefix}ping` (aka `p`)", 
            value="Performs a ping to see if the bot is up.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}list`', 
            value="Lists each role and everyone in them.", inline=False)
    embed.add_field(name=f'`{client.command_prefix}find foo`',
            value="Prints a list of everyone with role `foo`.", inline=False)
    embed.set_footer(text="Contact @radix#4520 with issues.")
    await ctx.send(embed=embed)



@client.command(aliases=['list'])
async def list_all_roles(ctx,*args):
    ALL_ROLES = {}

    #populate ALL_ROLES
    for m in ctx.guild.members:
        for role in m.roles:
            if role.name != "@everyone":
                if ALL_ROLES.__contains__(role.name):
                    ALL_ROLES[role.name].append(f'`{m.name}#{m.discriminator}`')
                else:
                    ALL_ROLES[role.name] = [f'`{m.name}#{m.discriminator}`']
    
    for role in ALL_ROLES:
        long_list = f'**{role}**: {", ".join(ALL_ROLES[role])}\n'
        if len(long_list) < 2000:
            await ctx.send(long_list)
        else: 
            parts = []
            for i in range(0, len(long_list), 1000):
                parts.append(long_list[i:i+1000])
            if len(parts) > 3:
                await ctx.send(f'(**{role}** has too many people in it to list)')
            else:
                for part in parts:
                    await ctx.send(part)
    return


@client.command(aliases=['find'])
async def find_people_with_role(ctx,*,role): 
    real_roles = []
    for real_role in ctx.guild.roles:
        real_roles.append(real_role.name)
    if role not in real_roles:
        return await ctx.send("That role does not exist!")
    
    people_in_role = []
    for m in ctx.guild.members:
        member_specific_roles = []
        for r in m.roles:
            member_specific_roles.append(r.name)
        if role in member_specific_roles: 
            people_in_role.append(f'`{m.name}#{m.discriminator}`')
    
    if not people_in_role:
        return await ctx.send(f'No one with that role!')
    
    long_list = f'People with role `{role}`:\n'
    for person in people_in_role:
        long_list += f'{person}\n'
    parts = []
    for i in range(0, len(long_list)-1, 1900):
        temp = long_list[i:i+1900].rindex("\n")
        try:
            await ctx.send(long_list[i:temp])
        except:
            print(f'Failed to ctx.send: {long_list[i:temp]}')
    return


client.run(TOKEN)