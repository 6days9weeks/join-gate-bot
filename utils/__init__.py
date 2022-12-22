"""Utils for the cogs."""
from __future__ import annotations
import typing
import discord  # pylint: disable=import-error
from discord.ext import vbu  # pylint: disable=import-error


async def fetch_default_join_amount(guild_id: int) -> int:
    """Fetch the default join amount."""
    async with vbu.Database() as db:  # pylint: disable=invalid-name
        default_join_amount = await db(
            "SELECT default_amount FROM join_gate WHERE guild_id=$1", guild_id
        )
        if not default_join_amount:
            return 5
        return default_join_amount[0]["default_amount"]


async def fetch_default_delay(guild_id: int) -> int:
    """Fetch the default delay."""
    async with vbu.Database() as db:  # pylint: disable=invalid-name
        default_delay = await db("SELECT default_delay FROM join_gate WHERE guild_id=$1", guild_id)
        if not default_delay:
            return 5
        return default_delay[0]["default_delay"]


async def fetch_staff(guild: discord.Guild) -> discord.Role:
    """Fetch the staff role."""
    async with vbu.Database() as db:  # pylint: disable=invalid-name
        staff = await db("SELECT staff_role FROM join_gate WHERE guild_id=$1", guild.id)
        if not staff:
            return None
        return guild.get_role(staff[0]["staff_role"])


async def fetch_log_channel(guild: discord.Guild) -> discord.TextChannel:
    """Fetch the log channel."""
    async with vbu.Database() as db:  # pylint: disable=invalid-name
        log_channel = await db("SELECT channel FROM join_gate WHERE guild_id=$1", guild.id)
        if not log_channel:
            return None
        return guild.get_channel(log_channel[0]["channel"])


async def fetch_role(guild: discord.Guild) -> discord.Role:
    """Fetch a role."""
    async with vbu.Database() as db:  # pylint: disable=invalid-name
        role = await db("SELECT restrict_role FROM join_gate WHERE guild_id=$1", guild.id)
        if not role:
            return None
        return guild.get_role(role[0]["restrict_role"])


async def send_staff_info(
    guild: discord.Guild,
    user: typing.Union[discord.Member, discord.User],
    role: discord.Role,
    log_channel: discord.TextChannel,
) -> None:
    """Send staff info."""
    active_staff: typing.List[discord.Member] = []
    no_active_staff = False
    for m in role.members:
        if m.status != discord.Status.offline:
            active_staff.append(m)
    if not active_staff:
        active_staff = role.members
        no_active_staff = True
    embed = vbu.Embed(use_random_colour=True, timestamp=discord.utils.utcnow())
    embed.set_footer(f"Sent from {guild.name} ({guild.id})")
    embed.set_author_to_user(user)
    embed.description = f"You've been restricted from verifying in {guild.name} due to a high join amount. Please contact a staff member to verify."
    embed.add_field(
        name="Staff",
        value=", ".join([f"{m.mention} ({m.id})" for m in active_staff]),
        inline=False,
    )
    if no_active_staff:
        embed.add_field(
            name="Note",
            value="There are no active staff members, so you may have to wait a while for someone to respond.",
            inline=False,
        )
    could_sent = False
    try:
        await user.send(embed=embed)
        could_sent = True
    except discord.HTTPException:
        could_sent = False
    if could_sent:
        embed = vbu.Embed(use_random_colour=True, timestamp=discord.utils.utcnow())
        embed.set_author_to_user(user)
        embed.description = f"{user.mention} ({user.id}) has been sucessfully notified about their restriction from verifying in the server. A staff member should be contacted by them soon."
        await log_channel.send(embed=embed)
    else:
        embed = vbu.Embed(use_random_colour=True, timestamp=discord.utils.utcnow())
        embed.set_author_to_user(user)
        embed.description = f"{user.mention} ({user.id}) could not be notified about their restriction from verifying in the server. Please contact them manually."
        await log_channel.send(embed=embed)
