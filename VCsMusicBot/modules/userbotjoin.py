from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from VCsMusicBot.helpers.decorators import authorized_users_only, errors
from VCsMusicBot.services.callsmusic.callsmusic import client as USER
from VCsMusicBot.config import SUDO_USERS

@Client.on_message(filters.command(["katil"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Önce beni grubunun yöneticisi olarak ekle</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "VCsMusicBot"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "İstediğiniz gibi buraya katıldım")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>sohbetinizde zaten yardımcı</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Taşan Bekleme Hatası 🛑 \n User {user.first_name} couldn't join your group due to heavy join requests for userbot! Make sure user is not banned in group."
            "\n\nVeya grubunuza el ile @sesmusicasistan ekleyin ve yeniden deneyin</b>",
        )
        return
    await message.reply_text(
        "<b>yardımcı userbot sohbetinize katıldı</b>",
    )


@USER.on_message(filters.group & filters.command(["ayril"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Kullanıcı grubunuzdan ayrılamadı! Floodwaits olabilir."
            "\n\nYa da beni manuel olarak grubunuza tekmelersiniz.</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Asistan Tüm sohbetleri bırakma")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Asistan ayrılıyor... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Asistan ayrılıyor... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Sohbet bile bağlantılı mı")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor channel first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "VCsMusicBot"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>helper already in your channel</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Taşan Bekleme Hatası 🛑 \n User {user.first_name} couldn't join your channel due to heavy join requests for userbot! Make sure user is not banned in channel."
            "\n\nVeya grubunuza el ile @sesmusicasistan ekleyin ve yeniden deneyin</b>",
        )
        return
    await message.reply_text(
        "<b>yardımcı userbot kanalınıza katıldı</b>",
    )
    
