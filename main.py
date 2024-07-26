import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

input_dir = os.path.join(base_dir, '/app/atualizacao_valor_condenacao/Entrada')
output_dir = os.path.join(base_dir, '/app/atualizacao_valor_condenacao/Saida')
processed_files_dir = os.path.join(base_dir, 'processed_files')
log_file = os.path.join(base_dir, 'logfile.txt')

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# arquivo
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            filename = os.path.basename(file_path)
            logging.info(f"Novo arquivo detectado: {filename}")

            try:
                # copia para output
                output_file_path = os.path.join(output_dir, f"copia_{filename}")
                shutil.copy(file_path, output_file_path)
                logging.info(f"Arquivo copiado para: {output_file_path}")

                # move arquivo original para processed_files
                processed_file_path = os.path.join(processed_files_dir, filename)
                shutil.move(file_path, processed_file_path)
                logging.info(f"Arquivo movido para: {processed_file_path}")

            except Exception as e:
                logging.error(f"Erro ao processar o arquivo {filename}: {str(e)}")


def main():
    # verifica se os diretórios existem, se não, cria-los
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(processed_files_dir, exist_ok=True)

    # Instancia o observador e o manipulador de eventos
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=input_dir, recursive=False)

    logging.info("Iniciando o monitoramento do diretório 'input'")

    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # Adiciona uma linha em branco no log para separar as execuções
    with open(log_file, 'a') as log:
        log.write("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
