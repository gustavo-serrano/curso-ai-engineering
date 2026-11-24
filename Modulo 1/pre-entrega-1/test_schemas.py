import unittest
from pydantic import ValidationError
from schemas import ChatMessage, ModelConfig


class SchemaTests(unittest.TestCase):
    def test_valid_config(self):
        self.assertEqual(ModelConfig(provider='openai', model='test').max_tokens, 256)

    def test_invalid_config(self):
        for params in ({'temperature': 3}, {'max_tokens': 0}, {'timeout': 0}, {'provider': 'invalid'}):
            with self.subTest(params=params), self.assertRaises(ValidationError):
                ModelConfig(**({'provider': 'openai', 'model': 'test'} | params))

    def test_invalid_message(self):
        with self.assertRaises(ValidationError):
            ChatMessage(role='invalid', content='Hola')
        with self.assertRaises(ValidationError):
            ChatMessage(role='user', content='')


if __name__ == '__main__':
    unittest.main()
