#!/usr/bin/env python3
"""
🤖 My Awesome Telegram Bot - Production Ready
A complete, feature-rich Telegram bot ready for deployment!
Created with ❤️ for the community
"""

import os
import logging
import random
import asyncio
import aiohttp
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 8000))
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')

# Simple in-memory storage (for free hosting)
user_data = {}
game_sessions = {}

class MyAwesomeBot:
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😂",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why did the math book look sad? It had too many problems! 📚",
            "What do you call a sleeping bull? A bulldozer! 😴",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "What's orange and sounds like a parrot? A carrot! 🥕",
            "Why did the cookie go to the doctor? Because it felt crumbly! 🍪",
            "What do you call a dinosaur that loves to sleep? A dino-snore! 🦕"
        ]
        
        self.fun_facts = [
            "🐙 Octopuses have three hearts and blue blood!",
            "🍯 Honey never spoils - archaeologists have found 3000-year-old honey that's still edible!",
            "🐧 Penguins can jump 6 feet in the air!",
            "🌙 A day on Venus is longer than its year!",
            "🦋 Butterflies taste with their feet!",
            "🐨 Koalas sleep 20-22 hours per day!",
            "🌟 There are more stars in the universe than grains of sand on all Earth's beaches!",
            "🐬 Dolphins have names for each other!",
            "🌍 Earth is the only planet not named after a god!",
            "🧠 Your brain uses about 20% of your body's energy!"
        ]
        
        self.animals = [
            ("🐶", "Dog"), ("🐱", "Cat"), ("🐰", "Rabbit"), ("🐼", "Panda"),
            ("🐨", "Koala"), ("🦊", "Fox"), ("🐸", "Frog"), ("🐧", "Penguin"),
            ("🦋", "Butterfly"), ("🐢", "Turtle"), ("🐝", "Bee"), ("🦁", "Lion"),
            ("🐯", "Tiger"), ("🐺", "Wolf"), ("🦉", "Owl"), ("🐙", "Octopus")
        ]
        
        self.quotes = [
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Life is what happens to you while you're busy making other plans.", "John Lennon"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
            ("The only impossible journey is the one you never begin.", "Tony Robbins"),
            ("In the middle of every difficulty lies opportunity.", "Albert Einstein"),
            ("Believe you can and you're halfway there.", "Theodore Roosevelt")
        ]
        
        self.quiz_questions = [
            {
                "question": "What's the largest planet in our solar system?",
                "options": ["🌍 Earth", "🪐 Jupiter", "🔴 Mars", "💫 Venus"],
                "correct": 1,
                "explanation": "Jupiter is the largest planet - it's so big that all other planets could fit inside it!"
            },
            {
                "question": "How many hearts does an octopus have?",
                "options": ["❤️ 1", "💕 2", "💖 3", "💝 4"],
                "correct": 2,
                "explanation": "Octopuses have 3 hearts! Two pump blood to the gills, one pumps to the rest of the body."
            },
            {
                "question": "What's the fastest land animal?",
                "options": ["🐆 Cheetah", "🦁 Lion", "🐎 Horse", "🐕 Greyhound"],
                "correct": 0,
                "explanation": "Cheetahs can run up to 70 mph (113 km/h) in short bursts!"
            },
            {
                "question": "Which element has the chemical symbol 'Au'?",
                "options": ["🥈 Silver", "🥇 Gold", "🔶 Copper", "⚡ Aluminum"],
                "correct": 1,
                "explanation": "Au comes from the Latin word 'aurum' meaning gold!"
            }
        ]

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message with interactive menu"""
        user = update.effective_user
        
        # Store user data
        user_data[user.id] = {
            'name': user.first_name,
            'username': user.username,
            'joined': datetime.now().isoformat(),
            'commands_used': user_data.get(user.id, {}).get('commands_used', 0)
        }
        
        welcome_text = f"""
🎉 **Welcome {user.first_name}!** 🎉

I'm your friendly bot assistant! Here's what I can do:

🎮 **Games & Fun:**
• `/roll` - Roll a dice
• `/game` - Number guessing game  
• `/quiz` - Quick trivia questions
• `/animal` - Random cute animal
• `/joke` - Funny jokes
• `/fact` - Amazing fun facts

🔧 **Useful Tools:**
• `/math` - Simple calculator
• `/weather` - Weather information
• `/quote` - Daily inspiration
• `/reminder` - Set reminders
• `/help` - Show all commands

