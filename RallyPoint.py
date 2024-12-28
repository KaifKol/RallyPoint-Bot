import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
load_dotenv() 

bot = commands.Bot(command_prefix="!", sync_commands_debug=True)


#TODO Modal

class Status(disnake.ui.Modal):
    def __init__(self):
        status = disnake.ui.TextInput(
            label="Статус",
            placeholder="писать через строку (как обычно) форматирование сделаеться само",
            custom_id="status",
            style=disnake.TextInputStyle.long
        )

        host = disnake.ui.TextInput(
            label="Хост",
            placeholder="",
            custom_id="host",
            style=disnake.TextInputStyle.short
        )

        super().__init__(
            title="Статус",
            custom_id="status4ik",
            components=[status, host],
        )

    async def callback(self, inter: disnake.ModalInteraction):
        status1 = inter.text_values["status"]
        host1 = inter.text_values["host"]
        
        description = (
            "---------------------\n"
            # "# СТАТУС\n"
            f"```{status1}```\n"
            "---------------------\n"
            f"Хост - {host1}\n"
            "---------------------"
        )

        embed = disnake.Embed(
            title="СТАТУС", 
            description=description, 
            color=0x3eff00
        )
    

        await inter.response.send_message(embed=embed) 

class Gymes(disnake.ui.Modal):
    def __init__(self):
        author = disnake.ui.TextInput(
            label="Автор",
            placeholder="пиши",
            custom_id="author",
            style=disnake.TextInputStyle.short,
        )

        data = disnake.ui.TextInput(
            label="Дата проведения сценария",
            placeholder="пиши",
            custom_id="data",
            style=disnake.TextInputStyle.long,
        )

        mode = disnake.ui.TextInput(
            label="Мод",
            placeholder="пиши",
            custom_id="mode",
            style=disnake.TextInputStyle.long
        )

        briefeng = disnake.ui.TextInput(
            label="Брифинг",
            placeholder="пиши",
            custom_id="briefeng",
            style=disnake.TextInputStyle.long
        )

        super().__init__(
            title="Обьявления игры",
            custom_id="anonse_game",
            components=[data, author, mode, briefeng],
        )

    async def callback(self, inter: disnake.ModalInteraction):
        data1 = inter.text_values["data"]
        author1 = inter.text_values["author"]
        mode1 = inter.text_values["mode"]
        briefeng1 = inter.text_values["briefeng"]

        description = (
            "---------------------\n"
            f"{mode1}\n"
            "---------------------\n"
            f"{briefeng1}\n"
            "---------------------"
        )

        embed = disnake.Embed(
            title=data1,
            description=description,
            color=0x00f7ff
        )

        embed.set_author(name=f"Автор сценария <<{author1}>>")

        message = await inter.response.send_message(embed=embed)

        await self.vetka(message)

    async def vetka(self, message):
        await message.create_thread(
            name="Бронирование",
            auto_archive_duration=60,
        )


#---


#TODO on ready

@bot.event
async def on_ready():
    print("Бот готов!")

    activity = disnake.Activity(
        name="RallyPoint",
        type=disnake.ActivityType.playing,
    )
    await bot.change_presence(status=disnake.Status.idle, activity=activity)


#TODO slash commands
        
@bot.slash_command(

    name="игра",
    description="Информация о игре"
)
async def games(inter: disnake.AppCmdInter):
    await inter.response.send_modal(modal=Gymes())

@bot.slash_command(
    name="статус",
    description="Статус"
)
async def status(inter: disnake.AppCmdInter):
    await inter.response.send_modal(modal=Status())

@bot.slash_command(
    name="ping",
    description="Возращает задержку бота",
)
async def ping(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message("Понг!")


#---


bot.run(os.getenv("DISCORD_TOKEN"))