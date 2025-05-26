from aiogram_dialog import Dialog

from app.bot.bookings.windows import get_capacity_window, get_table_window, get_date_window, get_slots_window, \
        get_confirmed_windows, get_my_book, admin_dialog_menu_window, admin_count_user

booking_dialog = Dialog(
get_capacity_window(),
        get_table_window(),
        get_date_window(),
        get_slots_window(),
        get_confirmed_windows()
)
my_booking_dialog = Dialog(
        get_my_book()
)
admin_dialog = Dialog(
        admin_dialog_menu_window(),
                admin_count_user()
)
