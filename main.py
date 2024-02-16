"""VSBot"""

from webser import keep_alive
import os
import discord
from discord.ext import commands
from discord import Webhook
import asyncio

keep_alive()
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix="!")
channel1IDS = 1106250814865027184

token = os.env[TOKEN]
status1 = 'модератора'
status2 = 'личные сообщения'

prefix = [
    "!", "<@848526366831804457>", "<@!848526366831804457>",
    "<@848526366831804457> ", "<@!848526366831804457> "
]


class ServerApplication(discord.ui.Modal):

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    username = discord.ui.InputText(label="Никнейм",
                                    placeholder="Ваш внутриигровой никнейм.",
                                    required=True,
                                    style=discord.InputTextStyle.short)
    age = discord.ui.InputText(
        label="Возраст",
        placeholder="Ваш возраст (необязательно, но желательно).",
        required=False,
        style=discord.InputTextStyle.short)
    hobby = discord.ui.InputText(
        label="Занятие",
        placeholder="Чем вы будете заниматься на сервере?",
        required=True,
        style=discord.InputTextStyle.paragraph)
    self.add_item(username)
    self.add_item(age)
    self.add_item(hobby)

  async def callback(self, interaction: discord.Interaction):
    embed = discord.Embed(title=f"Заявка от {interaction.user.display_name}")
    embed.add_field(name="Ник", value=self.children[0].value)
    embed.add_field(name="Возраст", value=self.children[1].value)
    embed.add_field(name="Занятие", value=self.children[2].value)
    channel = client.get_channel(1124798042273497200)

    await interaction.response.send_message(
        "Спасибо! Мы рассмотрим вашу заявку в течении 24 часов.",
        ephemeral=True)
    await channel.send(embed=embed)


class CoolButton(
    discord.ui.View
):  # Create a class called MyView that subclasses discord.ui.View

  @discord.ui.button(
      label="Получить доступ", style=discord.ButtonStyle.primary, emoji="✅"
  )  # Create a button with the label "😎 Click me!" with color Blurple
  async def button_callback(self, button, inter: discord.ApplicationContext):
    modal = ServerApplication(title="Заявка на Vanilla Spoon")
    await inter.response.send_modal(modal=modal)


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=status1))
  print(f'Logged in as {client.user.name}')
  asyncio.ensure_future(change_status())


async def change_status():
  while True:
    await client.change_presence(activity=discord.Game(name=status1))
    await asyncio.sleep(15)
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=status2))
    await asyncio.sleep(15)


@client.event
async def on_member_join(member):
  try:
    dm_channel = await member.create_dm()
    await dm_channel.send(embed=discord.Embed(
        title="Добро пожаловать на Vanilla Spoon!",
        description=
        'Если вы хотите играть на сервере, то вам нужно будет написать небольшую заявку:\n\n1. Ваш внутриигровой ник (С которого вы будете заходить на сервер)\n2. Ваш возраст\n3. Чем вы будете заниматься на сервере\n4. Вы прочитали и согласны с правилами?',
        color=discord.Color.blue()).set_footer(
            text="Если у вас будут вопросы, пишите их сюда!"))
  except discord.errors.Forbidden:
    print(f"Cannot send a DM to {member.name}")


@client.event
async def on_member_remove(member):
  try:
    dm_channel = await member.create_dm()
    await dm_channel.send(embed=discord.Embed(
        description=
        f'Здравствуйте {member.mention}! Администрации Vanilla Spoon стала интересна причина того что вы покинули наш сервер. Мы постараемя исправить проблему если она есть!',
        color=discord.Color.blue()))
  except discord.errors.Forbidden:
    print(f"Cannot send a DM to {member.name}")


@client.slash_command(name='ответ', description='Отправить ответ пользователю')
@client.slash_command(name='answer', description='Send answer to user')
@commands.has_role(1124787276061348010)
@commands.has_role(1124787746284765365)
@commands.has_role(1124791899501375508)
async def answer(ctx, user: discord.User, message: str = None):
  ttl = "Ваше сообщение приняли. Ждите ответ"
  if message is not None:
    ttl = message
  embed = discord.Embed(title=ttl, color=discord.Color.green())
  await user.send(embed=embed)
  await ctx.respond("\U0001F44D Команда успешно выполнена", ephemeral=True)


@client.slash_command(name='обомне', description='Описание бота')
@client.slash_command(name='aboutme', description='Bot description [RU]')
async def about_me(ctx):
  embed = discord.Embed(
      description=
      "Я бот созданный для помощи игрокам Vanilla Spoon. Если вы хотите задать приватный вопрос модерации, то вы можете написать мне в лс и в скором времени вам ответят",
      color=discord.Color.blue())
  await ctx.respond(embed=embed)


