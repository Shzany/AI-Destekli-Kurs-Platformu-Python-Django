
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
YOUR_API_KEY = os.getenv("YOUR_API_KEY")

class DesignWebsite():
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--headless")
        self.client = genai.Client(api_key=YOUR_API_KEY)  

    def create_prompts(self, subject):
        contents = f"Bana {subject} konusunu alt başlıklara ayır. Basit ve yalın başlıklar olsun emoji özel karakter kullanma . Herhangi bir açıklama istemiyorum. Yalnızca alt alta başlıklar olsun. Başka hiçibir şey olmasın. Boş satır olmasın. Boş satır sorun yaratıyor. Bir kurs programı edasıyla yaz. giriş fln gibi kısımlar olmasın daha somut ve net başlıklar olsun. {subject} konusundan şaşma. başlıklar sadece teknik yazılımsal olsun ve konuyu ince detayına kadar kategorisel olarak tanımlasın. Çok uç başlıklar yazma sadece konuyu öğrenmeye yönelik konu başlıkları olsun tıpkı bir kurs içeriğinin başlıkları gibi"
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
        self.prompt = response.text  
        print(self.prompt)
        return self.prompt.strip().splitlines()

    def create_content(self, prompt, subject):
        contents = subject + " " + prompt + f""" 
        Sadece <body> etiketinin içeriğini HTML ve satır içi CSS kullanarak oluştur. Sayfa iskeleti oluşturma. Modern ve estetik bir tasarım elde et.Yapabileceğin en öğretici ve bilgilendirici tasarımı yapmaya çalış. Aşağıdaki gereksinimleri karşıla:

        * Metinler ortalanmış olsun, ancak tamamen kenarlara yapışmasın; belirli bir boşluk bırak.
        * Arka plan rengi, gölge efekti, yazı tipi ve diğer stil detaylarını kullanarak modern bir görünüm sağla.
        * Başlık ve paragraf metni içersin.
        * Tasarım sade ama şık olsun.
        * Kod içeriği dışında hiçbir yazı istemiyorum.
        * Tasarım kayması olmasın ve sayfa responsive olsun.
        * Tasarımı yaparken iyi düşün.
        * Aşağıdaki metni kullanarak bir öğrenim akışı oluştur:

        * Her konu başlığı için gerektiği zaman aşağıdaki bilgileri sun:
            * Başlık
            * Açıklama
            * Kod örneği
            * Performans bilgisi
            * Kullanım alanları
        * Renk seçimleri ve genel tasarım, verdiğim örneğe yakın olsun.

        Örnek tasarım:
        
        "<div style="font-family: 'Arial', sans-serif; background-color: #f4f4f4; color: #333; text-align: center; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin: 20px; max-width: 800px; margin-left: auto; margin-right: auto;">

            <h1 style="color: #007bff; font-size: 2.5em; margin-bottom: 20px;">baslik</h1>

            ... (diğer içerikler) ...

        </div>"
        hiçbir açıklama ve benzeri metin istemiyorum açıklayıcı ve detaylı bir içerik olsun tasarımdan şaşma belirtilen gereksinimleri karşıla. Kod örnekleri bölümüne ekstra dikkat et. Satırların alt alta geldiğine dikkat et ve kod örneklerini düzgün bir şekilde yerleştir. kod kısmını hafif bir şekilde renklendirebilirsin. Kendine göre ** gibi tasarımsal elementler kullanma sadece html bootstrap olsun ve inner css de kullanabilirsin. Kod örnekleri için code etiketlerinin classı 
        {subject} = python ise language-python
        {subject} = csharp ise language-csharp
        {subject} = java ise language-java
        {subject} = javascript ise language-javascript
        diğerleride hangi dilse prism.js kütüphanesine uygun class lar alsın.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
        if(response):
            self.response = response.text.splitlines()
            self.response = "\n".join(self.response[1:-1])  
        return self.response  

    def send_to_website(self,header,subject):
        service = Service(executable_path="/Users/shzany/AI-Destekli-Kurs-Platformu-Python-Django/chromedriver")
        driver = webdriver.Chrome(service=service, options=self.options)

        try:
            driver.get("http://localhost:8000/admin")

            username = driver.find_element(By.NAME, "username")
            username.send_keys("shzany")
            password = driver.find_element(By.NAME, "password")
            password.send_keys("Unuttum1905m")
            submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit.click()
            time.sleep(2)
            driver.get("http://localhost:8000/admin/pages/page/add")
            time.sleep(2)

            title = driver.find_element(By.NAME, "title")
            title.send_keys(header)  

            content = driver.find_element(By.NAME, "content")
            content.send_keys(self.response)  

            image = driver.find_element(By.NAME, "image")
            image.send_keys("img-2.jpg")
            
            category = driver.find_element(By.NAME, "category")
            category.send_keys(subject)

            save = driver.find_element(By.NAME, "_save")
            save.click()
        
        except Exception as e:
            print(f"Hata oluştu: {e}")
        
        finally:
            driver.quit()  

subject = input("Konu ne olsun: ")
bot = DesignWebsite()
prompts = bot.create_prompts(subject=subject)
for prompt in prompts:
    prompt = prompt.lstrip("*")
    bot.create_content(prompt, subject)
    print(prompt)
    bot.send_to_website(prompt,subject=subject)
    print("Sayfa üretildi")