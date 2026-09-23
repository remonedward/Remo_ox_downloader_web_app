class TranslationManager:
    """Manages bilingual strings (Arabic and English) with direction support."""
    
    DICTIONARY = {
        'en': {
            'app_title': 'REMO_OX Downloader Web',
            'app_subtitle': 'Fast & Free Video/Audio Downloader for All Devices (iPhone, Android, Mac, Windows, Linux)',
            'version_tag': 'v0.1',
            'url_input_label': 'Paste Video / Audio Link:',
            'url_placeholder': 'YouTube, Facebook, Instagram, TikTok, Twitter/X, etc.',
            'fetch_btn': 'Analyze Link 🔍',
            'download_btn': 'Start Processing ⚡',
            'format_label': 'Download Format:',
            'quality_label': 'Video Quality:',
            'format_video': 'Video (MP4)',
            'format_audio': 'Audio (MP3)',
            'analyzing': 'Analyzing link and fetching available formats...',
            'processing': 'Downloading and converting on server... Please wait.',
            'ready_to_save': 'File is ready! Click the button below to save it directly to your device:',
            'save_to_device_btn': '⬇️ Download to Your Device ({})',
            'error_empty_url': 'Please enter a valid video link.',
            'error_generic': 'Error: {}',
            'bot_warning': 'YouTube bot verification required. Please try mobile client emulation or another link.',
            'platforms_supported': 'Supports YouTube, Facebook, Instagram, TikTok, X (Twitter), and 1000+ sites.',
            'lang_label': 'Language / اللغة:',
            'clean_btn': 'Clear Cache 🧹',
            'clean_done': 'Temporary files cleared successfully.',
            'update_engine_btn': 'Update Engine 🔄',
            'updating_engine': 'Updating core downloader engine... Please wait.',
            'engine_updated_success': 'Engine updated successfully! Current version: {}',
            'engine_update_failed': 'Failed to update engine: {}',
            'engine_version_label': 'Engine: yt-dlp {}',
            'adv_settings': '⚙️ Advanced Settings (Bypass & Cookies)',
            'client_mode_label': 'Bypass Mode:',
            'client_auto': 'Smart Auto (VisionOS / Recommended)',
            'client_tv': 'TV / Embedded Player',
            'client_android': 'Android Player',
            'client_web': 'Standard Web Player',
            'cookies_label': 'YouTube Cookies (Optional Netscape format):',
            'cookies_placeholder': 'Paste cookies.txt content here to bypass strict restrictions if any...'
        },
        'ar': {
            'app_title': 'ريمـو أوكـس - محمل الفيديوهات (ويب)',
            'app_subtitle': 'تحميل سريع ومجاني للفيديوهات والصوتيات لجميع الأجهزة (آيفون، أندرويد، ماك، ويندوز، لينكس)',
            'version_tag': 'الإصدار v0.1',
            'url_input_label': 'ضع رابط الفيديو أو الصوت هنا:',
            'url_placeholder': 'يوتيوب، فيسبوك، إنستغرام، تيك توك، إكس (تويتر)، وغيرها...',
            'fetch_btn': 'فحص الرابط 🔍',
            'download_btn': 'بدء المعالجة ⚡',
            'format_label': 'نوع التحميل:',
            'quality_label': 'جودة الفيديو:',
            'format_video': 'فيديو (MP4)',
            'format_audio': 'صوت نقي (MP3)',
            'analyzing': 'جاري فحص الرابط وجلب الجودات المتاحة...',
            'processing': 'جاري التحميل والدمج على السيرفر... يرجى الانتظار ثوانٍ.',
            'ready_to_save': 'اكتملت المعالجة بنجاح! اضغط الزر التالي لحفظ الملف مباشرة على هاتفك أو جهازك:',
            'save_to_device_btn': '⬇️ حفظ الملف على جهازك ({})',
            'error_empty_url': 'يرجى كتابة رابط فيديو صحيح أولاً.',
            'error_generic': 'خطأ: {}',
            'bot_warning': 'يوتيوب يطلب التحقق من البوت. يرجى تجربة رابط آخر أو محاكي الهواتف.',
            'platforms_supported': 'يدعم يوتيوب، فيسبوك، إنستغرام، تيك توك، تويتر، وأكثر من 1000 موقع عالمي.',
            'lang_label': 'اللغة / Language:',
            'clean_btn': 'تنظيف الذاكرة 🧹',
            'clean_done': 'تم مسح الملفات المؤقتة بنجاح.',
            'update_engine_btn': 'تحديث المحرك 🔄',
            'updating_engine': 'جاري تحديث محرك التحميل إلى أحدث إصدار... يرجى الانتظار.',
            'engine_updated_success': 'تم تحديث المحرك بنجاح! الإصدار الحالي: {}',
            'engine_update_failed': 'فشل تحديث المحرك: {}',
            'engine_version_label': 'المحرك: yt-dlp {}',
            'adv_settings': '⚙️ إعدادات متقدمة (أنماط التخطي والكوكيز)',
            'client_mode_label': 'نمط التخطي والتشغيل:',
            'client_auto': 'تلقائي ذكي (VisionOS / موصى به)',
            'client_tv': 'مشغل التلفاز المدمج (TV)',
            'client_android': 'مشغل أندرويد (Android)',
            'client_web': 'مشغل الويب العادي (Web)',
            'cookies_label': 'كوكيز يوتيوب (بصيغة Netscape اختيارية):',
            'cookies_placeholder': 'ضع نص الكوكيز هنا إذا واجهت رابطاً محمياً يتطلب تسجيل الدخول...'
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
