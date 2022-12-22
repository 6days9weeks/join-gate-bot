"""Join gate cog file."""
import time
import discord # pylint: disable=import-error
from discord.ext import vbu  # pylint: disable=import-error
from utils import (  # pylint: disable=import-error
    send_staff_info,
    fetch_default_join_amount,
    fetch_default_delay,
    fetch_role,
    fetch_staff,
    fetch_log_channel,
)


class JoinGate(vbu.Cog[vbu.Bot]):
    """Join gate cog."""

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.bot = bot
        self.enabled_guilds = set()
        self.cached_time = {}
        self.cached_join_amounts = {}
        self.cached_default_amounts = {}
        self.cached_default_delays = {}
        self.triggered = {}

    @vbu.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """On member join."""
        if member.guild.id not in self.enabled_guilds:
            return
        if member.bot:
            return
        if self.triggered.get(member.guild.id) and time.time() - self.triggered[
            member.guild.id
        ] < 600:
            role = await fetch_role(member.guild)
            staff = await fetch_staff(member.guild)
            channel = await fetch_log_channel(member.guild)
            await member.add_roles(role)
            await send_staff_info(member.guild, member, staff, channel)
        else:
            if not self.cached_join_amounts.get(member.guild.id):
                self.cached_join_amounts[member.guild.id] = 0
            self.cached_join_amounts[member.guild.id] += 1
            if not self.cached_default_amounts.get(member.guild.id):
                self.cached_default_amounts[member.guild.id] = await fetch_default_join_amount(
                    member.guild.id
                )
            if not self.cached_default_delays.get(member.guild.id):
                self.cached_default_delays[member.guild.id] = await fetch_default_delay(
                    member.guild.id
                )
            if not self.cached_time.get(member.guild.id):
                self.cached_time[member.guild.id] = time.time()
            if (
                time.time() - self.cached_time[member.guild.id]
                > self.cached_default_delays[member.guild.id]
            ):
                self.cached_time[member.guild.id] = time.time()
                self.cached_join_amounts[member.guild.id] = 0
            if (
                self.cached_join_amounts[member.guild.id]
                < self.cached_default_amounts[member.guild.id]
            ):
                return
            self.triggered[member.guild.id] = time.time()
        # check if triggered is less than 10 minutes ago and if so, work
            if time.time() - self.triggered[member.guild.id] < 600:
                role = await fetch_role(member.guild)
                staff = await fetch_staff(member.guild)
                channel = await fetch_log_channel(member.guild)
                await member.add_roles(role)
                await send_staff_info(member.guild, member, staff, channel)


def setup(bot: vbu.Bot):
    """Join gate cog load."""
    x = JoinGate(bot)  # pylint: disable=invalid-name
    bot.add_cog(x)
