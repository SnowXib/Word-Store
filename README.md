<img width="128" height="128" alt="Word Store Icon" src="https://github.com/user-attachments/assets/2371aecd-9443-4ef3-b5d9-8581ff7be512" align="left" />

# Word Store

> Расширение для обучения новым языкам

<br>

![Version](https://img.shields.io/badge/MVP-red)
![Version](https://img.shields.io/badge/version-0.1-blue)
![Language](https://img.shields.io/badge/Python-3.13-00ADD8)

<img width="345" height="488" alt="Word Store Interface" src="https://github.com/user-attachments/assets/74333414-13a1-4532-a869-41ea1f480dfd" />

---

## Старт

### Клонирование репозитория

```bash
git clone https://github.com/SnowXib/Word-Store
```

### Установка зависимостей

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Настройка расширения в Google Chrome

1. **Перейдите в управление расширениями**
   - Нажмите на иконку расширений в Chrome
   - Выберите "Управление расширениями"

   <img width="158" height="54" alt="Extensions Menu" src="https://github.com/user-attachments/assets/9a9b06e8-4090-4c18-8d45-49cd39ad6dab" />
   <img width="334" height="330" alt="Manage Extensions" src="https://github.com/user-attachments/assets/2a9ed18b-6246-4187-9969-4f978e56c9e3" />

2. **Включите режим разработчика**
   - Активируйте переключатель в правом верхнем углу

   <img width="485" height="293" alt="Developer Mode" src="https://github.com/user-attachments/assets/4a66673d-07e5-4cec-86ba-f9c148138a25" />

3. **Загрузите расширение**
   - Нажмите "Загрузить распакованное расширение"
   - Выберите папку **extension** из склонированного репозитория

   <img width="420" height="370" alt="Load Extension" src="https://github.com/user-attachments/assets/c952bd8c-b51f-4607-aeae-e9e7bbbcedca" />
   <img width="681" height="361" alt="Select Folder" src="https://github.com/user-attachments/assets/5a174067-313a-4372-988a-1164471ed5e8" />

4. **Проверьте установку**
   - Word Store должен появиться в списке расширений

   <img width="426" height="264" alt="Word Store in List" src="https://github.com/user-attachments/assets/f15bb8b5-d503-43b1-bc10-17d35e374a51" />

## Настройка OpenAI API

### Если у вас есть API-ключ:
- Вставьте его в `config.json`
- При необходимости измените `base_url`

### Если ключа нет:
1. Зарегистрируйтесь на [proxyapi.ru](https://proxyapi.ru)
2. Создайте API-ключ
3. Рекомендуем использовать `gpt-4o-mini` - экономичный вариант (≈10 руб./мес)

<img width="1487" height="564" alt="ProxyAPI Interface" src="https://github.com/user-attachments/assets/6091ffc8-72e0-489a-8874-4f9bfc62b595" />

> 💡 **Примечание**: Если вы хотите протестировать расширение перед регистрацией - свяжитесь с автором для получения тестового ключа.

Не забудьте добавить ключ в `config.json` в поле `api_key` и актуализировать остальные поля при необходимости.

## Запуск сервера

Перейдите в директорию `app` и выполните:

```bash
uvicorn app:app --reload
```

## Тестирование расширения

1. **Откройте расширение**
   - Нажмите на Word Store в выпадающем меню расширений

   <img width="334" height="370" alt="Open Extension" src="https://github.com/user-attachments/assets/208af707-32ba-42b6-b453-05f71b949a40" />

2. **Проверьте интерфейс**
   - При успешной настройке вы увидите основное окно

   <img width="307" height="367" alt="Main Interface" src="https://github.com/user-attachments/assets/ed7c9b90-9bd5-46b4-8a51-5cee8b652184" />

3. **Добавьте слова**
   - Выделите любое слово на иностранном языке
   - Нажмите ПКМ → "Send Word: …"
   - Откройте расширение - слово появится в таблице

   <img width="314" height="362" alt="Word Added" src="https://github.com/user-attachments/assets/1cbbf2c0-f708-4777-81ff-b486b8f3965e" />