@client.slash_command(name="новость",
                      description="Написать новость через вебхук и эмбед")
@client.slash_command(name="news",
                      description="Send news with webhook and embed")
@commands.has_role(1124787276061348010)
@commands.has_role(1124787746284765365)
@commands.has_role(1124791899501375508)
async def send_news(ctx,
                    title: str,
                    description: str,
                    color: discord.Color = discord.Color.blue(),
                    url: str = None,
                    thumbnailurl: str = None,
                    footertext: str = None,
                    footerimageurl: str = None):
  webhook_url = "https://discordapp.com/api/webhooks/1125786446888980501/RvN02K3R4Euv1Db0YN1jlDpp9rsCEL4YefJVewyEqTx2dht8FUAOKH_LgO5y_Ma1DrRw"

  # Создание вебхука
  webhook = Webhook.from_url(webhook_url, session=aiohttp.ClientSession())

  # Создание встроенного сообщения (embed)
  embed = discord.Embed(title=title, description=description, color=color)

  if url is not None:
    embed.url = url
  if thumbnailurl is not None:
    embed.set_thumbnail(url=thumbnailurl)
  if footertext is not None:
    if footerimageurl is not None:
      embed.set_footer(text=footertext, icon_url=footerimageurl)
    else:
      embed.set_footer(text=footertext)
  else:
    if footerimageurl is not None:
      embed.set_footer(icon_url=footerimageurl)

  # Отправка встроенного сообщения через вебхук
  await webhook.send(embed=embed)

  await ctx.respond("\U0001F44D Новость отправлена через вебхук",
                    ephemeral=True)


@client.slash_command(name='опрос', description='Создать опрос')
@client.slash_command(name='poll', description='Create poll')
@commands.has_role(1124787276061348010)
@commands.has_role(1124787746284765365)
@commands.has_role(1124791899501375508)
async def create_poll(ctx, question: str, answ: str, time: str):
  answers = answ.split(', ')
  embed = discord.Embed(title=question, color=discord.Color.blue())
  embed.set_footer(text="Окончание через " + time)

  for index, answer in enumerate(answers, start=1):
    embed.add_field(name="", value=answer, inline=False)

  poll_message = await ctx.send(embed=embed)
  thread = await poll_message.create_thread(name="Вопросы/предложения")
  await thread.send("Пишите сюда свои вопросы/предложения")

  time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
  time_value = int(time[:-1])
  time_multiplier = time[-1]
  time_seconds = time_value * time_units.get(time_multiplier, 1)

  await ctx.respond("\U0001F44D Команда успешно выполнена", ephemeral=True)
  await asyncio.sleep(time_seconds)  # Ожидание указанного времени

  embed.set_footer(text="Опрос окончен")
  await poll_message.edit(embed=embed)

  await ctx.author.send(
      embed=discord.Embed(title="Опрос окончен, подведи результаты :wink:",
                          color=discord.Color.blue()))


@client.slash_command(name='пинг', description='Понг!')
@client.slash_command(name='ping', description='Pong!')
async def ping(ctx):
  emb = discord.Embed(
      title="Понг! \U0001F3D3",
      description=f'Текущий пинг бота: {round(client.latency * 1000)}мс',
      color=discord.Color.blue())
  await ctx.respond(embed=emb)


@client.event
async def on_message(message):
  if message.content == "lorem lorem amen":
    embed = discord.Embed(
        color=discord.Color.blue(),
        title="Доступ к серверу",
        description=
        "Чтобы получить доступ к серверу, нужно нажать на кнопку снизу и заполнить все необходимые поля."
    )
    await client.get_channel(1124784820451549215).send(embed=embed,
                                                       view=CoolButton())
  if isinstance(message.channel, discord.DMChannel):
    channel = client.get_channel(
        1124798042273497200
    )  # замените 1234567890 на ID канала, куда вы хотите отправлять логи личных сообщений
    if message.author != client.user:
      author = message.author
      if message.author.discriminator == "0":
        author = message.author.name
      await channel.send(f"**{author}**: {message.content}")

    # отправка автоматического сообщения, если пользователь не пишет в личном чате бота в течение 5 секунд
    try:
      await client.wait_for('message',
                            timeout=5.0,
                            check=lambda m: m.author == message.author and
                            isinstance(m.channel, discord.DMChannel))
    except asyncio.TimeoutError:
      if message.author == client.user:
        return
      reply = "Хорошо! Скоро с вами свяжется модерация или администрация."
      await message.reply(
          embed=discord.Embed(title=reply, color=discord.Color.green()))


client.run(token)
