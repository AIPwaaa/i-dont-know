import unittest
import tarfile
import os
from New import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создаем временный конфигурационный файл для эмулятора
        self.config_path = 'test_config.json'
        config_content = {
            "username": "test_user",
            "vfs_path": "a.tar"
        }
        with open(self.config_path, 'w') as f:
            import json
            json.dump(config_content, f)

        # Загружаем виртуальную файловую систему из архива
        self.emulator = ShellEmulator(self.config_path)

    def tearDown(self):
        # Удаляем временный конфигурационный файл после тестов
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_ls_root(self):
        # Проверка команды ls для корня
        result = self.emulator.list_directory('/')
        self.assertIn("b", result)  # Пример: ожидаем, что корневая директория содержит 'subdir'
        
    def test_ls_subdirectory(self):
        # Проверка команды ls для поддиректории
        self.emulator.change_directory('b/d')
        result = self.emulator.list_directory('')
        self.assertIn("d.txt", result)  # Пример: проверяем, что файл 'file1.txt' есть в 'subdir'

    def test_ls_invalid(self):
        result = self.emulator.list_directory('a/b/c')
        self.assertEqual(result, "ls: cannot access 'a/b/c': No such file or directory")

    def test_cd_valid(self):
        # Проверка успешного перехода в поддиректорию
        self.emulator.change_directory('b')
        self.assertEqual(self.emulator.current_dir, 'a/b')

    def test_cd_invalid(self):
        # Переход в несуществующую директорию
        result = self.emulator.change_directory('invalid_dir')
        self.assertEqual(result, "cd: no such file or directory: invalid_dir")

    def test_cd(self):
        result = self.emulator.change_directory('a/c/h')
        self.assertEqual(result, "")

    def test_find_exact(self):
        # Проверка команды find с точным совпадением
        result = self.emulator.find('fa.txt')
        self.assertIn('a/fa.txt', result)

    def test_find_wildcard(self):
        # Проверка команды find с шаблоном *
        result = self.emulator.find('fa*t')
        self.assertIn('a/fa.txt', result)

    def test_find_question_mark(self):
        # Проверка команды find с шаблоном ?
        result = self.emulator.find('f?.txt')
        self.assertIn('a/fa.txt', result)

    def test_whoami(self):
        # Проверка команды whoami
        result = self.emulator.whoami()
        self.assertEqual(result, "test_user")

    def test_cal(self):
        # Проверка команды cal
        result = self.emulator.cal()
        self.assertIn("November 2024", result)  # Ожидаем название месяца

    def test_exit_shell(self):
        # Проверка команды exit
        result = self.emulator.exit_shell()
        self.assertEqual(result, "exit")
        
if __name__ == "__main__":
    unittest.main()
