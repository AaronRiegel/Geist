from setup import token, greetings
from discord.ext import commands
import CommandHelper
import random

description = '''Geist: the ghost bot who will helpfully haunt my discord'''
bot = commands.Bot(command_prefix='!', description=description)
polls = []


@bot.event
async def on_ready():
    print(f'[INFO] Bot session started as {bot.user.name}')
    print(f'---------------------------------------------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def hello(ctx):
    """Bot will return a greeting."""
    greeting = random.choice(greetings)

    if type(greeting) is tuple:
        await ctx.send(f'{greeting[0]} {ctx.author}{greeting[1]}')
    else:
        await ctx.send(f'{greeting} {ctx.author}')


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def poll(ctx):
    """Create a poll.
    !poll <title>:<categories>,<separated>,<by>,<commas>
    """
    if ':' in ctx.message.content:
        new_poll_title = await CommandHelper.create_poll(ctx, ctx.message.content)
        await ctx.send(f"Created {new_poll_title}")
    else:
        await ctx.send('no')


@bot.command()
async def endpoll(ctx):
    """
    End a poll.
    !endpoll <title>
    :return:
    """
    message = await CommandHelper.get_message(ctx.message.content, '!endpoll')
    print(f'{message}')
    await CommandHelper.show_pie_plt(ctx, message)


@bot.command()
async def vote(ctx):
    """
    !vote <category> to vote
    :param ctx:
    :return:
    """
    message = await CommandHelper.get_message(ctx.message.content, '!vote')
    await CommandHelper.submit_vote(ctx, message)


@bot.command()
async def lst(ctx):
    """
    !lst shows all current ongoing polls
    :param ctx:
    :return:
    """
    await CommandHelper.show_ongoing_polls(ctx)


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.invoked_subcommand} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('No, but it is spooky.')


@cool.command(name='Phelot')
async def _phelot(ctx):
    """Is Phelot cool?"""
    await ctx.send('Don\'t test my patience.')


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def shutdown(ctx):
    """
    Only possible by guild owner
    """
    if ctx.author.id is not ctx.guild.owner.id:
        await ctx.send(f'YOU ARE NOT AUTHORIZED {ctx.author}, THE {bot.user.name} TRAIN KEEPS GOING!')
    else:
        print("terminating bot...")
        await ctx.send("Goodbye, for now")
        await bot.close()
        print("bot terminated")


@bot.command()
async def nuke(ctx):
    """
    Under construction
    """
    if ctx.author.id is not ctx.guild.owner.id:
        await ctx.send(f'no u')
    else:
        await ctx.send(f'no u')

bot.run(token)

