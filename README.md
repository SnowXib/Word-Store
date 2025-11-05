<img width="128" height="128" alt="image" src="https://github.com/user-attachments/assets/2371aecd-9443-4ef3-b5d9-8581ff7be512" />
![Version](https://img.shields.io/badge/version-0.1-blue)
![Language](https://img.shields.io/badge/Python-3.13-00ADD8)
# Word Store

<img width="345" height="488" alt="Снимок экрана 2025-11-05 в 12 37 51" src="https://github.com/user-attachments/assets/74333414-13a1-4532-a869-41ea1f480dfd" />


Расширение для обучения новым языкам

---

## Как приступить к работе

- Склонируйте репозиторий

```bash
git clone https://github.com/SnowXib/Word-Store
```

- Создайте виртуальное окружение и установите зависимости
```bash
python3.13 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

- Настройте работу расширения в google chrome
Нажмите на иконку расширения в chrome

<img width="158" height="54" alt="Снимок экрана 2025-11-05 в 12 09 42" src="https://github.com/user-attachments/assets/9a9b06e8-4090-4c18-8d45-49cd39ad6dab" />

Затем нажмите на "Управление расширениями"   

<img width="334" height="330" alt="Снимок экрана 2025-11-05 в 12 11 30" src="https://github.com/user-attachments/assets/2a9ed18b-6246-4187-9969-4f978e56c9e3" />

Включите режим разработчика в правом верхнем углу

<img width="485" height="293" alt="Снимок экрана 2025-11-05 в 12 13 13" src="https://github.com/user-attachments/assets/4a66673d-07e5-4cec-86ba-f9c148138a25" />

Нажмите "Загрузить распакованное расширение"

<img width="420" height="370" alt="Снимок экрана 2025-11-05 в 12 14 11" src="https://github.com/user-attachments/assets/c952bd8c-b51f-4607-aeae-e9e7bbbcedca" />

В нем выберете **папку extension** в директории в которой склонировали репозиторий

<img width="681" height="361" alt="Снимок экрана 2025-11-05 в 12 15 32" src="https://github.com/user-attachments/assets/5a174067-313a-4372-988a-1164471ed5e8" />

После этого в списке расширений должен появится Word Store

<img width="426" height="264" alt="Снимок экрана 2025-11-05 в 12 17 03" src="https://github.com/user-attachments/assets/f15bb8b5-d503-43b1-bc10-17d35e374a51" />

- Настройте работу api OpenAi
Если у вас уже есть ключ, то вставьте его в `config.json` и измените `base_url` если это необходимо.
Если у вас нет ключа, то зарегестрируйтесь в proxyapi.ru и создайте его, рекомендую пользоваться `gpt-4o-mini`, потому что стоит крайне мало, вряд ли вы потратите больше 10 рублей в месяц

<img width="1487" height="564" alt="Снимок экрана 2025-11-05 в 12 24 27" src="https://github.com/user-attachments/assets/6091ffc8-72e0-489a-8874-4f9bfc62b595" />

Если вы пока не решили хотите ли вы использовать данное расширение на постоянной основе – напишите автору и он даст вам ключ

Не забудьте добавить ключ в `config.json` в графу `api_key`, а так же актуализировать остальные поля в случае персонального кейса

- Запустите сервер
Перейдите в директорию app в расширении и запустите
```bash
uvicorn app:app --reload
```

- Протестируйте работу расширения
Нажмите на расширение Word Store в выпадающем меню
<img width="334" height="370" alt="Снимок экрана 2025-11-05 в 12 29 15" src="https://github.com/user-attachments/assets/208af707-32ba-42b6-b453-05f71b949a40" />

Если я правильно описал документацию и вы сделали все верно, то вы увидите такое окно
<img width="307" height="367" alt="Снимок экрана 2025-11-05 в 12 30 53" src="https://github.com/user-attachments/assets/ed7c9b90-9bd5-46b4-8a51-5cee8b652184" />

Затем выделите любое слово на другом языке и нажмите ПКМ, затем отправьте слово посредством нажатия Send Word: "…" и снова откройте расширение, вы должны увидеть его в таблице

<img width="314" height="362" alt="Снимок экрана 2025-11-05 в 12 36 10" src="https://github.com/user-attachments/assets/1cbbf2c0-f708-4777-81ff-b486b8f3965e" />