✨ **Just send me any message and I'll chat with you!**

Try clicking the buttons below! 👇
        """
        
        keyboard = [
            [InlineKeyboardButton("🎲 Roll Dice", callback_data="roll"),
             InlineKeyboardButton("🎮 Play Game", callback_data="game")],
            [InlineKeyboardButton("😂 Tell Joke", callback_data="joke"),
             InlineKeyboardButton("🤓 Fun Fact", callback_data="fact")],
            [InlineKeyboardButton("🧠 Quick Quiz", callback_data="quiz"),
             InlineKeyboardButton("🐱 Cute Animal", callback_data="animal")],
            [InlineKeyboardButton("📊 My Stats", callback_data="stats"),
             InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all available commands"""
        help_text = """
🤖 **Bot Commands Help** 🤖

**🎮 Games & Entertainment:**
• `/roll` - Roll a 6-sided dice
• `/game` - Start number guessing game
• `/quiz` - Quick trivia questions
• `/joke` - Get a random joke
• `/fact` - Learn something amazing
• `/animal` - See a cute animal

**🔧 Utility Commands:**
• `/math <expression>` - Calculate math
• `/weather <city>` - Get weather info
• `/quote` - Daily inspiration
• `/reminder <min> <text>` - Set reminder
• `/stats` - Your personal statistics
• `/about` - About this bot

**💬 Chat Features:**
• Send any text for friendly responses
• Send math like "10+5" and I'll solve it
• Ask questions and I'll try to help!

Made with ❤️ for you! Need help? Just ask! 😊
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def roll_dice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Roll dice with animation"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        rolling_msg = await update.message.reply_text("🎲 Rolling dice... ")
        
        # Animation effect
        for i in range(3):
            await asyncio.sleep(0.5)
            await rolling_msg.edit_text(f"🎲 Rolling dice{'.' * (i+1)} ")
        
        result = random.randint(1, 6)
        dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        dice_emoji = dice_faces[result - 1]
        
        if result == 6:
            message = f"{dice_emoji} **You rolled {result}!** 🎉\n✨ Perfect! Maximum score!"
        elif result == 1:
            message = f"{dice_emoji} **You rolled {result}!** 😅\nEveryone needs luck sometimes!"
        else:
            message = f"{dice_emoji} **You rolled {result}!** 👍\nNice roll!"
        
        keyboard = [[InlineKeyboardButton("🎲 Roll Again", callback_data="roll")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await rolling_msg.edit_text(message, parse_mode='Markdown', reply_markup=reply_markup)

    async def start_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start number guessing game"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        secret_number = random.randint(1, 10)
        
        game_sessions[user_id] = {
            'type': 'number_guess',
            'number': secret_number,
            'attempts': 0,
            'max_attempts': 3
        }
        
        await update.message.reply_text(
            "🎮 **Number Guessing Game!**\n\n"
            "I'm thinking of a number between 1 and 10! 🤔\n"
            "You have **3 attempts** to guess it!\n\n"
            "Send me your guess (just type a number)!",
            parse_mode='Markdown'
        )

    async def quick_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick trivia quiz"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        question_data = random.choice(self.quiz_questions)
        
        game_sessions[user_id] = {
            'type': 'quiz',
            'question': question_data
        }
        
        keyboard = []
        for i, option in enumerate(question_data['options']):
            keyboard.append([InlineKeyboardButton(option, callback_data=f"quiz_{i}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🧠 **Quick Quiz!**\n\n{question_data['question']}",
            reply_markup=reply_markup
        )

    async def tell_joke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tell a random joke"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        joke = random.choice(self.jokes)
        
        keyboard = [[InlineKeyboardButton("😂 Another Joke", callback_data="joke")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"😄 **Here's a joke for you:**\n\n{joke}", 
            parse_mode='Markdown', 
            reply_markup=reply_markup
        )

    async def fun_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Share a fun fact"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        fact = random.choice(self.fun_facts)
        
        keyboard = [[InlineKeyboardButton("🤓 Another Fact", callback_data="fact")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🧠 **Amazing Fact:**\n\n{fact}", 
            parse_mode='Markdown', 
            reply_markup=reply_markup
        )

    async def cute_animal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show random cute animal"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        emoji, name = random.choice(self.animals)
        
        keyboard = [[InlineKeyboardButton("🐾 Another Animal", callback_data="animal")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"{emoji} **Your cute animal:** {name}!\n💕 Isn't it adorable?", 
            parse_mode='Markdown', 
            reply_markup=reply_markup
        )

    async def daily_quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send inspiring quote"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        quote, author = random.choice(self.quotes)
        
        quote_text = f"""
