import logging
import asyncio
from aiogram import Bot, Dispatcher , F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from database import init_db, close_db
from admin import router as admin_router , send_admin_notification
from database import Order, Product
from buttons import main_menu, product_keyboard, cart_keyboard, phone_button
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

TOKEN = "7838713709:AAFmbZCfjL7jTVAowNJIJFo3MU_JyD0nUOw"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(admin_router)

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu)

@dp.message(F.text == "🛍 Mahsulotlar")
async def show_products(message: types.Message):
    products = await Product.all()
    if not products:
        await message.answer("Hozircha mahsulotlar mavjud emas.")
        return
    product = products[0]
    await message.answer_photo(
        photo=product.photo,
        caption=f"📌 {product.name}\n💰 Narxi: {product.price} so‘m\nℹ️ {product.description}",
        reply_markup=await product_keyboard(product.id)
    )

@dp.callback_query(F.data.startswith("next_"))
async def next_product(callback: CallbackQuery):
    products = await Product.all()
    current_id = int(callback.data.split("_")[1])
    product_ids = [p.id for p in products]

    if current_id in product_ids:
        idx = product_ids.index(current_id)
        next_idx = (idx + 1) % len(products)
        product = products[next_idx]
        await callback.message.edit_media(
            types.InputMediaPhoto(
                media=product.photo,
                caption=f"📌 {product.name}\n💰 Narxi: {product.price} so‘m\nℹ️ {product.description}"
            ),
            reply_markup=await product_keyboard(product.id)
        )

@dp.callback_query(F.data.startswith("prev_"))
async def prev_product(callback: CallbackQuery):
    products = await Product.all()
    current_id = int(callback.data.split("_")[1])
    product_ids = [p.id for p in products]

    if current_id in product_ids:
        idx = product_ids.index(current_id)
        prev_idx = (idx - 1) % len(products)
        product = products[prev_idx]
        await callback.message.edit_media(
            types.InputMediaPhoto(
                media=product.photo,
                caption=f"📌 {product.name}\n💰 Narxi: {product.price} so‘m\nℹ️ {product.description}"
            ),
            reply_markup=await product_keyboard(product.id)
        )

@dp.callback_query(F.data.startswith("buy_"))
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    count = await Order.filter(user_id=user_id, product_id=product_id).count()
    if count >= 5:
        await callback.answer("❌ Siz bu mahsulotdan 5 martadan ko‘p xarid qila olmaysiz!", show_alert=True)
        return

    await Order.create(user_id=user_id, product_id=product_id)
    await callback.answer("✅ Mahsulot savatchaga qo‘shildi!", show_alert=True)

async def update_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    orders = await Order.filter(user_id=user_id).prefetch_related("product")

    if not orders:
        await callback.message.edit_text("📭 Sizning savatchangiz bo‘sh!")
        return

    total_price = sum(order.product.price for order in orders)
    cart_text = "🛍 **Sizning savatchangiz:**\n\n" + \
                "\n".join(f"📌 {order.product.name} — 💰 {order.product.price} so‘m" for order in orders) + \
                f"\n\n🛍 **Jami summa:** {total_price} so‘m"

    await callback.message.edit_text(cart_text, reply_markup=await cart_keyboard(orders), parse_mode="Markdown")

@dp.message(F.text == "🛒 Savatcha")
async def my_orders(message: Message):
    user_id = message.from_user.id
    orders = await Order.filter(user_id=user_id).prefetch_related("product")

    if not orders:
        await message.answer("📭 Sizning savatchangiz bo‘sh!")
        return

    total_price = sum(order.product.price for order in orders)
    cart_text = "🛍 **Sizning savatchangiz:**\n\n" + \
                "\n".join(f"📌 {order.product.name} — 💰 {order.product.price} so‘m" for order in orders) + \
                f"\n\n🛍 **Jami summa:** {total_price} so‘m"

    await message.answer(cart_text, reply_markup=await cart_keyboard(orders), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("remove_"))
async def remove_product(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    order = await Order.get_or_none(id=order_id, user_id=user_id)

    if not order:
        await callback.answer("❌ Bu buyurtma allaqachon o‘chirilgan!", show_alert=True)
        return

    await order.delete()
    await callback.answer("✅ Mahsulot savatchadan olib tashlandi!")
    await update_cart(callback)


class PaymentState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()


@dp.callback_query(F.data == "pay_now")
async def ask_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Iltimos, ismingizni kiriting:")
    await state.set_state(PaymentState.waiting_for_name)


@dp.message(PaymentState.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(
        f"Sizning ismingiz: {user_name}\nEndi telefon raqamingizni yuboring:",
        reply_markup=phone_button()
    )
    await state.set_state(PaymentState.waiting_for_phone)


@dp.message(PaymentState.waiting_for_phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    user_phone = message.contact.phone_number
    data = await state.get_data()
    user_name = data.get("name", "Noma'lum")

    await message.answer(
        f"Ismingiz: {user_name}\nTelefon raqamingiz: {user_phone}\n\n"
    )


    user_id = message.from_user.id
    await Order.filter(user_id=user_id).delete()

    await send_admin_notification(bot, user_name, user_phone)

    await message.answer(
        "Rahmat! Biz siz bilan keyinroq bog'lanamiz.",
        reply_markup=main_menu
    )

    await state.clear()

@dp.message(F.text == "📞 Biz bilan bog‘lanish")
async def contact(message: Message):
    await message.answer(" +998 99 999 99 99")

async def main():
    await init_db()
    try:
        await dp.start_polling(bot)
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())
