from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget
import string
import secrets
import os
import json
from datetime import datetime

PIN_FAYL = "pin.json"
SIFRE_FAYL = "sifreler.json"


class GradientWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_gradient, size=self.update_gradient)
        self.update_gradient()
    
    def update_gradient(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.68, 0.55, 0.88, 1)
            Rectangle(pos=(self.x, self.y + self.height * 0.5), size=(self.width, self.height * 0.5))
            Color(0.52, 0.67, 0.95, 1)
            Rectangle(pos=self.pos, size=(self.width, self.height * 0.5))


class PinDairesi(Widget):
    def __init__(self, dolu=False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(15), dp(15))
        self.dolu = dolu
        self.bind(pos=self.ciz, size=self.ciz)
        self.ciz()
    
    def ciz(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.dolu:
                Color(1, 1, 1, 1)
            else:
                Color(1, 1, 1, 0.4)
            Ellipse(pos=self.pos, size=self.size)
    
    def doldur(self, dolu):
        self.dolu = dolu
        self.ciz()


class PinEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "pin"
        self.daxil_edilmis_pin = ""
        self.pin_daireleri = []
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        gradient_bg = GradientWidget()
        self.add_widget(gradient_bg)
        
        layout = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20), size_hint=(1, 1))
        layout.add_widget(Widget(size_hint_y=0.15))
        
        logo_box = MDBoxLayout(orientation='vertical', size_hint_y=0.30, spacing=dp(20))
        logo_container = MDBoxLayout(size_hint_y=None, height=dp(120))
        logo_card = MDCard(size_hint=(None, None), size=(dp(120), dp(120)), pos_hint={'center_x': 0.5}, md_bg_color=(0.85, 0.75, 0.95, 0.3), radius=[dp(60)], elevation=0)
        logo_container.add_widget(logo_card)
        
        baslig = MDLabel(text="/// M-PERFORMANCE", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1), size_hint_y=None, height=dp(40))
        alt_baslig = MDLabel(text="PIN Kodu Daxil Edin", halign="center", font_style="Body1", theme_text_color="Custom", text_color=(1, 1, 1, 0.8), size_hint_y=None, height=dp(30))
        
        logo_box.add_widget(logo_container)
        logo_box.add_widget(baslig)
        logo_box.add_widget(alt_baslig)
        
        pin_box = MDBoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(20))
        pin_box.add_widget(Widget())
        
        self.pin_daireleri = []
        for i in range(4):
            daire = PinDairesi(dolu=False)
            self.pin_daireleri.append(daire)
            pin_box.add_widget(daire)
        pin_box.add_widget(Widget())
        
        reqemler_box = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=0.47, padding=[dp(20), 0, dp(20), 0])
        
        setir1 = MDBoxLayout(spacing=dp(15), size_hint_y=1)
        for reqem in ['1', '2', '3']:
            setir1.add_widget(self.reqem_duyme_yarat(reqem))
        
        setir2 = MDBoxLayout(spacing=dp(15), size_hint_y=1)
        for reqem in ['4', '5', '6']:
            setir2.add_widget(self.reqem_duyme_yarat(reqem))
        
        setir3 = MDBoxLayout(spacing=dp(15), size_hint_y=1)
        for reqem in ['7', '8', '9']:
            setir3.add_widget(self.reqem_duyme_yarat(reqem))
        
        setir4 = MDBoxLayout(spacing=dp(15), size_hint_y=1)
        setir4.add_widget(MDBoxLayout(size_hint_x=1))
        setir4.add_widget(self.reqem_duyme_yarat('0'))
        
        sag_box = MDBoxLayout(size_hint_x=1)
        btn_sil = MDIconButton(icon="backspace-outline", theme_text_color="Custom", text_color=(1, 1, 1, 0.7), icon_size="32sp")
        btn_sil.bind(on_press=lambda x: self.sil())
        sag_box.add_widget(MDLabel(text=""))
        sag_box.add_widget(btn_sil)
        sag_box.add_widget(MDLabel(text=""))
        setir4.add_widget(sag_box)
        
        reqemler_box.add_widget(setir1)
        reqemler_box.add_widget(setir2)
        reqemler_box.add_widget(setir3)
        reqemler_box.add_widget(setir4)
        
        layout.add_widget(logo_box)
        layout.add_widget(pin_box)
        layout.add_widget(reqemler_box)
        self.add_widget(layout)
    
    def reqem_duyme_yarat(self, reqem):
        btn = MDRaisedButton(text=reqem, size_hint=(1, 1), md_bg_color=(1, 1, 1, 0.9), text_color=(0.3, 0.3, 0.3, 1), font_size='26sp', elevation=0)
        btn.bind(on_press=lambda x: self.reqem_elave_et(reqem))
        return btn
    
    def reqem_elave_et(self, reqem):
        if len(self.daxil_edilmis_pin) < 4:
            self.daxil_edilmis_pin += reqem
            self.pin_gosterici_yenile()
            if len(self.daxil_edilmis_pin) == 4:
                self.pin_yoxla()
    
    def sil(self):
        if self.daxil_edilmis_pin:
            self.daxil_edilmis_pin = self.daxil_edilmis_pin[:-1]
            self.pin_gosterici_yenile()
    
    def pin_gosterici_yenile(self):
        for i, daire in enumerate(self.pin_daireleri):
            daire.doldur(i < len(self.daxil_edilmis_pin))
    
    def pin_yoxla(self):
        dogru_pin = self.pin_oxu()
        if self.daxil_edilmis_pin == dogru_pin:
            self.manager.current = "ana_menu"
            self.daxil_edilmis_pin = ""
            for daire in self.pin_daireleri:
                daire.doldur(False)
        else:
            self.xeta_mesaji()
            self.daxil_edilmis_pin = ""
            for daire in self.pin_daireleri:
                daire.doldur(False)
    
    def pin_oxu(self):
        if os.path.exists(PIN_FAYL):
            with open(PIN_FAYL, 'r') as f:
                data = json.load(f)
                return data.get('pin', '1234')
        else:
            self.pin_yaz('1234')
            return '1234'
    
    def pin_yaz(self, pin):
        with open(PIN_FAYL, 'w') as f:
            json.dump({'pin': pin}, f)
    
    def xeta_mesaji(self):
        dialog = MDDialog(title="Xəta!", text="Yanlış PIN!\nYenidən cəhd edin.", buttons=[MDRaisedButton(text="Bağla", md_bg_color=(0.65, 0.55, 0.88, 1), on_release=lambda x: dialog.dismiss())])
        dialog.open()


class AnaMenuEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "ana_menu"
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        gradient_bg = GradientWidget()
        self.add_widget(gradient_bg)
        
        layout = MDBoxLayout(orientation='vertical', padding=dp(25), spacing=dp(20), size_hint=(1, 1))
        baslig = MDLabel(text="/// M-PERFORMANCE", halign="center", font_style="H5", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1), size_hint_y=0.12)
        
        platforma_card = MDCard(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=None, height=dp(110), md_bg_color=(1, 1, 1, 0.15), radius=[20], elevation=0)
        platforma_label = MDLabel(text="PLATFORMA", font_style="Caption", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 0.9))
        self.platforma_field = MDTextField(hint_text="Instagram, Gmail...", mode="fill", size_hint_y=None, height=dp(50), hint_text_color=(1, 1, 1, 0.6), text_color=(1, 1, 1, 1), fill_color=(1, 1, 1, 0.1))
        platforma_card.add_widget(platforma_label)
        platforma_card.add_widget(self.platforma_field)
        
        uzunluq_card = MDCard(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=None, height=dp(110), md_bg_color=(1, 1, 1, 0.15), radius=[20], elevation=0)
        uzunluq_label = MDLabel(text="SIFRE UZUNLUGU", font_style="Caption", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 0.9))
        self.uzunluq_field = MDTextField(text="16", mode="fill", size_hint_y=None, height=dp(50), text_color=(1, 1, 1, 1), fill_color=(1, 1, 1, 0.1))
        uzunluq_card.add_widget(uzunluq_label)
        uzunluq_card.add_widget(self.uzunluq_field)
        
        yarat_btn = MDRaisedButton(text="YARAT VƏ SAXLA", size_hint_y=None, height=dp(60), md_bg_color=(1, 1, 1, 0.95), text_color=(0.5, 0.5, 0.5, 1), font_size='15sp', elevation=0)
        yarat_btn.bind(on_press=self.sifre_yarat)
        
        self.netice_label = MDLabel(text="", halign="center", font_style="Body2", theme_text_color="Custom", text_color=(1, 1, 1, 1), size_hint_y=0.12)
        
        duyme_box = MDBoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=None, height=dp(55))
        kopyala_btn = MDRaisedButton(text="KOPYALA", size_hint_x=0.5, md_bg_color=(1, 1, 1, 0.2), text_color=(1, 1, 1, 1), elevation=0)
        kopyala_btn.bind(on_press=self.kopyala)
        arxiv_btn = MDRaisedButton(text="TARIXCE", size_hint_x=0.5, md_bg_color=(1, 1, 1, 0.2), text_color=(1, 1, 1, 1), elevation=0)
        arxiv_btn.bind(on_press=self.arxive_kec)
        duyme_box.add_widget(kopyala_btn)
        duyme_box.add_widget(arxiv_btn)
        
        layout.add_widget(baslig)
        layout.add_widget(platforma_card)
        layout.add_widget(uzunluq_card)
        layout.add_widget(yarat_btn)
        layout.add_widget(self.netice_label)
        layout.add_widget(duyme_box)
        layout.add_widget(Widget())
        self.add_widget(layout)
    
    def sifre_yarat(self, instance):
        try:
            uzunluq = int(self.uzunluq_field.text)
            platforma = self.platforma_field.text.strip()
            
            if not platforma:
                self.mesaj("Platforma adını qeyd edin!")
                return
            if uzunluq < 8 or uzunluq > 128:
                self.mesaj("Uzunluq 8-128 arası olmalıdır!")
                return
            
            simvollar = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
            sifre = ''.join(secrets.choice(simvollar) for _ in range(uzunluq))
            self.netice_label.text = sifre
            
            sifreler = []
            if os.path.exists(SIFRE_FAYL):
                with open(SIFRE_FAYL, 'r', encoding='utf-8') as f:
                    sifreler = json.load(f)
            
            sifreler.append({'tarix': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'platforma': platforma, 'sifre': sifre})
            
            with open(SIFRE_FAYL, 'w', encoding='utf-8') as f:
                json.dump(sifreler, f, ensure_ascii=False, indent=2)
            
            self.mesaj("Şifrə yaradıldı!")
        except:
            self.mesaj("Xəta baş verdi!")
    
    def kopyala(self, instance):
        from kivy.core.clipboard import Clipboard
        if self.netice_label.text:
            Clipboard.copy(self.netice_label.text)
            self.mesaj("Kopyalandı!")
        else:
            self.mesaj("Əvvəlcə şifrə yaradın!")
    
    def arxive_kec(self, instance):
        self.manager.current = "arxiv"
    
    def mesaj(self, text):
        dialog = MDDialog(title="Bildiriş", text=text)
        dialog.open()
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: dialog.dismiss(), 1.5)


