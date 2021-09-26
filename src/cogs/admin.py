import os, sys
import discord
from discord.ext import commands
from discord.utils import get

# Inicializando o .env;
from dotenv import load_dotenv
load_dotenv()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx):
        await ctx.send(ctx.message.content[4:])

    # Membro Entrou
    @commands.Cog.listener()
    async def on_member_join(self, membro):
        pfp = membro.avatar_url
        
        vEmbed = discord.Embed(title=":wave: | Novo membro!",
                               description=f"Seja bem-vindo(a) {membro.mention} ao Python Brasil!",
                               color=discord.Color.from_rgb(54, 57, 62))
        vEmbed.set_image(url=pfp)
        
        await self.bot.get_channel(self.bot.canais["bv"]).send(embed=vEmbed)

    # Membro Saiu
    @commands.Cog.listener()
    async def on_member_remove(self, membro):
        pfp = membro.avatar_url
        
        vEmbed = discord.Embed(title=":wave: | Membro saiu!",
                               description=f"Adeus **{membro.name}**, sentiremos sua falta!",
                               color=discord.Color.from_rgb(54, 57, 62))
        # Esse truque não funciona quando o membro não está no server! (Obviamente lol);
        #vEmbed.set_image(url=pfp)
        
        await self.bot.get_channel(self.bot.canais["bv"]).send(embed=vEmbed)

    @commands.command()
    async def verificar(self, ctx):
        if ctx.channel.id == self.bot.canais["verificar"]:
            # Adicionando o cargo e deletando a mensagem;
            cargo = get(ctx.guild.roles, id=self.bot.cargos["verificado"])
            await ctx.author.add_roles(cargo)
            await ctx.message.delete()
            
            # Mensagem no chat geral;
            chan = self.bot.get_channel(self.bot.canais["chatg"])
            await chan.send(f":white_check_mark: | {ctx.author.mention} foi verificado(a)!")

            # Mensagem no privado;
            try:
                await ctx.author.send(":white_check_mark: | Você foi **verificado(a)**! Aproveite o acesso ao server!")
            except:
                pass

def setup(bot):
    bot.add_cog(Admin(bot))
