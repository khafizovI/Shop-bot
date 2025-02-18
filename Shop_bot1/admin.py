from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import Product
from buttons import admin_menu, main_menu
from aiogram.filters import Command
import random
from aiogram import Bot


ADMIN_ID = [5499596449, 802978542]

router = Router()

class AdminState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_desc = State()
    waiting_for_delete_id = State()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=admin_menu)
    else:
        await message.answer("❌ Siz admin emassiz!")

@router.message(F.text == "➕ Mahsulot qo‘shish")
async def admin_add_product(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await message.answer("🛍 Mahsulot rasmini yuboring:")
        await state.set_state(AdminState.waiting_for_photo)

@router.message(AdminState.waiting_for_photo, F.photo)
async def admin_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await message.answer("📌 Mahsulot nomini kiriting:")
    await state.set_state(AdminState.waiting_for_name)

@router.message(AdminState.waiting_for_name)
async def admin_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Mahsulot narxini kiriting:")
    await state.set_state(AdminState.waiting_for_price)

@router.message(AdminState.waiting_for_price)
async def admin_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Iltimos, faqat raqam kiriting.")
        return
    await state.update_data(price=int(message.text))
    await message.answer("ℹ️ Mahsulot tavsifini kiriting:")
    await state.set_state(AdminState.waiting_for_desc)

@router.message(AdminState.waiting_for_desc)
async def admin_desc(message: Message, state: FSMContext):
    data = await state.get_data()
    required_keys = ["name", "price", "photo"]
    for key in required_keys:
        if key not in data:
            await message.answer(f"❌ Xatolik: {key} mavjud emas. Iltimos, mahsulot qo‘shishni qayta boshlang.")
            await state.clear()
            return
    product_id = random.randint(1000, 9999)  # Generate a random product ID
    await Product.create(
        id=product_id,
        name=data["name"],
        price=data["price"],
        description=message.text,
        photo=data["photo"]
    )
    await message.answer(f"✅ Mahsulot qo‘shildi! ID: {product_id}", reply_markup=admin_menu)
    await state.clear()

@router.message(F.text == "🗑 Mahsulotni o‘chirish")
async def ask_product_id_for_deletion(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await message.answer("❌ O‘chirish uchun mahsulot ID sini kiriting:")
        await state.set_state(AdminState.waiting_for_delete_id)

@router.message(AdminState.waiting_for_delete_id)
async def delete_product_by_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Noto‘g‘ri ID. Iltimos, faqat raqam kiriting.")
        return
    product_id = int(message.text)
    product = await Product.get_or_none(id=product_id)
    if product:
        await product.delete()
        await message.answer(f"✅ Mahsulot o‘chirildi! ID: {product_id}")
    else:
        await message.answer("❌ Mahsulot topilmadi.")
    await state.clear()

@router.message(Command("products"))
async def list_all_products(message: Message):
    if message.from_user.id in ADMIN_ID:
        products = await Product.all()
        if not products:
            await message.answer("📭 Mahsulotlar ro‘yxati bo‘sh.")
            return

        product_list = "📦 **Barcha mahsulotlar:**\n\n"
        for product in products:
            product_list += f"🆔 ID: `{product.id}`\n📌 Nomi: {product.name}\n💰 Narxi: {product.price} so‘m\n\n"

        await message.answer(product_list)


async def send_admin_notification(bot: Bot, user_name: str, user_phone: str):
    admin_message = (
        f"🛍 **Yangi to‘lov ma’lumoti:**\n\n"
        f"👤 Ism: {user_name}\n"
        f"📞 Telefon: {user_phone}\n"
    )
    for admin_id in ADMIN_ID:
        await bot.send_message(admin_id, admin_message)




@router.message(F.text == "🔙 Orqaga")
async def go_back_to_main_menu(message: Message):
    await message.answer("🔙 Asosiy menyuga qaytdingiz.", reply_markup=main_menu)
