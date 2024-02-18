from flask import Flask, request, jsonify

app = Flask(__name__)

char_positions_filename = ""  # Початкове значення для імені файлу з позиціями символів

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Шандабило Олександр</title>
      <!-- Bootstrap CSS -->
      <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
      <style>
        /* Optional CSS styles for customization */
        .footer {
          background-color: #f8f9fa;
          padding: 20px 0;
          text-align: center;
        }
        .expandable {
          resize: both;
          overflow: auto;
        }
        .custom-input {
          font-size: inherit;
          min-height: 38px;
        }
        .custom-textarea {
          font-size: inherit;
          min-height: 100px;
        }
        /* Add margin between input and button */
        .form-inline .form-control {
          margin-right: 10px;
        }
        .padding {
          margin-top: 10px; /* Відступ зверху */
          height: 50px;
        }
        label {
          display: inline-block;
          background-color: indigo;
          color: white;
          padding: 0.4rem;
          font-family: sans-serif;
          border-radius: 0.3rem;
          cursor: pointer;
          margin-top: 1rem;
          margin-left: 10px; /* Відступ від кнопки Generate */
        }
        #upload {
          //display: none; /* Ховаємо стандартний input type="file" */
        }
        .navbar-toggler-icon {
          margin-left: auto;
          margin-right: auto;
        }
        .ml-auto {
          margin-left: auto !important;
        }
      </style>
    </head>
    <body>
      <!-- Navigation -->
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Метод шифрування</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <div class="ml-auto">
            <button class="btn btn-primary my-2 my-sm-0 mr-2" type="button" onclick="runScript(); startDownload();">Generate</button> <!-- Кнопка Generate -->
            <input type="file" id="fileInput" name="fileInput" onchange="uploadFile()" style="width:200px"" />
            <!--- <label for="upload" class="btn btn-primary my-2 my-sm-0">Choose file</label> ---><!-- Кнопка Choose file -->
          </div>
        </div>
      </nav>

      <!-- Content -->
      <div class="container mt-3">
        <div class="row">
          <div class="col-md-6 mt-3 mt-md-0">
            <form class="form-inline">
              <input class="form-control mr-sm-2 expandable custom-input col-md-12" id="inputTextf" type="text" placeholder="Enter Text" oninput="adjustInputSize(this)">
              <div class="padding"></div> <!-- Відступ -->
              <button id="encryptButton" class="btn btn-primary my-2 my-sm-0 mt-2" type="button">Encrypt</button>
            </form>
          </div>
          <div class="col-md-6">
            <textarea class="form-control expandable custom-input custom-textarea" rows="10" placeholder="Output Information" id="encryptedText"></textarea>
          </div>
        </div>
      </div>
      
      <!-- Duplicate Content -->
      <div class="container mt-3">
        <div class="row">
          <div class="col-md-6 mt-3 mt-md-0">
            <form class="form-inline">
              <input class="form-control mr-sm-2 expandable custom-input col-md-12" id="inputTextn" type="text" placeholder="Enter Text" oninput="adjustInputSize(this)">
              <div class="padding"></div> <!-- Відступ -->
              <button id="decryptButton" class="btn btn-primary my-2 my-sm-0 mt-2" type="button">Decrypt</button>
            </form>
          </div>
          <div class="col-md-6">
            <textarea class="form-control expandable custom-input custom-textarea" rows="10" placeholder="Decrypted Information" id="decryptedText"></textarea>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="footer mt-5">
        <div class="container">
          <p>Розробник Шандабило Олександр &copy; 2024</p>
        </div>
      </footer>

      <!-- Bootstrap JS (optional) -->
      <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
      <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
      
      <script>
        function adjustInputSize(inputField) {
          inputField.style.height = 'auto';
          inputField.style.height = (inputField.scrollHeight) + 'px';
        }
      </script>
      <script>
        function runScript() {
          fetch('/run-script')
            .then(response => {
              if (response.ok) {
                alert('Python script executed successfully!');
              } else {
                alert('Error executing Python script!');
              }
            });
        }
      </script>
      <script>
        function downloadTextFile() {
          var fileUrl = 'randomtext.txt'; 
          var a = document.createElement('a');
          a.href = fileUrl;
          a.download = 'randomtext.txt';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        }

        function startDownload() {
          setTimeout(downloadTextFile, 1000); // Задержка в 1 секунду
        }
      </script>
      <script>
        function uploadFile() {
          var fileInput = document.getElementById('fileInput');
          var file = fileInput.files[0];
          var formData = new FormData();
          formData.append('file', file);

          fetch('/upload', {
            method: 'POST',
            body: formData
          })
            .then(response => {
              if (response.ok) {
                alert('File uploaded successfully!');
              } else {
                alert('Error uploading file!');
              }
            })
            .catch(error => console.error('Error:', error));
        }
      </script>
      
    <script>
    document.getElementById('encryptButton').addEventListener('click', function() {
        var inputText = document.getElementById('inputTextf').value;

        fetch('/encrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: inputText })  // Виправлений параметр text
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('encryptedText').value = data.result;
        })
        .catch(error => console.error('Error:', error));
    });
    </script>

    <script>
    document.getElementById('decryptButton').addEventListener('click', function() {
        var inputText = document.getElementById('inputTextn').value;

        fetch('/decrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: inputText })  // Виправлений параметр text
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('decryptedText').value = data.result;
        })
        .catch(error => console.error('Error:', error));
    });
    </script>
    
    </body>
    </html>
    '''

@app.route('/run-script')
def run_script():
    # Тут ви можете виконати будь-які дії, які вам потрібні, наприклад, запуск Python-скрипта
    try:
        subprocess.run(['python', 'generator.py'])  # Виконати ваш Python-скрипт
        return '', 200
    except Exception as e:
        print(e)
        return '', 500

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Обробка завантаженого файлу тут
    # Наприклад, можна зберегти його на сервері:
    global char_positions_filename  # Використовуємо глобальну змінну
    char_positions_filename = file.filename  # Оновлюємо ім'я файлу з позиціями символів

    file_path = 'uploads/' + file.filename
    file.save(file.filename)

    return 'File uploaded successfully', 200

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json  # Отримуємо дані з JSON-формату
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    input_text = data['text']  # Отримуємо текст з даних
    try:
        # Застосування певних дій до вмісту файлу
        def encrypt_word(inputValue, char_positions, real_positions):
            encrypted_word = ''
            for char in inputValue:
                if char in real_positions:
                    char_index = real_positions[char] - 1
                    encrypted_char = list(char_positions.keys())[char_index]
                    encrypted_word += encrypted_char
                else:
                    encrypted_word += char  # Додавання пробілів до зашифрованого слова
            return encrypted_word

        def generate_real_positions():
            real_positions = {chr(i): i - 32 for i in range(33, 127)}
            return real_positions

        def read_character_positions(filename):
            with open(filename, 'r') as file:
                content = file.readlines()

            first_row = content[0].strip().split()

            char_positions = {}
            for index, char in enumerate(first_row, start=1):
                char_positions[char] = index

            return char_positions

        global char_positions_filename  # Використовуємо глобальну змінну
        char_positions = read_character_positions(char_positions_filename)

        real_positions = generate_real_positions()

        encrypted_word = encrypt_word(input_text, char_positions, real_positions)

        return jsonify({'result': encrypted_word}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


    
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json  # Отримуємо дані з JSON-формату
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    input_text = data['text']  # Отримуємо текст з даних
    try:
        # Операції розшифрування

        def decrypt_word(encrypted_word, char_positions, real_positions):
            decrypted_word = ''
            word_buffer = ''
            for char in encrypted_word:
                if char in char_positions:
                    char_index = char_positions[char] - 1  # Отримуємо позицію символу в char_positions
                    decrypted_char = list(real_positions.keys())[char_index]  # Отримуємо реальний символ зі словника real_positions
                    word_buffer += decrypted_char
                else:
                    word_buffer += char
                    if len(word_buffer) > 1:
                        decrypted_word += word_buffer
                    word_buffer = ''
            if len(word_buffer) > 1:
                decrypted_word += word_buffer
            return decrypted_word

        def read_character_positions(filename):
            with open(filename, 'r') as file:
                content = file.readlines()

            first_row = content[0].strip().split()

            char_positions = {}
            for index, char in enumerate(first_row, start=1):
                char_positions[char] = index

            return char_positions

        def generate_real_positions():
            real_positions = {chr(i): i - 32 for i in range(33, 127)}
            return real_positions

        global char_positions_filename  # Використовуємо глобальну змінну
        char_positions = read_character_positions(char_positions_filename)

        real_positions = generate_real_positions()

        decrypted_text = decrypt_word(input_text, char_positions, real_positions)

        return jsonify({'result': decrypted_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
