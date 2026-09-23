class TranslationManager:
    """Manages bilingual strings (Arabic and English) with direction support."""
    
    DICTIONARY = {
        'en': {
            'app_title': 'REMO_OX Downloader Web',
            'app_subtitle': 'Fast & Free Video/Audio Downloader for All Devices (iPhone, Android, Mac, Windows, Linux)',
            'version_tag': 'v0.1',
            'url_input_label': 'Video/Audio Link:',
            'url_placeholder': 'https://www.instagram.com/reel/... or TikTok, Facebook, Twitter (X)',
            'fetch_btn': 'Analyze Link 🔍',
            'download_btn': 'Download Now',
            'format_label': 'Download Format:',
            'quality_label': 'Quality:',
            'format_video': 'Video (MP4)',
            'format_audio': 'Audio (MP3)',
            'analyzing': 'Checking URL and formats...',
            'processing': 'Downloading and processing... Please wait a few seconds.',
            'ready_to_save': 'Download Finished! Click below to save to your device:',
            'save_to_device_btn': '⬇️ Save to Your Device ({})',
            'error_empty_url': 'Please enter a valid video link.',
            'error_generic': 'Error: {}',
            'youtube_blocked_title': '⚠️ YouTube Notice',
            'youtube_blocked_desc': 'YouTube blocks video downloads from cloud hosting servers. To download YouTube videos with 100% success and top speed, please use our free Desktop Application (Windows).',
            'download_desktop_btn': '⬇️ Download Desktop App for YouTube (Windows EXE)',
            'platforms_supported': 'Supports Instagram, TikTok, Facebook, Twitter (X), Pinterest, Vimeo, and 1000+ sites.',
            'lang_label': 'Language / اللغة:',
            'clean_btn': 'Clear Cache 🧹',
            'clean_done': 'Temporary files cleared successfully.',
            'update_engine_btn': 'Update Engine 🔄',
            'updating_engine': 'Updating core downloader engine... Please wait.',
            'engine_updated_success': 'Engine updated successfully! Current version: {}',
            'engine_update_failed': 'Failed to update engine: {}',
            'engine_version_label': 'Engine: yt-dlp {}',
            'install_shortcut_btn': '📲 Add App Shortcut to Mobile Home Screen',
            'install_guide_title': '📱 How to install as a Home Screen App:',
            'install_ios_title': '🍏 iPhone & iPad (Safari)',
            'install_ios_desc': "1. Tap the **Share** button `⎋` (square with arrow up at the bottom).\n2. Scroll down and tap **'Add to Home Screen'** `➕`.\n3. Tap **'Add'** in the top right corner.\n\n✨ The app icon will appear on your home screen and open in full-screen standalone mode!",
            'install_android_title': '🤖 Android (Chrome)',
            'install_android_desc': "1. Tap the **three dots menu** `⋮` in the top right of Chrome.\n2. Tap **'Install app'** or **'Add to Home screen'** `➕`.\n3. Tap **'Install'** to confirm.\n\n✨ The app icon will be installed directly on your home screen like any native app!"
        },
        'ar': {
            'app_title': 'ريمـو أوكـس - محمل الفيديوهات (ويب)',
            'app_subtitle': 'تحميل سريع ومجاني للفيديوهات والصوتيات لجميع الأجهزة (آيفون، أندرويد، ماك، ويندوز، لينكس)',
            'version_tag': 'الإصدار v0.1',
            'url_input_label': 'رابط الفيديو أو الصوت:',
            'url_placeholder': 'https://www.instagram.com/reel/... أو تيك توك، فيسبوك، تويتر (X)',
            'fetch_btn': 'فحص الرابط 🔍',
            'download_btn': 'بدء التحميل',
            'format_label': 'نوع التحميل:',
            'quality_label': 'الجودة:',
            'format_video': 'فيديو (MP4)',
            'format_audio': 'صوت (MP3)',
            'analyzing': 'جاري فحص الرابط...',
            'processing': 'جاري التحميل والمعالجة... يرجى الانتظار ثوانٍ.',
            'ready_to_save': 'اكتمل التحميل بنجاح! اضغط الزر التالي لحفظ الملف على جهازك:',
            'save_to_device_btn': '⬇️ حفظ الملف على جهازك ({})',
            'error_empty_url': 'يرجى كتابة رابط فيديو صحيح أولاً.',
            'error_generic': 'خطأ: {}',
            'youtube_blocked_title': '⚠️ تنبيه خاص بيوتيوب',
            'youtube_blocked_desc': 'يوتيوب يفرض حظراً كاملاً على التنزيل من السيرفرات السحابية. لتحميل فيديوهات يوتيوب بدون أي قيود وبأعلى جودة، يرجى استخدام تطبيق سطح المكتب المخصص (ويندوز).',
            'download_desktop_btn': '⬇️ تحميل تطبيق الكمبيوتر لتحميل يوتيوب (Windows EXE)',
            'platforms_supported': 'يدعم إنستغرام، تيك توك، فيسبوك، تويتر (X)، بنترست، فيميو، وأكثر من 1000 موقع عالمي.',
            'lang_label': 'اللغة / Language:',
            'clean_btn': 'تنظيف الذاكرة 🧹',
            'clean_done': 'تم مسح الملفات المؤقتة بنجاح.',
            'update_engine_btn': 'تحديث المحرك 🔄',
            'updating_engine': 'جاري تحديث محرك التحميل إلى أحدث إصدار... يرجى الانتظار.',
            'engine_updated_success': 'تم تحديث المحرك بنجاح! الإصدار الحالي: {}',
            'engine_update_failed': 'فشل تحديث المحرك: {}',
            'engine_version_label': 'المحرك: yt-dlp {}',
            'install_shortcut_btn': '📲 تثبيت أيقونة التطبيق على شاشة هاتفك',
            'install_guide_title': '📱 طريقة إضافة أيقونة التطبيق للشاشة الرئيسية لهاتفك:',
            'install_ios_title': '🍏 هواتف آيفون (iPhone عبر متصفح Safari)',
            'install_ios_desc': "1. اضغط على زر **المشاركة** `⎋` (مربع بسهم لأعلى في شريط المتصفح بالأسفل).\n2. اسحب للأسفل واختر **'إضافة إلى الصفحة الرئيسية'** `➕` (Add to Home Screen).\n3. اضغط على **'إضافة'** (Add) في أعلى اليمين.\n\n✨ ستظهر أيقونة التطبيق فوراً على شاشة هاتفك وتفتح كتطبيق حقيقي ملء الشاشة بدون شريط المتصفح!",
            'install_android_title': '🤖 هواتف أندرويد (Android عبر متصفح Chrome)',
            'install_android_desc': "1. اضغط على قائمة **الثلاث نقاط** `⋮` في أعلى متصفح كروم.\n2. اختر **'تثبيت التطبيق'** (Install app) أو **'إضافة إلى الشاشة الرئيسية'** `➕`.\n3. اضغط على **'تثبيت'** للتأكيد.\n\n✨ ستضاف أيقونة التطبيق إلى شاشة هاتفك وتعمل كتطبيق مستقل بضغطة زر واحدة!"
        }
    }

    def __init__(self, current_lang='ar'):
        self.current_lang = current_lang if current_lang in self.DICTIONARY else 'ar'

    def set_language(self, lang_code):
        if lang_code in self.DICTIONARY:
            self.current_lang = lang_code

    def get(self, key, default=''):
        return self.DICTIONARY.get(self.current_lang, {}).get(key, default)

    @property
    def is_rtl(self):
        return self.current_lang == 'ar'
