# Refresh member list
        users = db.get_all_users()
        keyboard = []
        for u in users:
            status = "🔴 BLOCKED" if u["is_blocked"] else "🟢 ACTIVE"
            name = u["full_name"] or u["username"] or str(u["telegram_id"])
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{name} [{status}]",
                        callback_data=f"toggle_user_{u['telegram_id']}",
                    )
                ]
            )
        keyboard.append(
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        )
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if data == "admin_delete_books":
        books = db.get_books()
        if not books:
            await query.message.reply_text("ℹ️ No books to delete.")
            return

        text = "🗑 Select a book to permanently delete:"
        keyboard = []
        for b in books:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"❌ Delete {b['title']}",
                        callback_data=f"delbook_{b['id']}",
                    )
                ]
            )
        keyboard.append(
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        )
        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data.startswith("delbook_"):
        book_id = int(data.split("_")[1])
        file_path = db.delete_book(book_id)
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                logger.error(f"Error removing file {file_path}: {e}")

        await query.answer("Book deleted successfully.", show_alert=True)

        # Refresh delete list
        books = db.get_books()
        if not books:
            await query.edit_message_text("ℹ️ All books have been deleted.")
            return

        keyboard = []
        for b in books:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"❌ Delete {b['title']}",
                        callback_data=f"delbook_{b['id']}",
                    )
                ]
            )
        keyboard.append(
            [InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]
        )
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return


# ==========================================
# APPLICATION ENTRYPOINT
# ==========================================


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("library", library_command))
    application.add_handler(CommandHandler("admin", admin_command))

    # Callback Queries (Inline buttons)
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Admin PDF Upload
    application.add_handler(
        MessageHandler(filters.Document.PDF, handle_document_upload)
    )

    # Text Messages (Registration password input)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
    )

    logger.info("A PLUS PDF LIBRARY Bot started successfully.")
    application.run_polling(drop_pending_updates=True)


if name == "main":
    main()
