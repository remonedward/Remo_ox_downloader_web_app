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
        if 'download_result' not in st.session_state:
            st.session_state.download_result = None

    def inject_custom_styles(self):
        """Injects mobile-first responsive CSS styling matching the desktop app."""
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
            
            /* App header */
            .app-header {{
                text-align: center;
                padding: 5px 0 15px 0;
            }}
            .app-title {{
                color: #00d2ff;
                font-size: 2.1rem;
                font-weight: 800;
                margin-bottom: 4px;
                letter-spacing: -0.5px;
            }}
            .app-subtitle {{
                color: #a0aec0;
                font-size: 0.95rem;
                margin-bottom: 8px;
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
            .engine-tag {{
                display: inline-block;
                background: #0f2738;
                color: #00d2ff;
                border: 1px solid #00d2ff;
                padding: 3px 8px;
                border-radius: 6px;
                font-size: 0.75rem;
                margin-top: 6px;
            }}

            /* Bypass Card Box matching desktop EXE */
            .bypass-card {{
                background-color: #161b22;
                border: 1.5px solid #2d3748;
                border-radius: 10px;
                padding: 15px 18px 10px 18px;
                margin: 15px 0;
            }}
            .bypass-title {{
                color: #00d2ff;
                font-size: 0.95rem;
                font-weight: bold;
                margin-bottom: 12px;
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

            /* Primary Download Button (Big Blue matching EXE) */
            .stButton > button[kind="primary"] {{
                width: 100% !important;
                background-color: #0078d7 !important;
                color: white !important;
                font-size: 1.15rem !important;
                font-weight: bold !important;
                padding: 12px !important;
                border: none !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 15px rgba(0, 120, 215, 0.4) !important;
                transition: all 0.2s ease-in-out !important;
            }}
            .stButton > button[kind="primary"]:hover {{
                background-color: #008aff !important;
                box-shadow: 0 6px 20px rgba(0, 138, 255, 0.6) !important;
                transform: translateY(-1px);
            }}

            /* Secondary buttons */
            .stButton > button {{
                border-radius: 8px !important;
                font-weight: 600 !important;
            }}

            /* Direct save button for mobile */
            .stDownloadButton > button {{
                width: 100% !important;
                background: linear-gradient(135deg, #00d2ff 0%, #0078d7 100%) !important;
                color: #050505 !important;
                font-size: 1.15rem !important;
                font-weight: bold !important;
                padding: 14px !important;
                border: none !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4) !important;
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
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Renders top header with language switch and Update Engine button."""
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col2:
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
        """Renders URL input, format, quality, and the YouTube Bypass Settings box."""
        url = st.text_input(
            label=self.translations.get('url_input_label'),
            placeholder=self.translations.get('url_placeholder'),
            key="url_input"
        )

        # Format & Quality
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

        # ⚡ YouTube Bypass & Security Settings (Visible on main screen exactly like EXE)
        st.markdown(f"""
        <div class="bypass-card">
            <div class="bypass-title">{self.translations.get('bypass_header')}</div>
        </div>
        """, unsafe_allow_html=True)

        col_cook, col_byp = st.columns(2)
        with col_cook:
            cookie_options = {
                self.translations.get('cookie_none'): 'none',
                self.translations.get('cookie_chrome'): 'chrome',
                self.translations.get('cookie_edge'): 'edge',
                self.translations.get('cookie_firefox'): 'firefox',
                self.translations.get('cookie_brave'): 'brave',
                self.translations.get('cookie_opera'): 'opera'
            }
            selected_cookie_label = st.selectbox(
                label=self.translations.get('cookies_label'),
                options=list(cookie_options.keys()),
                index=0
            )
            selected_cookie = cookie_options[selected_cookie_label]

        with col_byp:
            client_options = {
                self.translations.get('client_auto'): 'auto',
                self.translations.get('client_ios'): 'ios',
                self.translations.get('client_android'): 'android',
                self.translations.get('client_web'): 'web'
            }
            selected_client_label = st.selectbox(
                label=self.translations.get('client_label'),
                options=list(client_options.keys()),
                index=0
            )
            selected_client = client_options[selected_client_label]

        # Big Download Now Button
        start_clicked = st.button(
            self.translations.get('download_btn'),
            type="primary",
            use_container_width=True
        )

        if start_clicked:
            if not url or len(url.strip()) < 5:
                st.error(self.translations.get('error_empty_url'))
            else:
                self.process_download(url.strip(), is_audio, quality_choice, selected_cookie, selected_client)

    def process_download(self, url, is_audio, quality, cookies_browser="none", client_mode="auto"):
        """Executes the download and handles results."""
        with st.spinner(self.translations.get('processing')):
            success, file_path, filename, mime_type, err = self.downloader.download(
                url=url,
                is_audio=is_audio,
                quality=quality,
                cookies_browser=cookies_browser,
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
