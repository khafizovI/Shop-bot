from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🛍 Mahsulotlar")],
    [KeyboardButton(text="🛒 Savatcha"), KeyboardButton(text="📞 Biz bilan bog‘lanish")]
], resize_keyboard=True)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Mahsulot qo‘shish"), KeyboardButton(text="🗑 Mahsulotni o‘chirish")],
        [KeyboardButton(text="🔙 Orqaga")]
    ],
    resize_keyboard=True
)

async def product_keyboard(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"prev_{product_id}"),
             InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"next_{product_id}")],
            [InlineKeyboardButton(text="🛒 Savatchaga qo‘shish", callback_data=f"buy_{product_id}")]
        ]
    )

async def cart_keyboard(orders):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for order in orders:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=f"❌ {order.product.name} ni o‘chirish", callback_data=f"remove_{order.id}")]
        )
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="💳 To‘lov qilish", callback_data="pay_now")])
    return keyboard


def remove_button(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Savatchadan olib tashlash", callback_data=f"remove_{order_id}")],
            [InlineKeyboardButton(text="🛒 Sotib olish", callback_data=f"buy_{order_id}")]
        ]
    )

def payment_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("💳 To‘lov qilish", callback_data="pay_now")
    keyboard.add(button)
    return keyboard


def admin_remove_button(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ O‘chirish", callback_data=f"remove_{product_id}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_admin_menu")]
        ]
    )

province_buttons = [
    "Toshkent", "Samarkand", "Buxoro", "Farg‘ona", "Andijon",
    "Namangan", "Jizzax", "Qashqadaryo", "Surxondaryo",
    "Xorazm", "Sirdaryo", "Navoiy"
]

def province_keyboard():
    keyboard = [
        [InlineKeyboardButton(text=province_buttons[i], callback_data=f"province_{province_buttons[i]}")]
        for i in range(len(province_buttons))
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def phone_button():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )


def inline_province_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=province_buttons[i], callback_data=f"province_{province_buttons[i]}")
             for i in range(0, len(province_buttons), 2)],
            [InlineKeyboardButton(text=province_buttons[i], callback_data=f"province_{province_buttons[i]}")
             for i in range(1, len(province_buttons), 2)]
        ]
    )