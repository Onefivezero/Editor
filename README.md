# Editor
Demo Editor

Python kod editörü.

Yapılan her(muhtemelen) işlemi kaydediyor ve belirli aralıklarla yazılan kodun uzunluğunu ölçüyor.

Web dosyaları WEB_API'de bulunuyor

Servisi başlatmak için net.py dosyasının çalıştırılması yeterli, tarayıcıda localhost:<port numarası> yazarsanız çalışacaktır

Upload/Download kısmına geçmek için URL'ye "localhost:<port numarası>/upload" yazılması gerekiyor. Dosya yüklendikten sonra otomatik olarak download kısmına geçiş yapacaktır.

Repository temizlendi, artık sadece editor_windows ve editor_pardus olacak

Chatbox komutları:
"hata" : Chatbox, Veritabanındaki en son girilen hatayı alarak yapılan hatayı düzeltmek için tavsiyede bulunur(Şimdilik sadece "undefined variable" için)
"merhaba" : Chatbox "Merhaba!" diyerek karşılık verir