class ArixvEkrani(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "arxiv"
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        gradient_bg = GradientWidget()
        self.add_widget(gradient_bg)
        
        layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))
        baslig_box = MDBoxLayout(size_hint_y=0.12, padding=[dp(25), dp(25), dp(25), dp(10)])
        baslig = MDLabel(text="SIFRE TARIXCESI", font_style="H5", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1))
        baslig_box.add_widget(baslig)
        
        scroll = MDScrollView(size_hint=(1, 0.78))
        self.sifreler_box = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=dp(25), adaptive_height=True)
        scroll.add_widget(self.sifreler_box)
        
        geri_btn = MDRaisedButton(text="GERIYE QAYIT", size_hint=(1, 0.1), md_bg_color=(1, 1, 1, 0.2), text_color=(1, 1, 1, 1), elevation=0)
        geri_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'ana_menu'))
        
        layout.add_widget(baslig_box)
        layout.add_widget(scroll)
        layout.add_widget(geri_btn)
        self.add_widget(layout)
    
    def on_enter(self):
        self.sifreler_box.clear_widgets()
        if not os.path.exists(SIFRE_FAYL):
            self.sifreler_box.add_widget(MDLabel(text="Hələ ki şifrə yoxdur.", halign="center", theme_text_color="Custom", text_color=(1, 1, 1, 0.7)))
            return
        
        with open(SIFRE_FAYL, 'r', encoding='utf-8') as f:
            sifreler = json.load(f)
        
        for item in reversed(sifreler):
            card = MDCard(orientation='vertical', padding=dp(18), spacing=dp(8), size_hint_y=None, height=dp(110), md_bg_color=(1, 1, 1, 0.15), radius=[15], elevation=0)
            card.add_widget(MDLabel(text=item['tarix'], font_style="Caption", theme_text_color="Custom", text_color=(1, 1, 1, 0.7), size_hint_y=None, height=dp(18)))
            card.add_widget(MDLabel(text=f"[{item['platforma']}]", font_style="Subtitle1", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1), size_hint_y=None, height=dp(28)))
            card.add_widget(MDLabel(text=item['sifre'], font_style="Body2", theme_text_color="Custom", text_color=(1, 1, 1, 0.9), size_hint_y=None, height=dp(35)))
            self.sifreler_box.add_widget(card)


class MPassApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        sm = MDScreenManager()
        sm.add_widget(PinEkrani())
        sm.add_widget(AnaMenuEkrani())
        sm.add_widget(ArixvEkrani())
        return sm


if __name__ == "__main__":
    MPassApp().run()
�
