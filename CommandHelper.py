from Poll import Poll
import discord
import re

ongoing_polls = {}


async def get_message(message):
    return re.search("\\s(.*)", message).group().lstrip()


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

        print(f"categories list: {categories_list}")

        poll = Poll(categories_list, title)
        ongoing_polls[title] = poll
        return title

    except Exception:
        await ctx.send(
            'Error: Incorrect syntax, remember to use: '
            '\n!poll <title>: <categories>, <separated>, <by>, <commas>')


async def submit_vote(ctx, message):
    """
    Add a vote to the poll, if the poll exists
    :param ctx:
    :param message:
    :return:
    """
    voted = False

    for poll in ongoing_polls:
        if message in ongoing_polls[poll].cat_dict.keys():
            if ongoing_polls[poll].did_vote(ctx.author.id):
                await ctx.send(f"{ctx.author}, you have already voted in {poll}")
                return

            voted = True
            update_ongoing_polls(ongoing_polls[poll], message, ctx.author.id, add_vote=True)
            await ctx.send(f"{ctx.author}, vote added to {ongoing_polls[poll].title}: {message}")
    if voted is False:
        await ctx.send(f"{message} not a category in any poll")


def update_ongoing_polls(poll, message=None, author=None, add_vote=False):
    """
    Update the poll with new input
    :param poll:
    :param message:
    :param author:
    :param add_vote:
    :return:
    """
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
    """
    Create an image of a poll and display it in the chat
    :param ctx:
    :param poll:
    :return:
    """
    if poll in ongoing_polls.keys():
        print('poll exists')
        ongoing_polls[poll].pie_votes()
        await ctx.send(file=discord.File('poll.png'))
        await purge_poll(poll)
    else:
        await ctx.send(f"{poll} does not exist")


async def purge_poll(poll):
    """
    Remove a poll from the current ongoing_polls list
    :param poll:
    :return:
    """
    try:
        del ongoing_polls[poll]
    except KeyError:
        print(f"[INFO] Error deleting {poll} from ongoing polls")


async def show_ongoing_polls(ctx):
    """
    Send a list of the ongoing polls in the chat
    :param ctx:
    :return:
    """
    if ongoing_polls:
        await ctx.send("Ongoing polls: ")
        ongoing_list = [poll for poll in ongoing_polls]
        ongoing = '\n'.join(ongoing_list)
        await ctx.send(f"{ongoing}")

    else:
        await ctx.send(f"{ctx.author}, there are no ongoing polls")


async def save_poll(ctx):
    """
    Save a when the bot goes offline.
    :param ctx:
    :return:
    """
    # TODO: implement saving
    pass
