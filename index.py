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
    for m in ctx.guild.members:
        name_to_use = f'Name: `{m.name}#{m.discriminator}`' 
        if m.nick:
            name_to_use += f'(or {m.nick})'
        
        for role in m.roles:
            if role.name != "@everyone":
                if ALL_ROLES.__contains__(role.name):
                    ALL_ROLES[role.name].append(f'{m.name}#{m.discriminator}')
                else:
                    ALL_ROLES[role.name] = [f'{m.name}#{m.discriminator}']
    
    to_return = ""
    for role in ALL_ROLES:
        if len(to_return) < 1000:
            to_return += f'**{role}**: {", ".join(ALL_ROLES[role])}\n'
        else:
            await ctx.send(to_return)
            to_return = ""
    return await ctx.send(to_return)


@client.command(aliases=['find'])
async def find_people_with_role(ctx,*,role): 
    ALL_ROLES = []
    for real_role in ctx.guild.roles:
        ALL_ROLES.append(real_role.name)
    if role not in ALL_ROLES:
        return await ctx.send("That role does not exist!")
    
    people_in_role = []
    for m in ctx.guild.members:
        member_specific_roles = []
        for r in m.roles:
            member_specific_roles.append(r.name)

        if role in member_specific_roles: 
            people_in_role.append(f'`{m.name}#{m.discriminator}`')
    
    if not people_in_role:
        to_return = f'No one with that role!'
    else:
        to_return = f'People with role `{role}`: \n'
        for person in people_in_role:
            if len(to_return) < 1000:
                to_return += f'{person}\n'
            else:
                await ctx.send(to_return)
                to_return = ""
    return await ctx.send(to_return)


client.run(TOKEN)