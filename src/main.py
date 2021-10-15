import os, sys
import discord
from discord.ext import commands

# Carregando o .env;
from dotenv import load_dotenv
load_dotenv()

# Criando as variáveis e constantes;
TOKEN = os.getenv("token")
COGS = ["cogs.admin"]
CANAIS = {
    "bv": 888196899897749555,
    "comandos": 888134154661810176,
    "verificar": 888197581786730526,
    "chatg": 888134082570108958,
    "sug": 891729339874443274
}
CARGOS = {
    "staff": 891526793360723978,
    "verificado": 888134846499676210
}

# Criando o BOT, setando as Intents e criando variáveis extras;
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
bot.canais = CANAIS
bot.cargos = CARGOS

@bot.event
async def on_ready():
    print("\n+ BOT Inicializado")
    print("\n\n------------------\n")

# Checando o canal correto;
@bot.event
async def on_message(message):
    # Pegando o cargo da STAFF;
    cargo = discord.utils.find(lambda r: r.id == bot.cargos["staff"], 
    bot.get_guild(888132590119305238).roles)
    
    # Verificando por mensagens no canal de sugestões;
    if message.channel.id == bot.canais["sug"] and  not message.author.bot:

        # Verificando se o membro tem o cargo de STAFF;
        if cargo in message.author.roles:
            return
            
        embed = discord.Embed(title=f"Nova sugestão de {message.author.name}!",
                                  description=f"{message.content}")
        embed.color = discord.Color.from_rgb(54, 57, 62)
        await message.channel.send(embed=embed)
        await message.delete()
    
    # Verificando o canal onde o comando foi executado;
    cmdCanal = bot.get_channel(bot.canais["comandos"])
    
    if message.content.lower().startswith('.'):
        if message.channel.id == cmdCanal.id or cargo in message.author.roles or message.channel.id == bot.canais["verificar"]:
            # Comando no canal correto;
            await bot.process_commands(message)
        else:
            # Comando no canal errado;
            await message.channel.send(':x: | {}, você não pode usar este comando aqui! Use o em {}!'
                                       .format(message.author.mention, cmdCanal.mention))

# Error handler GLOBAL;
@bot.event
async def on_command_error(ctx, error):

        # Não deixa erros em comandos que tenham handlers locais chegarem ao global.
        if hasattr(ctx.command, 'on_error'):
            return

        # Não deixa erros em cogs com handlers locais chegarem ao global.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = ()

        # Pegando o erro original.
        error = getattr(error, 'original', error)

        # Ignorando os erros ignorados.
        if isinstance(error, ignored):
            return
        
        # Comando não existe.
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.author.mention}, esse comando não existe!")

        # Comando desabilitado.
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.author.mention}, esse comando está desabilitado.')

        # Comando sem uso na DM.
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.author.mention}, esse comando não pode ser usado na DM.')
            except discord.HTTPException:
                pass

        else:
            # Erro não reconhecido acima, mandando ao console.
            print('\n+ Ignorando exceção no comando {}!'.format(ctx.command))

# Carregando as COGs;
print("\n- Iniciando carregamento das COGs.")
for cog in COGS:
    try:
        bot.load_extension(cog)
        print(f"\n+ A COG {cog} foi iniciada com sucesso.")
    except Exception as e:
        print("\n+ Erro ao tentar carregar a COG {cog}.")
        print(f"\n{e}")
        pass
print("\n- Carregamento das COGs concluído!")

print("\n- Inicializando o BOT...")
bot.run(TOKEN)






