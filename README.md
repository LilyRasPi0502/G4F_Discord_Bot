# G4F_Discord_Bot
基於<a href="https://pypi.org/project/gpt4free/0.0.2.6/">G4F</a> Python庫的Discord機器人

# 安裝方法
安裝python 3.7以上版本
複製以下指令貼於命令窗:
```cmd
python -m pip install -U py-cord

pip install gpt4free==0.0.2.6
```
如需在Replit上執行則:
`pip install Flask`

# 設定方法
### 以下檔案都在./data/json/目錄下:

- `CharacterSet.json`: 設定機器人的角色設定

- `DC_config.json`:
  - DC_key :<br>
  ![image](https://github.com/LilyRasPi0502/G4F_Discord_Bot/assets/115215163/45a4f069-73dc-48f1-8f73-979c81f67f77)
  - bot_ID :<br>
  ![image](https://github.com/LilyRasPi0502/G4F_Discord_Bot/assets/115215163/99d63831-3b17-452f-838c-8c3088d8a33c)
  - Master_ID: 自己的ID

- `Name.json`: 機器人暱稱與@時自動更換的名稱
  - 使用json架構Name Key可自由增減

- `Stetas.json`: 設定機器人狀態(本程式採用Playing,可在`Bot.py`內修改)

# 啟動方式
- windows:
  - 直接使用Launcher.exe或於Launcher.exe的目錄下執行Launcher.py(如無法執行請將Keep_alive相關函數註解)
- linux:
  - 於Launcher.exe的目錄下執行Launcher.py(如無法執行請將Keep_alive相關函數註解)
- Replit:
  - 執行Launcher.py
- Mac:
  - 等您贊助我就可以開發ㄌ
