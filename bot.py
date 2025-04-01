from pyrogram import Client, filters
import os
import asyncio
from traceback import print_exc
from subprocess import PIPE, STDOUT
from time import time

api_id = os.environ['19383278']
api_hash = os.environ['6e6c8100d5564c59bfd82a7a86aadb95']
bot_token = os.environ['7732328266:AAGhxsBFyR0v_cKp5LvQ4Kx5U2-2W0mnIco']

app = Client('m3u8', api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command('start'))
async def start(_, message):
    await message.reply(f'''Kullanım: `/convert m3u8_link`
Github Repo: [Click to go.](https://github.com/lambda-stock/Telegram-m3u8-Converter/)
''')

@app.on_message(filters.command(['convert', 'cevir']))
async def convert(client, message):
    try:
        link = message.text.split(' ', 1)[1]
    except:
        print_exc()
        return await message.reply(f'''Kullanım: `/convert m3u8_link`
Github Repo: [Click to go.](https://github.com/lambda-stock/Telegram-m3u8-Converter/)
''')
    _info = await message.reply('Lütfen bekleyin...')
    filename = f'{message.from_user.id}_{int(time())}'
    proc = await asyncio.create_subprocess_shell(
        f'ffmpeg -i {link} -c copy -bsf:a aac_adtstoasc {filename}.mp4',
        stdout=PIPE,
        stderr=PIPE
    )
    await _info.edit("Dosya mp4'e çevriliyor...")
    out, err = await proc.communicate()
    await _info.edit('Dosya başarıyla çevrildi.')
    print('\n\n\n', out, err, sep='\n')
    try: 
        await _info.edit('Thumbnail ekleniyor...')
        proc2 = await asyncio.create_subprocess_shell(
            f'ffmpeg -i {filename}.mp4 -ss 00:00:30.000 -vframes 5 {filename}.jpg',
            stdout=PIPE,
            stderr=PIPE
        )
        await proc2.communicate()
        await _info.edit('Video süresi çekiliyor...')
        proc3 = await asyncio.create_subprocess_shell(
            f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filename}.mp4',
            stdout=PIPE,
            stderr=STDOUT
        )
        duration, _ = await proc3.communicate()
        await _info.edit('Telegrama yükleniyor...')

        await _info.edit("Dosya Telegram'a yükleniyor...")
        def progress(current, total):
            print(message.from_user.first_name, ' -> ', current, '/', total, sep='')
        await client.send_video(message.chat.id, f'{filename}.mp4', duration=int(duration.decode()), thumb=f'{filename}.jpg', caption = f'{filename}', progress=progress)
        os.remove(f'{filename}.mp4')
        os.remove(f'{filename}.jpg')
    except:
        print_exc()
        return await _info.edit('`Bir hata oluştu.`')


app.run()
