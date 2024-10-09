# FlexiPrompt

FlexiPrompt is a flexible and powerful templating library, allowing you to create and manage text prompts with ease. It supports nested templates, prevents infinite recursion, and provides a simple yet powerful API for building complex text prompts.

## Installation

To install FlexiPrompt, you can use pip. First, ensure you have Python 3.12 or later installed.

```bash
pip install flexi_prompt
```

Alternatively, you can build and install the project from the source by running:

```bash
git clone https://github.com/VELIKII-DIVAN/flexi_prompt.git
cd flexi_prompt
pip install .
```

## Documentation

### Basic Usage

Here's a simple example to get you started:

```python
from flexi_prompt import FlexiPrompt

fp = FlexiPrompt()
fp.greeting = "Hello, $name!"
fp.name = "John"
print(fp.greeting().build())  # Output: Hello, John!
```

### Nested Templates

FlexiPrompt supports nested templates:

```python
fp1 = FlexiPrompt()
fp1.introduction = "I am $age years old."
fp1.age = 30

fp1.introduction()

fp = FlexiPrompt()
fp.greeting = "Hello, $name! $introduction"
fp.name = "John"
fp.introduction = fp1


print(fp.greeting().build())  # Output: Hello, John! I am 30 years old.
```

### External Functions

You can also use external functions in your templates:

```python
def get_name():
    # any useful actions
    # ...
    return "John"

fp = FlexiPrompt()
fp.greeting = "Hello, $name!"
fp.name = get_name
print(fp.greeting().build())  # Output: Hello, John!
```

### Preventing Infinite Recursion

FlexiPrompt ensures that templates do not cause infinite recursion:

```python
fp = FlexiPrompt()
fp.greeting = "Hello, $name!"
fp.name = "$greeting"
try:
    fp.greeting().build()
except ValueError as e:
    print(e)  # Output: Template recursion detected
```

## Features

- **Flexible Templating**: Create and manage text prompts with ease.
- **Nested Templates**: Support for nesting templates within each other.
- **External Functions**: Use external functions in your templates.
- **Recursion Detection**: Prevent infinite recursion in templates.

## Contributing

We welcome contributions to FlexiPrompt! Here are some ways you can help:

1. **Report Bugs**: If you encounter any issues, please report them on our [issue tracker](https://github.com/VELIKII-DIVAN/flexi_prompt/issues).
2. **Submit Pull Requests**: If you have a fix or new feature, feel free to submit a pull request. Please ensure your code follows our coding standards and includes tests.
3. **Improve Documentation**: Help us improve our documentation to make it easier for others to use FlexiPrompt.

### Setting Up Your Development Environment

1. **Clone the repository**:

    ```bash
    git clone https://github.com/VELIKII-DIVAN/flexi_prompt.git
    cd flexi_prompt
    ```

2. **Install dependencies**:

    ```bash
    pip install -e .[test]
    ```

3. **Run Tests**:

    We use `hatch` for testing. You can run the tests with:

    ```bash
    hatch run test
    ```

Thank you for considering contributing to FlexiPrompt!

## License

The FlexiPrompt is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).