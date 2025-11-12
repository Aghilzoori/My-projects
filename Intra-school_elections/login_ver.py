import random

# داده‌ها
admin_data = {}
numbers = []
elections = {}  
Deta_Admin = {}
admin_elections = {}
votes = {}


class Login:
    def __init__(self):
        self.message_1 = False
        self.mode_bot = ""
        self.login_success = False
        self.admin_login = None
        self.user_login = None
        self.admin_window = None  

    def reset(self):
        """ریست کردن تمام وضعیت‌ها به حالت اول"""
        self.message_1 = False
        self.admin_login = None
        self.user_login = None
        self.mode_bot = ""
        self.login_success = False
        self.admin_window = None

    def process_message(self, message):   
        
        if message == "/bot_order":
            self.reset()
            return "🔄 ربات ریست شد!\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n\n👨‍💼 برای ورود ادمین ⟵ 1\n👤 برای ورود کاربر ⟵ 2"
        
        if self.login_success:
            if self.mode_bot == "Admin" and self.admin_window:
                return self.admin_window.last(message)

        if not self.message_1:
            self.message_1 = True
            return "🎯 **به سیستم رأی‌گیری خوش آمدید**\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n\n👨‍💼 ورود ادمین ⟵ 1\n👤 ورود کاربر ⟵ 2"
        
        if self.mode_bot == "Admin" and self.admin_login:
            if self.admin_login.login_success:
                if not self.admin_window:
                    self.admin_window = WindowAdmin(self.admin_login.user_data[1])
                    self.login_success = True
                    return self.admin_window.last("")
                else:
                    return self.admin_window.last(message)
            else:
                return self.admin_login.process_message(message)
        
        elif self.mode_bot == "User" and self.user_login:
            if self.user_login.login_complete:
                if self.user_login.voting_stage:
                    result = self.user_login.vote(message)
                    if not self.user_login.voting_stage:
                        self.login_success = True
                    return result
                else:
                    result = self.user_login.login(message)
                    if "رأی شما" in result or "قبلاً" in result:
                        self.login_success = True
                    return result
            else:
                result = self.user_login.login(message)
                if self.user_login.login_complete:
                    self.login_success = True
                return result
        
        elif message == "2":
            self.mode_bot = "User"
            self.user_login = Login_User()
            return self.user_login.login(message)
        
        elif message == "1":
            self.mode_bot = "Admin"
            self.admin_login = AdminLogin()
            return self.admin_login.process_message(message)
        else:
            return "⚠️ لطفاً ابتدا گزینه 1 یا 2 را انتخاب کنید"


