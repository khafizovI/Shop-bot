🛍 Shop Bot
Bu Shop Bot – Aiogram 3 va Tortoise-ORM asosida yaratilgan Telegram do‘kon botidir. Bot orqali foydalanuvchilar mahsulotlarni ko‘rish, buyurtma qilish va ma’murlar esa mahsulotlarni boshqarishlari mumkin.

🚀 Xususiyatlar
✅ Foydalanuvchilar uchun:

Mahsulotlarni ko‘rish
Har bir mahsulot uchun rasm, tavsif va narx
"Sotib olish" tugmasi orqali buyurtma berish
"Mening buyurtmalarim" bo‘limi
✅ Ma’murlar uchun:

Token bilan Admin_id ni ozgartiring!!!!!

Mahsulot qo‘shish (nomi, tavsifi, narxi va rasmi bilan)
Yangi buyurtmalarni kuzatish
Barcha mahsulotlarni boshqarish
🛠 O‘rnatish
Loyihani ishga tushirish uchun quyidagi qadamlarni bajaring:

Repositoryni yuklab oling

git clone https://github.com/khafizovI/shop-bot.git
cd shop-bot
Virtual muhit yaratish va aktivlashtirish

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
Kerakli kutubxonalarni o‘rnatish

pip install -r requirements.txt
.env faylini yaratish va sozlash .env fayliga bot tokeni va PostgreSQL bazasiga ulanish ma’lumotlarini kiriting:

BOT_TOKEN="1234567890:ABCDEFGHJKLMNOPQRSTUVWXYZ"
DB_URL="postgres://user:password@localhost:5432/shopbot_db"
Ma’lumotlar bazasini ishga tushirish

alembic upgrade head  # Agar Alembic ishlatilsa
yoki

python database.py  # Agar Tortoise-ORM ishlatilsa
Botni ishga tushirish

python main.py
🎛 Foydalanish
🔹 Foydalanuvchilar uchun buyruqlar:

/start – Botni ishga tushirish
🔹 Ma’murlar uchun buyruqlar:

/admin – Yangi mahsulot qo‘shish
/products – Barcha buyurtmalarni ko‘rish
🛡 Texnologiyalar
Aiogram 3 – Telegram bot uchun asinxron framework
Tortoise-ORM – Ma’lumotlar bazasi bilan ishlash uchun ORM
PostgreSQL – Ma’lumotlar bazasi
Docker – Loyihani konteynerlash (agar kerak bo‘lsa)
📌 Muallif
👤 Ismingiz – [https://github.com/khafizovI]

Loyihaga hissa qo‘shmoqchimisiz? Bemalol PR (Pull Request) oching yoki muammolar bo‘lsa Issues bo‘limida xabar qoldiring! 😊
