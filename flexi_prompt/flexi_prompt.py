import re

MAX_TEMPLATE_DEPTH = 10000


class FlexiPrompt:
    def __init__(self, chunks_dict: dict = None):
        if chunks_dict is None:
            chunks_dict = {}
        if not isinstance(chunks_dict, dict):
            raise TypeError("chunks_dict must be a dictionary")
        self.chunks_dict = chunks_dict
        self.prompt = ""

    def __getattr__(self, name: str):
        if name in self.chunks_dict:

            class TemplateProperty:
                def __init__(self, superself, name, value):
                    self.name = name
                    self.value = value
                    self.superself = superself

                def __call__(self):
                    # Add the template value to the prompt when called as a function
                    self.value = self.superself._expand_named_templates(
                        self.value, set()
                    )
                    self.superself.prompt = self.superself.prompt + self.value
                    return self.superself

                def __repr__(self):
                    # Return the current value of the template when accessed as a simple value
                    return self.value

            return TemplateProperty(self, name, self.chunks_dict[name])
        else:
            if name in ["chunks_dict", "prompt"]:
                return super().__getattr__(name)
            raise AttributeError(f"'PromptBuilder' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: str):
        if name in ["chunks_dict", "prompt"]:
            super().__setattr__(name, value)
        else:
            self.chunks_dict[name] = value

    def _expand_named_templates(self, chunk: str, visited: set):
        pattern = r"\$(\w+)"
        for _ in range(MAX_TEMPLATE_DEPTH):
            match = re.search(pattern, chunk)
            if match is None:
                break
            name = match.group(1)
            if name in visited:
                raise ValueError("Template recursion detected")
            visited.add(name)
            if name in self.chunks_dict:
                replacement = self.chunks_dict[name]

                for _2 in range(MAX_TEMPLATE_DEPTH):
                    if callable(replacement):
                        replacement = replacement()
                    elif isinstance(replacement, FlexiPrompt):
                        replacement = replacement.build()
                    else:
                        replacement = str( replacement )
                        chunk = chunk.replace(f"${name}", replacement)
                        break
        else:
            raise ValueError("Template recursion exceeded maximum depth")
        return chunk

    def is_infinite_recursion(self, name: str, visited: set = None):
        """
        Check if a template value will cause infinite recursion.

        Args:
            name: The name of the template value to check.
            visited: A set of template names that have already been visited.

        Returns:
            True if the template value will cause infinite recursion, False otherwise.
        """
        if visited is None:
            visited = set()
        if name in visited:
            return True
        visited.add(name)
        if name in self.chunks_dict:
            pattern = r"\$(\w+)"
            matches = re.findall(pattern, self.chunks_dict[name])
            for match in matches:
                if self.is_infinite_recursion(match, visited):
                    return True
        visited.remove(name)
        return False

    def reset(self):
        """
        Reset the prompt to an empty string and return the current object.
        """
        self.prompt = ""
        return self

    def build(self) -> str:
        """
        Return the current prompt and reset it to an empty string.

        Returns:
            str: The current prompt.
        """
        result = self.prompt
        self.prompt = ""
        return result
