import pytest
from flexi_prompt import FlexiPrompt

def test_simple_template():
    fp = FlexiPrompt()
    fp.greeting = "Hello, $name!"
    fp.name = "John"
    assert fp.greeting().build() == "Hello, John!"

def test_template_with_multiple_placeholders():
    fp = FlexiPrompt()
    fp.greeting = "Hello, $name! You are $age years old."
    fp.name = "John"
    fp.age = 30
    assert fp.greeting().build() == "Hello, John! You are 30 years old."

def test_nested_templates():
    fp = FlexiPrompt()
    fp.greeting = "Hello, $name! $introduction"
    fp.name = "John"
    fp.introduction = "I am $age years old."
    fp.age = 30
    assert fp.greeting().build() == "Hello, John! I am 30 years old."

def test_nested_builders():
    fp1 = FlexiPrompt()
    fp1.greeting = "Hello, $name!"
    fp1.name = "John"
    fp1.greeting()

    fp2 = FlexiPrompt()
    fp2.introduction = "$nestedGreeting I am $age years old."
    fp2.age = 30
    fp2.nestedGreeting = fp1

    assert fp2.introduction().build() == "Hello, John! I am 30 years old."

def test_recursion_check():
    fp = FlexiPrompt()
    fp.greeting = "Hello, $name!"
    fp.name = "$greeting"
    with pytest.raises(ValueError):
        fp.greeting().build()

def test_external_function():
    def get_name():
        return "John"

    fp = FlexiPrompt()
    fp.greeting = "Hello, $name!"
    fp.name = get_name
    assert fp.greeting().build() == "Hello, John!"
