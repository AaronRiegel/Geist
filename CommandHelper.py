from Poll import Poll
import discord

ongoing_polls = {}


async def create_poll(ctx, message):
    """
    form !poll <title>: <args>, <separated>, <by>, <commas>
    :return:
    """
    try:
        split_args = message.split(':')
        title = str(split_args[0][5:].lstrip())
        print(f"title: {title}")
        categories = split_args[1].split(',')
        print(f"categories: {categories}")

        categories_list = list(map(lambda x: x.strip(' '), categories))

        poll = Poll(categories_list, title)
        ongoing_polls[title] = poll
        return title

    except Exception:
        await ctx.send(
            'Error: Incorrect syntax, remember to use: '
            '\n!poll <title>: <categories>, <separated>, <by>, <commas>')


async def submit_vote(ctx, message):
    voted = False

    for poll in ongoing_polls:
        if message in ongoing_polls[poll].cat_dict.keys():
            if ctx.author.id in ongoing_polls:
                await ctx.send(f"{ctx.author}, you have alread voted in {poll}")
                return

            voted = True
            update_ongoing_polls(ongoing_polls[poll], message, ctx.author.id, add_vote=True)
            await ctx.send(f"{ctx.author}, vote added to {ongoing_polls[poll].title}: {message}")
    if voted is False:
        await ctx.send(f"{message} not a category in any poll")


def update_ongoing_polls(poll, message=None, author=None, add_vote=False):
    if add_vote:
        try:
            poll.add_vote(message)
            poll.user_voted(author)
            ongoing_polls[poll.title] = poll
        except Exception:
            print("No author provided")
    else:
        ongoing_polls[poll.title] = poll


async def show_pie_plt(ctx, poll):
    if poll in ongoing_polls.keys():
        print('poll exists')
        ongoing_polls[poll].pie_votes()
    await ctx.send(file=discord.File('poll.png'))

async def purge_poll(ctx, poll):
    pass

async def save_poll(ctx):
    pass