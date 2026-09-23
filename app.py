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
        """Injects mobile-first responsive CSS styling and hides GitHub/Fork/branding."""
        is_rtl = self.translations.is_rtl
        direction = "rtl" if is_rtl else "ltr"
        text_align = "right" if is_rtl else "left"

        st.markdown(f"""
        <!-- PWA Mobile Web App Meta Tags -->
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="REMO_OX">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#0e1117">

        <style>
            /* 1. HIDE ALL STREAMLIT HEADER, TOOLBAR, FORK BUTTON, GITHUB ICONS & MANAGE APP */
            header[data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stToolbarActions"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            .stDeployButton,
            #MainMenu,
            footer,
            div:has(> a[href*="github.com"]),
            a[href*="github.com"],
            #manage-app-button,
            [data-testid="manage-app-button"],
            button#manage-app-button,
            div[class*="viewerBadge"],
            div[class*="manageApp"],
            .viewerBadge_container__r5tak,
            .viewerBadge_link__1S137,
            div:has(> #manage-app-button) {{
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                opacity: 0 !important;
                pointer-events: none !important;
                margin: 0 !important;
                padding: 0 !important;
            }}

            /* 2. Main container */
            .main .block-container {{
                direction: {direction};
                text-align: {text_align};
                max-width: 780px;
                padding-top: 1.5rem !important;
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
                margin-top: 10px !important;
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
                padding: 5px 12px;
                margin: 4px;
                border-radius: 6px;
                font-size: 0.85rem;
                font-weight: 500;
            }}

            /* Footer credit */
            .footer-credit {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #1e2433;
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

    def render_pwa_guide(self):
        """Renders shortcut installation guide for mobile users."""
        with st.expander(self.translations.get('install_shortcut_btn'), expanded=False):
            st.markdown(f"#### {self.translations.get('install_guide_title')}")
            col_ios, col_and = st.columns(2)
            with col_ios:
                st.markdown(f"""
                <div style="background: #161b22; padding: 14px; border-radius: 8px; border: 1px solid #2d3748; height: 100%;">
                    <h4 style="color: #00d2ff; margin-top: 0;">{self.translations.get('install_ios_title')}</h4>
                    <p style="color: #cbd5e0; font-size: 0.9rem; line-height: 1.6; white-space: pre-line;">{self.translations.get('install_ios_desc')}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_and:
                st.markdown(f"""
                <div style="background: #161b22; padding: 14px; border-radius: 8px; border: 1px solid #2d3748; height: 100%;">
                    <h4 style="color: #00d2ff; margin-top: 0;">{self.translations.get('install_android_title')}</h4>
                    <p style="color: #cbd5e0; font-size: 0.9rem; line-height: 1.6; white-space: pre-line;">{self.translations.get('install_android_desc')}</p>
                </div>
                """, unsafe_allow_html=True)

    def render_input_section(self):
        """Renders URL input, format, and quality controls."""
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
                self.process_download(url.strip(), is_audio, quality_choice)

    def process_download(self, url, is_audio, quality):
        """Executes the download and handles results."""
        # Check if YouTube link was provided
        if 'youtube.com' in url.lower() or 'youtu.be' in url.lower():
            st.session_state.download_result = None
            st.warning(f"**{self.translations.get('youtube_blocked_title')}**\n\n{self.translations.get('youtube_blocked_desc')}")
            st.link_button(
                label=self.translations.get('download_desktop_btn'),
                url=MediaDownloader.DESKTOP_RELEASE_URL,
                use_container_width=True
            )
            return

        with st.spinner(self.translations.get('processing')):
            success, file_path, filename, mime_type, err = self.downloader.download(
                url=url,
                is_audio=is_audio,
                quality=quality
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
        """Renders supported platform badges and ONLY Developed By REMO_OX."""
        st.markdown(f"""
        <div class="badge-row">
            <span class="platform-tag">🟣 Instagram</span>
            <span class="platform-tag">⚫ TikTok</span>
            <span class="platform-tag">🔵 Facebook</span>
            <span class="platform-tag">⚪ Twitter / X</span>
            <span class="platform-tag">🔴 Pinterest</span>
            <span class="platform-tag">🌐 1000+ Platforms</span>
        </div>
        <div class="footer-credit">
            <p style="color: #00d2ff; font-weight: 700; font-size: 1rem; letter-spacing: 0.5px; margin: 0;">
                Developed By REMO_OX
            </p>
        </div>
        """, unsafe_allow_html=True)

    def run(self):
        """Application execution pipeline."""
        self.inject_custom_styles()
        self.render_header()
        self.render_pwa_guide()
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
