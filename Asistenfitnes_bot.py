import telebot

TOKEN = '7802743141:AAGNqfxc5vFNYkN21DN4V_HFGqz7jNhdCPc'
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def mulai(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    bot.send_message(user_id, "Halo! Saya bot makro nutrisi. Yuk mulai! Berapa berat badan kamu (kg)?")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'berat' not in user_data[m.chat.id])
def tanya_berat(message):
    user_id = message.chat.id
    try:
        berat = float(message.text)
        user_data[user_id]['berat'] = berat
        bot.send_message(user_id, "Berapa tinggi badan kamu (cm)?")
    except:
        bot.send_message(user_id, "Tolong masukkan angka yang benar untuk berat badan.")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'tinggi' not in user_data[m.chat.id])
def tanya_tinggi(message):
    user_id = message.chat.id
    try:
        tinggi = float(message.text)
        user_data[user_id]['tinggi'] = tinggi
        bot.send_message(user_id, "Berapa umur kamu?")
    except:
        bot.send_message(user_id, "Tolong masukkan angka yang benar untuk tinggi badan.")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'umur' not in user_data[m.chat.id])
def tanya_umur(message):
    user_id = message.chat.id
    try:
        umur = int(message.text)
        user_data[user_id]['umur'] = umur
        bot.send_message(user_id, "Jenis kelamin kamu? (pria/wanita)")
    except:
        bot.send_message(user_id, "Tolong masukkan angka yang benar untuk umur.")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'gender' not in user_data[m.chat.id])
def tanya_gender(message):
    user_id = message.chat.id
    gender = message.text.lower()
    if gender in ['pria', 'wanita']:
        user_data[user_id]['gender'] = gender
        bot.send_message(user_id, "Tujuan kamu apa? (bulking/cutting/maintenance)")
    else:
        bot.send_message(user_id, "Tulis 'pria' atau 'wanita' ya.")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'tujuan' not in user_data[m.chat.id])
def tanya_tujuan(message):
    user_id = message.chat.id
    tujuan = message.text.lower()
    if tujuan in ['bulking', 'cutting', 'maintenance']:
        user_data[user_id]['tujuan'] = tujuan
        hitung_dan_kirim(user_id)
    else:
        bot.send_message(user_id, "Tulis 'bulking', 'cutting', atau 'maintenance' ya.")

def hitung_dan_kirim(user_id):
    data = user_data[user_id]
    berat = data['berat']
    tinggi = data['tinggi']
    umur = data['umur']
    gender = data['gender']
    tujuan = data['tujuan']

    # Hitung BMR
    if gender == 'pria':
        bmr = 10 * berat + 6.25 * tinggi - 5 * umur + 5
    else:
        bmr = 10 * berat + 6.25 * tinggi - 5 * umur - 161

    kalori = bmr * 1.5  # aktivitas ringan

    if tujuan == 'bulking':
        kalori += 300
    elif tujuan == 'cutting':
        kalori -= 300

    # Makronutrien
    protein = (kalori * 0.3) / 4
    lemak = (kalori * 0.25) / 9
    karbo = (kalori * 0.45) / 4

    hasil = (
        f"Kebutuhan kalori harian kamu: {int(kalori)} kcal\n"
        f"Protein: {int(protein)} gram\n"
        f"Lemak: {int(lemak)} gram\n"
        f"Karbohidrat: {int(karbo)} gram"
    )

    # Tambahkan rekomendasi latihan
    if tujuan == 'bulking':
        rekomendasi = "Rekomendasi latihan: Fokus pada compound movement seperti squat, deadlift, bench press. Gunakan progressive overload."
    elif tujuan == 'cutting':
        rekomendasi = "Rekomendasi latihan: Lakukan latihan intensitas tinggi (HIIT), superset, dan volume tinggi."
    else:
        rekomendasi = "Rekomendasi latihan: Kombinasi latihan kekuatan dan kardio ringan."

    bot.send_message(user_id, hasil + "\n\n" + rekomendasi)

print("Bot makro nutrisi siap jalan...")
bot.polling()