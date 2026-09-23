import os
import sys
import streamlit as st

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from core.config import AppConfig
from core.translations import TranslationManager
from core.downloader import MediaDownloader
from core.cleaner import TempCleaner

class RemoOxWebApp:
    """Main Application Controller implementing OOP architecture for Streamlit."""

    def __init__(self):
        self.init_session_state()
        self.translations = TranslationManager(st.session_state.lang)
        self.downloader = MediaDownloader()
        
        # Periodic background clean of old temp files
        TempCleaner.clean_old_files()

    def init_session_state(self):
        """Initializes persistent Streamlit session variables."""
        if 'lang' not in st.session_state:
            st.session_state.lang = 'ar'
        if 'media_info' not in st.session_state:
            st.session_state.media_info = None
        if 'download_result' not in st.session_state:
            st.session_state.download_result = None

    def inject_custom_styles(self):
        """Injects mobile-first responsive CSS styling with dark neon theme."""
        is_rtl = self.translations.is_rtl
        direction = "rtl" if is_rtl else "ltr"
        text_align = "right" if is_rtl else "left"

        st.markdown(f"""
        <style>
            /* Main container */
            .main .block-container {{
                direction: {direction};
                text-align: {text_align};
                max-width: 780px;
                padding-top: 1.5rem;
                padding-bottom: 3rem;
            }}
            
            /* App title styling */
            .app-header {{
                text-align: center;
                padding: 5px 0 15px 0;
            }}
            .app-title {{
                color: #00d2ff;
                font-size: 2.1rem;
                font-weight: 800;
                margin-bottom: 6px;
                letter-spacing: -0.5px;
            }}
            .app-subtitle {{
                color: #a0aec0;
                font-size: 0.95rem;
                margin-bottom: 10px;
            }}
            .version-badge {{
                display: inline-block;
                background: linear-gradient(135deg, #00d2ff 0%, #0078d7 100%);
                color: #000;
                font-weight: bold;
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.75rem;
            }}

            /* Input box */
            .stTextInput input {{
                border-radius: 8px !important;
                border: 1.5px solid #2d3748 !important;
                background-color: #11141c !important;
                color: #fff !important;
                font-size: 1rem !important;
                padding: 10px 14px !important;
            }}
            .stTextInput input:focus {{
                border-color: #00d2ff !important;
                box-shadow: 0 0 10px rgba(0, 210, 255, 0.2) !important;
            }}

            /* Buttons */
            .stButton > button {{
                border-radius: 8px !important;
                font-weight: 600 !important;
                padding: 8px 16px !important;
                transition: all 0.2s ease-in-out !important;
            }}
            .stButton > button:hover {{
                transform: translateY(-1px);
            }}

            /* Download to device button */
            .stDownloadButton > button {{
                width: 100% !important;
                background: linear-gradient(135deg, #00d2ff 0%, #0078d7 100%) !important;
                color: #050505 !important;
                font-size: 1.15rem !important;
                font-weight: bold !important;
                padding: 14px !important;
                border: none !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3) !important;
            }}
            .stDownloadButton > button:hover {{
                box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5) !important;
                color: #000 !important;
            }}

            /* Supported badges */
            .badge-row {{
                text-align: center;
                margin-top: 25px;
                padding-top: 15px;
                border-top: 1px solid #232936;
            }}
            .platform-tag {{
                display: inline-block;
                background: #1e2433;
                color: #cbd5e0;
                padding: 4px 10px;
                margin: 3px;
                border-radius: 6px;
                font-size: 0.8rem;
            }}
            .engine-tag {{
                display: inline-block;
                background: #0f2738;
                color: #00d2ff;
                border: 1px solid #00d2ff;
                padding: 3px 8px;
                border-radius: 6px;
                font-size: 0.75rem;
                margin-top: 8px;
            }}
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Renders top header with language switch and Update Engine button."""
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col2:
            # The Update Engine button
            if st.button(self.translations.get('update_engine_btn'), key="btn_update_engine", use_container_width=True):
                with st.spinner(self.translations.get('updating_engine')):
                    ok, version, msg = MediaDownloader.upgrade_engine()
                    if ok:
                        st.toast(self.translations.get('engine_updated_success').format(version), icon="✅")
                    else:
                        st.error(self.translations.get('engine_update_failed').format(msg))
                st.rerun()

        with col3:
            current_lang = st.session_state.lang
            lang_label = "English 🇬🇧" if current_lang == 'ar' else "العربية 🇪🇬"
            if st.button(lang_label, key="lang_btn", use_container_width=True):
                st.session_state.lang = 'en' if current_lang == 'ar' else 'ar'
                st.rerun()

        engine_ver = MediaDownloader.get_engine_version()
        st.markdown(f"""
        <div class="app-header">
            <span class="version-badge">{self.translations.get('version_tag')}</span>
            <div class="engine-tag">⚡ {self.translations.get('engine_version_label').format(engine_ver)}</div>
            <h1 class="app-title">{self.translations.get('app_title')}</h1>
            <p class="app-subtitle">{self.translations.get('app_subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)

    def render_input_section(self):
        """Renders URL input, format options, and advanced settings."""
        url = st.text_input(
            label=self.translations.get('url_input_label'),
            placeholder=self.translations.get('url_placeholder'),
            key="url_input"
        )

        col_fmt, col_qty = st.columns(2)
        with col_fmt:
            format_choice = st.selectbox(
                label=self.translations.get('format_label'),
                options=[self.translations.get('format_video'), self.translations.get('format_audio')],
                index=0
            )
        with col_qty:
            is_audio = (format_choice == self.translations.get('format_audio'))
            quality_choice = st.selectbox(
                label=self.translations.get('quality_label'),
                options=AppConfig.VIDEO_QUALITIES,
                index=0,
                disabled=is_audio
            )

        # Advanced Settings Expander (Bypass client & Cookies support)
        with st.expander(self.translations.get('adv_settings'), expanded=False):
            client_options = {
                self.translations.get('client_auto'): 'auto',
                self.translations.get('client_tv'): 'tv',
                self.translations.get('client_android'): 'android',
                self.translations.get('client_web'): 'web'
            }
            selected_client_label = st.selectbox(
                label=self.translations.get('client_mode_label'),
                options=list(client_options.keys()),
                index=0
            )
            client_mode = client_options[selected_client_label]

            cookies_text = st.text_area(
                label=self.translations.get('cookies_label'),
                placeholder=self.translations.get('cookies_placeholder'),
                height=80,
                key="cookies_input"
            )

        col_action, col_clear = st.columns([3, 1])
        with col_action:
            start_clicked = st.button(
                self.translations.get('download_btn'),
                type="primary",
                use_container_width=True
            )
        with col_clear:
            if st.button(self.translations.get('clean_btn'), use_container_width=True):
                count = TempCleaner.clear_all()
                st.session_state.download_result = None
                st.toast(self.translations.get('clean_done'))

        if start_clicked:
            if not url or len(url.strip()) < 5:
                st.error(self.translations.get('error_empty_url'))
            else:
                self.process_download(url.strip(), is_audio, quality_choice, cookies_text, client_mode)

    def process_download(self, url, is_audio, quality, cookies_text=None, client_mode="auto"):
        """Executes the download and handles results."""
        with st.spinner(self.translations.get('processing')):
            success, file_path, filename, mime_type, err = self.downloader.download(
                url=url,
                is_audio=is_audio,
                quality=quality,
                cookies_text=cookies_text,
                client_mode=client_mode
            )

            if success and file_path and os.path.exists(file_path):
                # Read file into session memory
                with open(file_path, "rb") as f:
                    file_data = f.read()

                # Clean up server temp file
                try:
                    os.remove(file_path)
                except Exception:
                    pass

                st.session_state.download_result = {
                    'data': file_data,
                    'filename': filename,
                    'mime': mime_type,
                    'size_mb': len(file_data) / (1024 * 1024)
                }
            else:
                st.session_state.download_result = None
                if err == "BOT_DETECTED":
                    st.warning(self.translations.get('bot_warning'))
                else:
                    st.error(self.translations.get('error_generic').format(err))

    def render_download_result(self):
        """Displays the download button to transfer file to phone/computer."""
        res = st.session_state.download_result
        if res:
            st.success(self.translations.get('ready_to_save'))
            st.info(f"📁 **{res['filename']}** ({res['size_mb']:.1f} MB)")

            # The direct download button for iOS Safari / Android Chrome / PC
            btn_label = self.translations.get('save_to_device_btn').format(f"{res['size_mb']:.1f} MB")
            st.download_button(
                label=btn_label,
                data=res['data'],
                file_name=res['filename'],
                mime=res['mime'],
                key="direct_download_button"
            )

    def render_footer(self):
        """Renders supported platform badges and footer credits."""
        engine_ver = MediaDownloader.get_engine_version()
        st.markdown(f"""
        <div class="badge-row">
            <span class="platform-tag">🔴 YouTube</span>
            <span class="platform-tag">🔵 Facebook</span>
            <span class="platform-tag">🟣 Instagram</span>
            <span class="platform-tag">⚫ TikTok</span>
            <span class="platform-tag">⚪ Twitter / X</span>
            <span class="platform-tag">🌐 1000+ Platforms</span>
            <p style="color: #6b7280; font-size: 0.8rem; margin-top: 15px;">
                {AppConfig.DISPLAY_NAME} ({AppConfig.VERSION}) • Core: yt-dlp {engine_ver} • Developed by {AppConfig.AUTHOR}
            </p>
        </div>
        """, unsafe_allow_html=True)

    def run(self):
        """Application execution pipeline."""
        self.inject_custom_styles()
        self.render_header()
        self.render_input_section()
        self.render_download_result()
        self.render_footer()


# Streamlit Page Setup
st.set_page_config(
    page_title=AppConfig.DISPLAY_NAME,
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if __name__ == "__main__":
    app = RemoOxWebApp()
    app.run()