class AdminLogin:
    def __init__(self):
        self.initial_message_shown = False
        self.registration_stage = 0
        self.login_stage = 0
        self.user_data = []
        self.mode = None
        self.login_success = False
    
    def reset(self):
        self.initial_message_shown = False
        self.registration_stage = 0  
        self.login_stage = 0  
        self.user_data = []
        self.mode = None  
        self.login_success = False
    
    def handle_registration(self, message):
        if self.registration_stage == 0:
            self.registration_stage = 1
            return "📍 **مرحله ۱ از ۴: شهر**\n\nلطفاً اسم شهر خود را وارد کنید:"
        
        elif self.registration_stage == 1:
            self.user_data.append(message)
            self.registration_stage = 2
            return f"✅ شهر **{message}** ثبت شد\n\n👤 **مرحله ۲ از ۴: نام کامل**\n\nلطفاً نام و نام خانوادگی خود را وارد کنید:"
        
        elif self.registration_stage == 2:
            self.user_data.append(message)
            self.registration_stage = 3
            return f"✅ نام و نام خانوادگی **{message}** ثبت شد\n\n🏫 **مرحله ۳ از ۴: مدرسه**\n\nلطفاً اسم مدرسه خود را وارد کنید:"
        
        elif self.registration_stage == 3:
            self.user_data.append(message)
            self.registration_stage = 4
            return f"✅ مدرسه **{message}** ثبت شد\n\n🔐 **مرحله ۴ از ۴: رمز عبور**\n\nلطفاً رمز عبور خود را وارد کنید:"
        
        elif self.registration_stage == 4:
            self.user_data.append(message)
            
            admin_data[self.user_data[1]] = {
                'city': self.user_data[0],
                'full_name': self.user_data[1],
                'school': self.user_data[2],
                'password': self.user_data[3]  
            }
            
            self.login_success = True
            return '🎉 **ثبت‌نام با موفقیت انجام شد!**\n\nاکنون می‌توانید از منوی مدیریت استفاده کنید.'

    def handle_login(self, message):
        if self.login_stage == 0:
            self.login_stage = 1
            return "👤 **مرحله ۱ از ۲: نام کاربری**\n\nلطفاً نام و نام خانوادگی خود را وارد کنید:"
        
        elif self.login_stage == 1:
            user_found = False
            for full_name, user_data in admin_data.items():
                if user_data['full_name'] == message:
                    user_found = True
                    self.user_data = [
                        user_data['city'], 
                        user_data['full_name'], 
                        user_data['school'], 
                        user_data['password']
                    ]
                    break
            
            if user_found:
                self.login_stage = 2
                return "🔐 **مرحله ۲ از ۲: رمز عبور**\n\nلطفاً رمز عبور خود را وارد کنید:"
            else:
                return "❌ نام و نام خانوادگی اشتباه است\n\nلطفاً مجدداً نام و نام خانوادگی خود را وارد کنید:"

        elif self.login_stage == 2:
            if message == self.user_data[-1]:
                self.login_success = True
                return "✅ **ورود موفق!**\n\nخوش آمدید! اکنون می‌توانید از منوی مدیریت استفاده کنید."
            else:
                return "❌ رمز عبور اشتباه است\n\nلطفاً مجدداً رمز عبور خود را وارد کنید:"

    def process_message(self, message):
        if not self.initial_message_shown:
            self.initial_message_shown = True
            return "👨‍💼 **پنل مدیریت**\n\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n\n📝 ثبت‌نام ادمین جدید ⟵ 1\n🔐 ورود ادمین موجود ⟵ 2"
        
        if message == "1":
            self.mode = 'register'
            return self.handle_registration("")
        elif message == "2":
            self.mode = 'login'
            return self.handle_login("")
        else:
            if self.mode == 'register':
                return self.handle_registration(message)
            elif self.mode == 'login':
                return self.handle_login(message)
            else:
                return "⚠️ لطفاً 1 یا 2 را وارد کنید"