✨ **Daily Inspiration** ✨

"{quote}"

— {author}

🌟 Have an amazing day! 🌟
        """
        
        keyboard = [[InlineKeyboardButton("✨ Another Quote", callback_data="quote")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(quote_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def calculate_math(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simple math calculator"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        if not context.args:
            await update.message.reply_text(
                "🧮 **Math Calculator**\n\n"
                "Usage: `/math <expression>`\n\n"
                "Examples:\n"
                "• `/math 5 + 3`\n"
                "• `/math 10 * 2`\n"
                "• `/math (5 + 3) * 2`",
                parse_mode='Markdown'
            )
            return
        
        expression = ' '.join(context.args)
        
        try:
            import re
            if re.match(r'^[\d\s+\-*/()\.,]+$', expression):
                result = eval(expression)
                await update.message.reply_text(
                    f"🧮 **Math Result:**\n\n`{expression} = {result}`",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text("❌ Invalid expression! Only numbers and basic operators allowed.")
        except Exception:
            await update.message.reply_text("❌ Error in calculation. Please check your expression!")

    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get weather (placeholder - requires API key)"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        if not context.args:
            await update.message.reply_text(
                "🌤️ **Weather Service**\n\n"
                "Usage: `/weather <city name>`\n"
                "Example: `/weather London`\n\n"
                "Weather service requires API setup. Coming soon! ✨"
            )
            return
        
        city = ' '.join(context.args)
        
        # Placeholder response (implement with actual weather API)
        await update.message.reply_text(
            f"🌤️ **Weather for {city.title()}**\n\n"
            "Weather service is being set up! 🔧\n"
            "Get a free API key from openweathermap.org to enable this feature.\n\n"
            "Coming soon with real weather data! ☀️"
        )

    async def reminder_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set a reminder"""
        user_id = update.effective_user.id
        self.update_user_stats(user_id)
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "⏰ **Set a Reminder**\n\n"
                "Usage: `/reminder <minutes> <message>`\n\n"
                "Examples:\n"
                "• `/reminder 5 Take a break`\n"
                "• `/reminder 30 Meeting time`\n"
                "• `/reminder 60 Call mom`",
                parse_mode='Markdown'
            )
            return
        
        try:
            minutes = int(context.args[0])
            reminder_text = ' '.join(context.args[1:])
            
            if minutes > 1440:  # More than 24 hours
                await update.message.reply_text("❌ Maximum reminder time is 24 hours!")
                return
            
            await update.message.reply_text(
                f"⏰ **Reminder Set!**\n\n"
                f"I'll remind you in **{minutes} minute{'s' if minutes != 1 else ''}**:\n"
                f"📝 *{reminder_text}*",
                parse_mode='Markdown'
            )
            
            # Schedule reminder
            asyncio.create_task(self.send_reminder(update.effective_chat.id, minutes, reminder_text))
            
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number of minutes!")

    async def send_reminder(self, chat_id: int, minutes: int, message: str):
        """Send reminder after specified time"""
        await asyncio.sleep(minutes * 60)
        
        reminder_text = f"""
🔔 **REMINDER ALERT!** 🔔

⏰ You asked me to remind you:
📝 *{message}*

Hope this helps! ✨
        """
        
        try:
            application = Application.builder().token(BOT_TOKEN).build()
            await application.bot.send_message(
                chat_id=chat_id, 
                text=reminder_text, 
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to send reminder: {e}")

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user statistics"""
        user_id = update.effective_user.id
        user_info = user_data.get(user_id, {})
        
        if not user_info:
            await update.message.reply_text("❌ No stats available. Use /start first!")
            return
        
        joined_date = user_info.get('joined', 'Unknown')
        if joined_date != 'Unknown':
            joined_date = datetime.fromisoformat(joined_date).strftime('%B %d, %Y')
        
        commands_used = user_info.get('commands_used', 0)
        
        stats_text = f"""
📊 **Your Bot Statistics** 📊

👤 **Name:** {user_info.get('name', 'Unknown')}
📅 **Joined:** {joined_date}
🎯 **Commands Used:** {commands_used}
🏆 **Status:** {'Power User 🌟' if commands_used > 20 else 'Active User 💪' if commands_used > 5 else 'Getting Started 🌱'}

Thanks for using the bot! 🎉
        """
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """About this bot"""
        about_text = """
🤖 **About This Bot** 🤖

**Version:** 2.0.0
**Features:** Games, utilities, fun facts, and more!
**Status:** Running 24/7 on free hosting ⚡

**What I can do:**
✅ Interactive games and quizzes
✅ Math calculator and utilities  
✅ Fun facts and daily inspiration
✅ Reminders and helpful tools
✅ Friendly conversations

**Free & Open Source** 💝
This bot runs on free hosting and is available to everyone!

**Developer:** Made with ❤️ for the Telegram community
**Support:** If you find issues, let us know!

Enjoy using the bot! 🌟
        """
        
        await update.message.reply_text(about_text, parse_mode='Markdown')

    def update_user_stats(self, user_id: int):
        """Update user command count"""
        if user_id in user_data:
            user_data[user_id]['commands_used'] = user_data[user_id].get('commands_used', 0) + 1

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        message = update.message.text.lower()
        
        # Handle game sessions
        if user_id in game_sessions:
            await self.handle_game_input(update, context)
            return
        
        # Math expressions
        if any(op in message for op in ['+', '-', '*', '/', '=']) and any(c.isdigit() for c in message):
            try:
                import re
                math_expr = re.sub(r'[^\d+\-*/().\s]', '', message)
                if math_expr.strip():
                    result = eval(math_expr)
                    await update.message.reply_text(f"🧮 {math_expr.strip()} = **{result}**", parse_mode='Markdown')
                    return
            except:
                pass
        
        # Friendly responses
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        questions = ['how are you', 'what can you do', 'help me']
        compliments = ['thank you', 'thanks', 'awesome', 'great', 'amazing', 'cool']
        
        if any(greeting in message for greeting in greetings):
            responses = [
                f"Hello {user_name}! 👋 How can I help you today?",
                f"Hi there, {user_name}! 😊 What would you like to do?",
                f"Hey {user_name}! 🎉 Ready for some fun? Try /roll or /game!"
            ]
        elif any(question in message for question in questions):
            responses = [
                f"I can do lots of things, {user_name}! Try /help to see all my commands! 🤖",
                "I'm here to entertain and help you! Games, facts, math, and more! 🎯",
                f"I'm doing great, {user_name}! I can play games, tell jokes, do math, and chat! 😄"
            ]
        elif any(compliment in message for compliment in compliments):
            responses = [
                f"You're very welcome, {user_name}! 😊 I'm happy to help!",
                f"Aww, thanks {user_name}! 🥰 You're awesome too!",
                "I'm glad you like it! Feel free to use me anytime! ✨"
            ]
        else:
            responses = [
                f"That's interesting, {user_name}! 🤔 Try /help to see what I can do!",
                f"Cool message, {user_name}! 👍 Want to play a game? Try /game!",
                f"Thanks for sharing, {user_name}! 😊 How about a fun fact? Try /fact!"
            ]
        
        response = random.choice(responses)
        
        # Quick action buttons
        keyboard = [
            [InlineKeyboardButton("🎲 Roll Dice", callback_data="roll"),
             InlineKeyboardButton("😂 Tell Joke", callback_data="joke")],
            [InlineKeyboardButton("🎮 Play Game", callback_data="game"),
             InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(response, reply_markup=reply_markup)

    async def handle_game_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle game inputs"""
        user_id = update.effective_user.id
        session = game_sessions[user_id]
        
        if session['type'] == 'number_guess':
            await self.handle_number_guess(update, context)

    async def handle_number_guess(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle number guessing game"""
        user_id = update.effective_user.id
        session = game_sessions[user_id]
        
        try:
            guess = int(update.message.text)
        except ValueError:
            await update.message.reply_text("❌ Please send a number between 1 and 10!")
            return
        
        if guess < 1 or guess > 10:
            await update.message.reply_text("❌ Please guess between 1 and 10!")
            return
        
        session['attempts'] += 1
        secret = session['number']
        
        if guess == secret:
            del game_sessions[user_id]
            await update.message.reply_text(
                f"🎉 **CONGRATULATIONS!** 🎉\n\n"
                f"You guessed it! The number was **{secret}**!\n"
                f"You won in {session['attempts']} attempt{'s' if session['attempts'] > 1 else ''}! 🏆\n\n"
                f"Play again with /game!",
                parse_mode='Markdown'
            )
        elif session['attempts'] >= session['max_attempts']:
            del game_sessions[user_id]
            await update.message.reply_text(
                f"😅 **Game Over!**\n\n"
                f"The number was **{secret}**. Try again with /game!",
                parse_mode='Markdown'
            )
        else:
            remaining = session['max_attempts'] - session['attempts']
            hint = "higher! 📈" if guess < secret else "lower! 📉"
            
            await update.message.reply_text(
                f"❌ Try {hint}\n"
                f"Attempts remaining: **{remaining}** 🎯",
                parse_mode='Markdown'
            )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        # Create a fake message for handlers that expect update.message
        class FakeMessage:
            def __init__(self, original_message):
                self.message_id = original_message.message_id
                self.chat = original_message.chat
                self.date = original_message.date
        
        update.message = FakeMessage(query.message)
        
        # Handle different button types
        if query.data == "roll":
            await self.roll_dice(update, context)
        elif query.data == "joke":
            await self.tell_joke(update, context)
        elif query.data == "fact":
            await self.fun_fact(update, context)
        elif query.data == "animal":
            await self.cute_animal(update, context)
        elif query.data == "game":
            await self.start_game(update, context)
        elif query.data == "quiz":
            await self.quick_quiz(update, context)
        elif query.data == "quote":
            await self.daily_quote(update, context)
        elif query.data == "stats":
            await self.show_stats(update, context)
        elif query.data == "help":
            await self.help_command(update, context)
        elif query.data.startswith("quiz_"):
            await self.handle_quiz_answer(update, context, query.data)

    async def handle_quiz_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
        """Handle quiz answer selection"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        if user_id not in game_sessions or game_sessions[user_id]['type'] != 'quiz':
            await query.edit_message_text("❌ Quiz session expired. Try /quiz again!")
            return
        
        answer_index = int(callback_data.split('_')[1])
        question_data = game_sessions[user_id]['question']
        correct_index = question_data['correct']
        
        del game_sessions[user_id]  # Clear session
        
        if answer_index == correct_index:
            result_text = f"🎉 **Correct!** 🎉\n\n{question_data['explanation']}\n\nWell done! 🏆"
        else:
            correct_option = question_data['options'][correct_index]
            result_text = f"❌ **Not quite!**\n\nThe correct answer was: {correct_option}\n\n{question_data['explanation']}\n\nTry another question! 💪"
        
        keyboard = [[InlineKeyboardButton("🧠 Another Quiz", callback_data="quiz")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(result_text, parse_mode='Markdown', reply_markup=reply_markup)

    def setup_application(self):
        """Setup the bot application with all handlers"""
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("roll", self.roll_dice))
        application.add_handler(CommandHandler("game", self.start_game))
        application.add_handler(CommandHandler("quiz", self.quick_quiz))
        application.add_handler(CommandHandler("joke", self.tell_joke))
        application.add_handler(CommandHandler("fact", self.fun_fact))
        application.add_handler(CommandHandler("animal", self.cute_animal))
        application.add_handler(CommandHandler("quote", self.daily_quote))
        application.add_handler(CommandHandler("math", self.calculate_math))
        application.add_handler(CommandHandler("weather", self.weather_command))
        application.add_handler(CommandHandler("reminder", self.reminder_command))
        application.add_handler(CommandHandler("stats", self.show_stats))
        application.add_handler(CommandHandler("about", self.about_command))
        
        # Button callback handler
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for regular text
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        return application

def main():
    """Main function to run the bot"""
    print("🚀 Starting My Awesome Telegram Bot...")
    
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN environment variable not set!")
        print("Please set your bot token from BotFather")
        return
    
    bot = MyAwesomeBot()
    application = bot.setup_application()
    
    # Check if running in webhook mode (production) or polling mode (development)
    if WEBHOOK_URL:
        # Production mode with webhooks
        print(f"🌐 Starting webhook server on port {PORT}...")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
        )
    else:
        # Development mode with polling
        print("🔧 Running in development mode with polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
