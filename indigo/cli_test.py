# Fire documentation

import fire

# Claude

class CLI:
    def hello(self, firstname: str, lastname: str) -> str:
        return f"Hello, {firstname.title()} {lastname.title()}"
    
    def goodbye(self, name: str) -> str:
        return f"Goodbye, {name.title()}"

if __name__ == "__main__":
    fire.Fire(CLI)