class WindowAdmin:
    def __init__(self, admin_name=""):
        self.stage1 = False
        self.add_stage1 = False
        self.add_stage2 = False
        self.add_stage3 = False
        self.deta = []
        self.edit_stage1 = False
        self.edit_stage2 = False
        self.mode_edit = ""
        self.edit_data = []
        self.edit2_data = []
        self.deta_name = []
        self.mode = ""
        self.neme_election = ""
        self.admin_name = admin_name
        self.delete_stage = False
        self.results_stage = False
    
    def add(self, message):
        if not self.add_stage1:
            self.add_stage1 = True
            return "📋 **مرحله ۱ از ۲: نام انتخابات**\n\nلطفاً موضوع یا یک اسم برای انتخابات خود انتخاب کنید:"
        
        elif self.add_stage1 and not self.add_stage2:
            self.add_stage2 = True
            self.deta.append(message)
            return f"✅ نام انتخابات **{message}** ثبت شد\n\n🔐 **مرحله ۲ از ۲: رمز انتخابات**\n\nلطفاً رمز عبور انتخابات برای ورود کاربران را وارد کنید:"
        
        elif self.add_stage2 and not self.add_stage3:
            self.add_stage3 = True
            self.deta.append(message)
            
            election_name = self.deta[0]
            election_password = self.deta[1]
            candidates = []
            
            if self.admin_name not in admin_elections:
                admin_elections[self.admin_name] = {}
            
            admin_elections[self.admin_name][election_name] = {
                'password': election_password,
                'candidates': candidates,
                'votes': {}
            }
            
            elections[election_name] = {
                'admin': self.admin_name,
                'password': election_password,
                'candidates': candidates,
                'votes': {}
            }
            
            # بازنشانی متغیرها
            self.add_stage1 = False
            self.add_stage2 = False
            self.add_stage3 = False
            self.deta = []  # باگ: فراموش شده بود
            self.mode = ""
            
            return f"""🎉 **انتخابات با موفقیت ایجاد شد!**

📝 اطلاعات انتخابات:
• نام: **{election_name}**
• رمز: **{election_password}**

📌 برای افزودن کاندیدا به بخش «ویرایش انتخابات» مراجعه کنید.

👨‍💼 **پنل مدیریت انتخابات**

📋 گزینه‌های موجود:
➕ ساخت انتخابات جدید ⟵ 1
✏️ ویرایش انتخابات موجود ⟵ 2  
🗑️ حذف انتخابات ⟵ 3
📊 مشاهده نتایج انتخابات ⟵ 4

لطفاً گزینه مورد نظر را انتخاب کنید:"""

    def delete_election(self, message):
        if not self.delete_stage:
            self.delete_stage = True
            admin_election_list = []
            if self.admin_name in admin_elections:
                admin_election_list = list(admin_elections[self.admin_name].keys())
            
            if not admin_election_list:
                self.delete_stage = False
                return "📭 **هیچ انتخابی برای حذف وجود ندارد**\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            
            elections_text = '\n'.join([f"• {election}" for election in admin_election_list])
            
            return f"""🗑️ **حذف انتخابات**

📋 لیست انتخابات‌های شما:
{elections_text}

⚠️ لطفاً نام انتخابات مورد نظر برای حذف را وارد کنید (برای انصراف ⟵ 00):"""
        
        elif self.delete_stage:
            if message == "00":
                self.delete_stage = False
                self.mode = ""  # باگ: فراموش شده بود
                return "✅ **عملیات حذف لغو شد**\n\nبه منوی اصلی بازگشتید.\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            
            if self.admin_name in admin_elections and message in admin_elections[self.admin_name]:
                # حذف از admin_elections
                del admin_elections[self.admin_name][message]
                
                # حذف از elections
                if message in elections:
                    del elections[message]
                
                # حذف از votes
                if message in votes:
                    del votes[message]
                
                self.delete_stage = False
                self.mode = ""  # باگ: فراموش شده بود
                return f"✅ **انتخابات «{message}» با موفقیت حذف شد**\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            else:
                return "❌ انتخابات مورد نظر یافت نشد\n\nلطفاً نام انتخابات را مجدداً وارد کنید (برای انصراف ⟵ 00):"

    def show_results(self, message):
        if not self.results_stage:
            self.results_stage = True
            admin_election_list = []
            if self.admin_name in admin_elections:
                admin_election_list = list(admin_elections[self.admin_name].keys())
            
            if not admin_election_list:
                self.results_stage = False
                return "📭 **هیچ انتخابی برای مشاهده نتایج وجود ندارد**\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            
            elections_text = '\n'.join([f"• {election}" for election in admin_election_list])
            
            return f"""📊 **مشاهده نتایج انتخابات**

📋 لیست انتخابات‌های شما:
{elections_text}

لطفاً نام انتخابات مورد نظر برای مشاهده نتایج را وارد کنید (برای انصراف ⟵ 00):"""
        
        elif self.results_stage:
            if message == "00":
                self.results_stage = False
                self.mode = ""  # باگ: فراموش شده بود
                return "✅ **عملیات مشاهده نتایج لغو شد**\n\nبه منوی اصلی بازگشتید.\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            
            if self.admin_name in admin_elections and message in admin_elections[self.admin_name]:
                election = admin_elections[self.admin_name][message]
                candidates = election['candidates']
                
                if not candidates:
                    self.results_stage = False
                    self.mode = ""  # باگ: فراموش شده بود
                    return f"📭 **هیچ کاندیدی در انتخابات «{message}» ثبت نشده است**\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
                
                # محاسبه آرای هر کاندید
                vote_counts = {candidate[0]: 0 for candidate in candidates}
                
                # شمارش آرای از votes
                if message in votes:
                    for user_id, candidate_index in votes[message].items():
                        if 0 <= candidate_index < len(candidates):
                            candidate_name = candidates[candidate_index][0]
                            vote_counts[candidate_name] += 1
                
                # مرتب‌سازی بر اساس تعداد آراء (نزولی)
                sorted_results = sorted(vote_counts.items(), key=lambda x: x[1], reverse=True)
                
                # ساخت متن نتایج
                results_text = "🏆 **نتایج انتخابات:**\n\n"
                for i, (candidate, count) in enumerate(sorted_results):
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
                    results_text += f"{medal} {candidate}: {count} رأی\n"
                
                # تعداد کل آراء
                total_votes = sum(vote_counts.values())
                results_text += f"\n📊 تعداد کل آراء: {total_votes}"
                
                self.results_stage = False
                self.mode = ""  # باگ: فراموش شده بود
                return f"""📊 **نتایج انتخابات: {message}**

{results_text}

👨‍💼 **پنل مدیریت انتخابات**

📋 گزینه‌های موجود:
➕ ساخت انتخابات جدید ⟵ 1
✏️ ویرایش انتخابات موجود ⟵ 2  
🗑️ حذف انتخابات ⟵ 3
📊 مشاهده نتایج انتخابات ⟵ 4

لطفاً گزینه مورد نظر را انتخاب کنید:"""
            else:
                return "❌ انتخابات مورد نظر یافت نشد\n\nلطفاً نام انتخابات را مجدداً وارد کنید (برای انصراف ⟵ 00):"

    def Edit(self, message):
        if not self.edit_stage1:
            self.edit_stage1 = True
            admin_election_list = []
            if self.admin_name in admin_elections:
                admin_election_list = list(admin_elections[self.admin_name].keys())
            
            if not admin_election_list:
                self.edit_stage1 = False
                return "📭 **هیچ انتخابی برای ویرایش وجود ندارد**\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            
            elections_text = '\n'.join([f"• {election}" for election in admin_election_list])
            
            return f"""✏️ **ویرایش انتخابات**

    📋 لیست انتخابات‌های شما:
    {elections_text}

    📝 لطفاً نام انتخابات مورد نظر برای ویرایش را وارد کنید:"""
        
        elif self.edit_stage1 and not self.edit_stage2:
            if self.admin_name in admin_elections and message in admin_elections[self.admin_name]:
                self.neme_election = message
                self.edit_stage2 = True
                return f"""✅ **دسترسی به انتخابات «{message}» باز شد**

    📋 گزینه‌های ویرایش:
    ➕ افزودن کاندیدا ⟵ 8
    ➖ حذف کاندیدا ⟵ 9
    🚪 خروج ⟵ 00

    لطفاً گزینه مورد نظر را انتخاب کنید:"""
            else:
                return "❌ انتخابات مورد نظر یافت نشد\n\nلطفاً نام انتخابات را مجدداً وارد کنید:"
        
        elif self.edit_stage2:
            if message == "8":
                self.mode_edit = "add"
                return "👤 **افزودن کاندیدا**\n\nلطفاً نام کاندیدای جدید را وارد کنید (برای پایان ⟵ 11):"
            
            elif message == "9":
                self.mode_edit = "del"
                candidates = admin_elections[self.admin_name][self.neme_election]['candidates']
                if not candidates:
                    return "📭 **هیچ کاندیدی برای حذف وجود ندارد**\n\n📋 گزینه‌های ویرایش:\n➕ افزودن کاندیدا ⟵ 8\n➖ حذف کاندیدا ⟵ 9\n🚪 خروج ⟵ 00\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
                
                candidate_list = "\n".join([f"• {c[0]}" for c in candidates])
                return f"""➖ **حذف کاندیدا**

    📋 کاندیداهای فعلی:
    {candidate_list}

    🗑️ لطفاً نام دقیق کاندیدای مورد نظر برای حذف را وارد کنید:"""
            
            elif message == "00":
                self.edit_stage1 = False
                self.edit_stage2 = False
                self.mode_edit = ""
                self.mode = ""
                return "✅ **ویرایش پایان یافت**\n\nبه منوی اصلی بازگشتید.\n\n👨‍💼 **پنل مدیریت انتخابات**\n\n📋 گزینه‌های موجود:\n➕ ساخت انتخابات جدید ⟵ 1\n✏️ ویرایش انتخابات موجود ⟵ 2  \n🗑️ حذف انتخابات ⟵ 3\n📊 مشاهده نتایج انتخابات ⟵ 4\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
            
            elif self.mode_edit == "add":
                if message == "11":
                    self.mode_edit = ""
                    self.edit2_data = []
                    return "✅ **کاندیداها با موفقیت ثبت شدند**\n\nمی‌توانید اقدامات دیگر را انجام دهید.\n\n📋 گزینه‌های ویرایش:\n➕ افزودن کاندیدا ⟵ 8\n➖ حذف کاندیدا ⟵ 9\n🚪 خروج ⟵ 00\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
                
                number = random.randint(0, 999999)
                while number in numbers:
                    number = random.randint(0, 999999)
                numbers.append(number)
                app_list = [message, number]
                self.edit2_data.append(app_list)
                
                if self.admin_name in admin_elections and self.neme_election in admin_elections[self.admin_name]:
                    admin_elections[self.admin_name][self.neme_election]['candidates'].append(app_list)
                    elections[self.neme_election]['candidates'].append(app_list)
                
                return f"✅ کاندیدای **{message}** با کد **{number}** اضافه شد\n\nنام کاندیدای بعدی را وارد کنید (برای پایان ⟵ 11):"
            
            elif self.mode_edit == "del":
                if self.admin_name in admin_elections and self.neme_election in admin_elections[self.admin_name]:
                    candidates = admin_elections[self.admin_name][self.neme_election]['candidates']
                    candidate_found = False
                    
                    for i, candidate in enumerate(candidates):
                        if message == candidate[0]:
                            # حذف کاندیدا
                            del candidates[i]
                            candidate_found = True
                            
                            # حذف از elections
                            if self.neme_election in elections:
                                elections_candidates = elections[self.neme_election]['candidates']
                                for j, ec in enumerate(elections_candidates):
                                    if message == ec[0]:
                                        del elections_candidates[j]
                                        break
                            
                            # حذف آرای مربوط به این کاندیدا
                            if self.neme_election in votes:
                                for user_id in list(votes[self.neme_election].keys()):
                                    if votes[self.neme_election][user_id] >= i:
                                        if votes[self.neme_election][user_id] == i:
                                            del votes[self.neme_election][user_id]
                                        else:
                                            votes[self.neme_election][user_id] -= 1
                            
                            break
                    
                    if candidate_found:
                        return "✅ **کاندیدا با موفقیت حذف شد**\n\nمی‌توانید اقدامات دیگر را انجام دهید.\n\n📋 گزینه‌های ویرایش:\n➕ افزودن کاندیدا ⟵ 8\n➖ حذف کاندیدا ⟵ 9\n🚪 خروج ⟵ 00\n\nلطفاً گزینه مورد نظر را انتخاب کنید:"
                
                return "❌ کاندیدای مورد نظر یافت نشد\n\nلطفاً نام دقیق کاندیدا را وارد کنید:"
            
            else:
                return "⚠️ دستور نامعتبر است\n\nلطفاً از گزینه‌های معتبر استفاده کنید:\n➕ افزودن کاندیدا ⟵ 8\n➖ حذف کاندیدا ⟵ 9\n🚪 خروج ⟵ 00"
    def last(self, messages):
        if not self.stage1:
            self.stage1 = True
            return """👨‍💼 **پنل مدیریت انتخابات**

📋 گزینه‌های موجود:
➕ ساخت انتخابات جدید ⟵ 1
✏️ ویرایش انتخابات موجود ⟵ 2  
🗑️ حذف انتخابات ⟵ 3
📊 مشاهده نتایج انتخابات ⟵ 4

لطفاً گزینه مورد نظر را انتخاب کنید:"""
        
        if messages == "1":
            self.mode = "made"
            self.add_stage1 = False
            self.add_stage2 = False
            self.add_stage3 = False
            self.deta = []
            return self.add(messages)
        
        elif messages == "2":
            self.mode = "edit"
            self.edit_stage1 = False
            self.edit_stage2 = False
            self.mode_edit = ""
            self.edit2_data = []
            return self.Edit(messages)
        
        elif messages == "3":
            self.mode = "delete"
            self.delete_stage = False
            return self.delete_election(messages)
        
        elif messages == "4":
            self.mode = "results"
            self.results_stage = False
            return self.show_results(messages)
        
        else:
            if self.mode == "made":
                return self.add(messages)
            elif self.mode == "edit":
                return self.Edit(messages)
            elif self.mode == "delete":
                return self.delete_election(messages)
            elif self.mode == "results":
                return self.show_results(messages)
            else:
                return "⚠️ گزینه نامعتبر است\n\nلطفاً 1، 2، 3 یا 4 را وارد کنید:"
