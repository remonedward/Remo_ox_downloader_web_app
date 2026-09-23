class TranslationManager:
    """Manages bilingual strings (Arabic and English) with direction support."""
    
    DICTIONARY = {
        'en': {
            'app_title': 'REMO_OX Downloader Web',
            'app_subtitle': 'Fast & Free Video/Audio Downloader for All Devices (iPhone, Android, Mac, Windows, Linux)',
            'version_tag': 'v0.1',
            'url_input_label': 'Video/Audio URL:',
            'url_placeholder': 'https://www.youtube.com/watch?v=... or Facebook, Instagram, TikTok',
            'fetch_btn': 'Analyze Link 🔍',
            'download_btn': 'Download Now',
            'format_label': 'Download Format:',
            'quality_label': 'Quality:',
            'format_video': 'Video (MP4)',
            'format_audio': 'Audio (MP3)',
            'bypass_header': '⚡ YouTube Bypass & Security Settings',
            'cookies_label': 'Browser Cookies:',
            'client_label': 'Bypass Mode:',
            'cookie_none': 'None (Direct)',
            'cookie_chrome': 'Google Chrome',
            'cookie_edge': 'Microsoft Edge',
            'cookie_firefox': 'Mozilla Firefox',
            'cookie_brave': 'Brave Browser',
            'cookie_opera': 'Opera',
            'client_auto': 'Smart Auto (Recommended)',
            'client_ios': 'iOS Emulation',
            'client_android': 'Android Emulation',
            'client_web': 'Standard Web',
            'analyzing': 'Checking URL and formats...',
            'processing': 'Downloading and merging... Please wait.',
            'ready_to_save': 'Download Finished! Click below to save to your device:',
            'save_to_device_btn': '⬇️ Save to Your Device ({})',
            'error_empty_url': 'Please enter a valid video link.',
            'error_generic': 'Error: {}',
            'bot_warning': 'YouTube bot check! Try selecting your browser under "Browser Cookies" (e.g. Chrome or Edge).',
            'platforms_supported': 'Supports YouTube, Facebook, Instagram, TikTok, X (Twitter), and 1000+ sites.',
            'lang_label': 'Language / اللغة:',
            'clean_btn': 'Clear Cache 🧹',
            'clean_done': 'Temporary files cleared successfully.',
            'update_engine_btn': 'Update Engine 🔄',
            'updating_engine': 'Updating core downloader engine... Please wait.',
            'engine_updated_success': 'Engine updated successfully! Current version: {}',
            'engine_update_failed': 'Failed to update engine: {}',
            'engine_version_label': 'Engine: yt-dlp {}'
        },
        'ar': {
            'app_title': 'ريمـو أوكـس - محمل الفيديوهات (ويب)',
            'app_subtitle': 'تحميل سريع ومجاني للفيديوهات والصوتيات لجميع الأجهزة (آيفون، أندرويد، ماك، ويندوز، لينكس)',
            'version_tag': 'الإصدار v0.1',
            'url_input_label': 'رابط الفيديو أو الصوت:',
            'url_placeholder': 'https://www.youtube.com/watch?v=... أو فيسبوك، إنستغرام، تيك توك',
            'fetch_btn': 'فحص الرابط 🔍',
            'download_btn': 'بدء التحميل',
            'format_label': 'نوع التحميل:',
            'quality_label': 'الجودة:',
            'format_video': 'فيديو (MP4)',
            'format_audio': 'صوت (MP3)',
            'bypass_header': '⚡ إعدادات تخطي حظر وقيود يوتيوب (Bypass Settings)',
            'cookies_label': 'كوكيز المتصفح (Browser Cookies):',
            'client_label': 'نمط التخطي (Bypass Mode):',
            'cookie_none': 'بدون (مباشر - None)',
            'cookie_chrome': 'جوجل كروم (Chrome)',
            'cookie_edge': 'مايكروسوفت إيدج (Edge)',
            'cookie_firefox': 'موزيلا فايرفوكس (Firefox)',
            'cookie_brave': 'متصفح بريف (Brave)',
            'cookie_opera': 'متصفح أوبرا (Opera)',
            'client_auto': 'تلقائي ذكي (Smart Auto - موصى به)',
            'client_ios': 'محاكي iOS (iOS Emulation)',
            'client_android': 'محاكي أندرويد (Android Emulation)',
            'client_web': 'متصفح الويب القياسي (Standard Web)',
            'analyzing': 'جاري فحص الرابط...',
            'processing': 'جاري التحميل والدمج... يرجى الانتظار ثوانٍ.',
            'ready_to_save': 'اكتمل التحميل بنجاح! اضغط الزر التالي لحفظ الملف على جهازك:',
            'save_to_device_btn': '⬇️ حفظ الملف على جهازك ({})',
            'error_empty_url': 'يرجى كتابة رابط فيديو صحيح أولاً.',
            'error_generic': 'خطأ: {}',
            'bot_warning': 'يوتيوب يطلب التحقق من الهوية! يرجى اختيار متصفحك من "كوكيز المتصفح" وإعادة المحاولة.',
            'platforms_supported': 'يدعم يوتيوب، فيسبوك، إنستغرام، تيك توك، تويتر، وأكثر من 1000 موقع عالمي.',
            'lang_label': 'اللغة / Language:',
            'clean_btn': 'تنظيف الذاكرة 🧹',
            'clean_done': 'تم مسح الملفات المؤقتة بنجاح.',
            'update_engine_btn': 'تحديث المحرك 🔄',
            'updating_engine': 'جاري تحديث محرك التحميل إلى أحدث إصدار... يرجى الانتظار.',
            'engine_updated_success': 'تم تحديث المحرك بنجاح! الإصدار الحالي: {}',
            'engine_update_failed': 'فشل تحديث المحرك: {}',
            'engine_version_label': 'المحرك: yt-dlp {}'
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