class Login_User:
    def __init__(self):
        self.reset()

    def reset(self):
        self.deta_user = []
        self.current_stage_user = 0
        self.stage = 0
        self.login_complete = False
        self.voting_stage = False
        self.current_election = None
        self.showing_elections = False
        self.vote_count = 0  # شمارنده تعداد رأی‌های کاربر
        self.max_votes = 7   # حداکثر تعداد رأی مجاز
        self.in_voting_session = False  # وضعیت جدید برای مدیریت جلسه رأی‌گیری

    def show_elections(self, school_name):
        available_elections = []
        for election_name, election_data in elections.items():
            admin_name = election_data['admin']
            if admin_name in admin_data:
                admin_school = admin_data[admin_name]['school']
                if admin_school == school_name:
                    available_elections.append(election_name)
        return available_elections

    def get_user_identifier(self):
        return f"{self.deta_user[0]}_{self.deta_user[1]}_{self.deta_user[2]}"

    def vote(self, message):
        if not self.voting_stage:
            return "⚠️ خطا در وضعیت رأی‌گیری"

        # اگر کاربر به حداکثر رأی رسیده باشد
        if self.vote_count >= self.max_votes:
            self.voting_stage = False
            self.showing_elections = False
            self.in_voting_session = False
            return f"""❌ **شما به حداکثر تعداد رأی مجاز رسیده‌اید!**

📊 شما در این جلسه به {self.vote_count} نفر رأی داده‌اید.

🔚 جلسه رأی‌گیری پایان یافت.

👋 با تشکر از مشارکت شما!"""

        # اگر در حال نمایش لیست انتخابات هستیم
        if self.showing_elections:
            try:
                election_index = int(message) - 1
                available_elections = self.show_elections(self.deta_user[2])
                
                if 0 <= election_index < len(available_elections):
                    election_name = available_elections[election_index]
                    self.current_election = election_name
                    self.showing_elections = False
                    self.in_voting_session = True
                    
                    election = elections[election_name]
                    candidates = election['candidates']
                    
                    if not candidates:
                        self.showing_elections = True
                        return "📭 **هیچ کاندیدی در این انتخابات ثبت نشده است**\n\nلطفاً انتخابات دیگری انتخاب کنید:"
                    
                    candidate_list = "\n".join([f"{i+1}. {candidate[0]}" for i, candidate in enumerate(candidates)])
                    remaining_votes = self.max_votes - self.vote_count
                    
                    return f"""🗳️ **انتخابات: {election_name}**

👥 کاندیداها:
{candidate_list}

📊 شما تاکنون {self.vote_count} رأی داده‌اید (حداکثر {self.max_votes} رأی)
🎯 {remaining_votes} رأی باقی‌مانده

🔢 لطفاً شماره کاندیدای مورد نظر خود را وارد کنید (برای بازگشت به لیست انتخابات ⟵ 0):"""
                else:
                    return "❌ شماره انتخابات نامعتبر است\n\nلطفاً شماره صحیح را وارد کنید:"
            except ValueError:
                return "⚠️ لطفاً یک عدد وارد کنید:"
        
        # اگر در حال رأی دادن هستیم
        else:
            try:
                # امکان بازگشت به لیست انتخابات
                if message == "0":
                    self.showing_elections = True
                    self.current_election = None
                    available_elections = self.show_elections(self.deta_user[2])
                    election_list = "\n".join([f"{i+1}. {election}" for i, election in enumerate(available_elections)])
                    remaining_votes = self.max_votes - self.vote_count
                    
                    return f"""🗳️ **انتخابات‌های فعال**

{election_list}

📊 شما تاکنون {self.vote_count} رأی داده‌اید (حداکثر {self.max_votes} رأی)
🎯 {remaining_votes} رأی باقی‌مانده

🔢 لطفاً شماره انتخابات مورد نظر را وارد کنید:"""
                
                candidate_index = int(message) - 1
                election = elections[self.current_election]
                candidates = election['candidates']
                
                if 0 <= candidate_index < len(candidates):
                    user_id = self.get_user_identifier()
                    
                    # ثبت رأی (بدون بررسی قبلی بودن)
                    if self.current_election not in votes:
                        votes[self.current_election] = {}
                    
                    # ثبت رأی جدید (امکان رأی دادن مکرر در یک انتخابات)
                    votes[self.current_election][f"{user_id}_{self.vote_count}"] = candidate_index
                    
                    selected_candidate = candidates[candidate_index][0]
                    self.vote_count += 1
                    
                    remaining_votes = self.max_votes - self.vote_count
                    
                    # اگر کاربر به حداکثر رأی رسیده باشد
                    if self.vote_count >= self.max_votes:
                        self.voting_stage = False
                        self.showing_elections = False
                        self.in_voting_session = False
                        return f"""✅ **رأی شما ثبت شد!**

🎉 شما به **{selected_candidate}** رأی دادید.

❌ **شما به حداکثر تعداد رأی مجاز رسیده‌اید!**

📊 شما در این جلسه به {self.vote_count} نفر رأی داده‌اید.

🔚 جلسه رأی‌گیری پایان یافت.

👋 با تشکر از مشارکت شما!"""
                    else:
                        # بازگشت به لیست کاندیداهای همان انتخابات برای رأی بعدی
                        candidate_list = "\n".join([f"{i+1}. {candidate[0]}" for i, candidate in enumerate(candidates)])
                        
                        return f"""✅ **رأی شما ثبت شد!**

🎉 شما به **{selected_candidate}** رأی دادید.

📊 شما تاکنون {self.vote_count} رأی داده‌اید (حداکثر {self.max_votes} رأی)
🎯 {remaining_votes} رأی باقی‌مانده

🗳️ **انتخابات: {self.current_election}**

👥 کاندیداها:
{candidate_list}

🔢 لطفاً شماره کاندیدای بعدی مورد نظر خود را وارد کنید (برای بازگشت به لیست انتخابات ⟵ 0):"""
                else:
                    return "❌ شماره کاندیدا نامعتبر است\n\nلطفاً شماره صحیح را وارد کنید:"
            except ValueError:
                return "⚠️ لطفاً یک عدد وارد کنید:"

    def login(self, message):
        if self.stage == 0:
            self.stage = 1
            return "👤 **مرحله ۱ از ۳: نام کامل**\n\nلطفاً نام و نام خانوادگی خود را وارد کنید:"
        
        elif self.stage == 1:
            self.deta_user.append(message)
            self.stage = 2
            return f"✅ نام و نام خانوادگی **{message}** ثبت شد\n\n📍 **مرحله ۲ از ۳: شهر**\n\nلطفاً اسم شهر یا شهرستان خود را وارد کنید:"
        
        elif self.stage == 2:
            self.deta_user.append(message)
            self.stage = 3
            return f"✅ شهر/شهرستان **{message}** ثبت شد\n\n🏫 **مرحله ۳ از ۳: مدرسه**\n\nلطفاً نام مدرسه خود را وارد کنید:"
        
        elif self.stage == 3:
            self.deta_user.append(message)
            self.stage = 4
            
            school_found = False
            admin_name = ""
            
            for full_name, admin_info in admin_data.items():
                if admin_info['school'] == self.deta_user[-1]:
                    school_found = True
                    admin_name = admin_info['full_name']
                    break
            
            if school_found:
                self.login_complete = True
                available_elections = self.show_elections(self.deta_user[-1])
                
                if available_elections:
                    election_list = "\n".join([f"• {election}" for i, election in enumerate(available_elections)])
                    return f"""✅ **ورود موفق!**

🏫 مدرسه: **{self.deta_user[-1]}**
👨‍💼 مدیر: **{admin_name}**

🗳️ انتخابات‌های فعال:
{election_list}

📊 شما می‌توانید حداکثر به {self.max_votes} نفر رأی دهید.

📌 برای شروع رأی‌گیری عدد ⟵ 4 را وارد کنید"""
                else:
                    return f"""✅ **ورود موفق!**

🏫 مدرسه: **{self.deta_user[-1]}**
👨‍💼 مدیر: **{admin_name}**

📭 **هیچ انتخابات فعالی وجود ندارد**

🔄 برای بررسی مجدد عدد ⟵ 4 را وارد کنید"""
            else:
                return "❌ مدرسه‌ای با این نام یافت نشد\n\nلطفاً مجدداً نام مدرسه را وارد کنید:"
        
        elif self.stage == 4 and self.login_complete:
            if message == "4":
                if self.vote_count >= self.max_votes:
                    return f"""❌ **شما به حداکثر تعداد رأی مجاز رسیده‌اید!**

📊 شما تاکنون به {self.vote_count} نفر رأی داده‌اید.

🔚 امکان رأی دادن بیشتر وجود ندارد.

👋 با تشکر از مشارکت شما!"""
                
                available_elections = self.show_elections(self.deta_user[2])
                if not available_elections:
                    return "📭 **هیچ انتخابات فعالی برای مدرسه شما وجود ندارد**\n\nلطفاً بعداً مجدداً تلاش کنید."
                
                self.voting_stage = True
                self.showing_elections = True
                self.in_voting_session = True
                
                election_list = "\n".join([f"{i+1}. {election}" for i, election in enumerate(available_elections)])
                remaining_votes = self.max_votes - self.vote_count
                
                return f"""🗳️ **شروع جلسه رأی‌گیری**

📊 شما می‌توانید تا {self.max_votes} رأی دهید.
🎯 {remaining_votes} رأی باقی‌مانده

{election_list}

🔢 لطفاً شماره انتخابات مورد نظر را وارد کنید:"""
            else:
                return "📌 برای شروع رأی‌گیری عدد ⟵ 4 را وارد کنید"
        
        else:
            return "⚠️ خطا در پردازش\n\nلطفاً مجدداً تلاش کنید."
# تست کد
if __name__ == "__main__":
    bot = Login()
    print("🤖 ربات شروع به کار کرد...")
    
    while True:
        user_input = input("شما: ")
        response = bot.process_message(user_input)
        print("ربات:", response)
        
        if user_input.lower() == 'exit':
            break